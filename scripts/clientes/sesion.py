"""Sesión HTTP lista para las fuentes públicas españolas: guides/cliente-http.md convertido en código.

    from fuentes_publicas.clientes.sesion import sesion, texto
    s = sesion()
    r = s.get("https://www.tesoro.es/sites/default/files/estadisticas/01.xlsx")

Lo que resuelve sin configurar nada:
- Certificados FNMT sin intermedia (quirk tls-chain-incomplete): la primera vez genera ca-age.pem (certifi, los
  bundles del entorno y las CA de FNMT) en ~/.cache/fuentes-publicas y lo usa en cada petición, aunque
  REQUESTS_CA_BUNDLE esté definido (requests lo antepondría a session.verify).
- User-Agent y Accept-Language de navegador (user-agent-browser); varios servidores dan 403 a los de curl o requests.
- Reintentos con espera ante 403 intermitentes de WAF, 429 (respeta Retry-After), 5xx y cortes de conexión.
- Páginas de bloqueo de WAF o antibots (Incapsula, Akamai, F5, Anubis): excepción Bloqueado en vez de un HTML como dato.
- texto(): UTF-8 aunque la cabecera diga ISO-8859-15 (CSV de PC-Axis), BOM y Latin-1 real; contenido(): gzip sin anunciar.
"""
from __future__ import annotations

import codecs
import gzip
import hashlib
import json as _json
import os
import re
import ssl
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
ACCEPT = "application/json, text/html;q=0.9, */*;q=0.8"
CACHE = Path(os.environ.get("FUENTES_PUBLICAS_CACHE") or Path.home() / ".cache" / "fuentes-publicas")

FNMT = "https://www.sede.fnmt.gob.es/documents/10445900/10526749"
CERTS_FNMT = [f"{FNMT}/{n}.cer" for n in (
    "AC_Componentes_Informaticos_SHA256", "AC_Servidores_Seguros_Tipo1", "AC_Servidores_Seguros_Tipo2",
    "AC_Servidores_Seguros_Tipo1_G2", "AC_Servidores_Seguros_Tipo2_G2", "AC_Servidores_Seguros_Tipo2_G2R",
    "AC_Administracion_Publica_SHA256", "AC_Sector_Publico", "AC_Sector_Publico_G2", "AC_Raiz_FNMT-RCM-SS",
    "AC_Raiz_FNMT-RCM_G2", "AC_RAIZ_FNMTRCM_Servidores_Seguros_G2R")]
# Intermedia que no está en la lista de la sede pero sí en el AIA de certificados vigentes
CERTS_EXTRA = ["http://www.cert.fnmt.es/certs/ACCOMP.crt"]

# Texto de las páginas de bloqueo vistas en las verificaciones (guides/cliente-http.md, waf-*): marca, motivo y si
# conviene repetir la petición (403 intermitente de Akamai) o no (bloqueo por IP que cada intento alarga)
BLOQUEOS = [
    ("_Incapsula_Resource", "Incapsula (REData, datos.gob.es, Catastro): rechaza IP de centros de datos", False),
    ("Incapsula incident ID", "Incapsula (REData, datos.gob.es, Catastro): rechaza IP de centros de datos", False),
    ("Petición HTTP bloqueada", "bloqueo por IP del Catastro tras ráfagas; esperar minutos o cambiar de red", False),
    ("Petici&#243;n HTTP bloqueada", "bloqueo por IP del Catastro tras ráfagas; esperar minutos o cambiar de red", False),
    ("The requested URL was rejected", "F5 (OEPM, ENAIRE): rechaza clientes automatizados", False),
    ("Request Rejected", "WAF del CTT o F5: hace falta cookie jar y User-Agent de navegador", False),
    ("Web Application Firewall has denied", "WAF de PLACSP: 200 con HTML de 187 bytes; rechaza la IP (centros de datos)", False),
    ("Making sure you", "Anubis (Digital.CSIC y otros): prueba de trabajo en JavaScript", False),
    ("hcaptcha.com", "reto hCaptcha (Open Data BCN fuera de /data/api/): probar desde una IP residencial", False),
    ("Acceso denegado", "Akamai (Seguridad Social): 403 intermitente", True),
    ("Access Denied", "Akamai: 403 intermitente o bloqueo temporal del host", True),
]
PEM_RE = re.compile(rb"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----", re.S)


class Bloqueado(requests.HTTPError):
    """El servidor devolvió una página de bloqueo (WAF o antibots) en lugar de los datos."""


def _pem(data: bytes) -> str:
    """PEM de un .cer de FNMT: algunos son PEM con cabecera de texto delante, otros DER."""
    m = PEM_RE.search(data)
    pem = m.group(0).decode("ascii") if m else ssl.DER_cert_to_PEM_cert(data)
    ssl.PEM_cert_to_DER_cert(pem)  # falla si no es un certificado
    return pem


def _bundles_entorno() -> list[str]:
    """Bundles del entorno (proxies corporativos o sandboxes) que hay que conservar para no romper el TLS."""
    vistos = []
    for var in ("EXTRA_CA_BUNDLE", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE", "SSL_CERT_FILE"):
        p = os.environ.get(var)
        # un ca-age*.pem ya contiene certifi y FNMT: incluirlo duplicaría el bundle en cada regeneración
        if p and os.path.isfile(p) and p not in vistos and not os.path.basename(p).startswith("ca-age"):
            vistos.append(p)
    return vistos


def generar_bundle(destino: str | Path, timeout: float = 40) -> tuple[Path, int, int]:
    """Escribe certifi + bundles del entorno + CA de FNMT en destino. Devuelve (ruta, descargados, total)."""
    import certifi

    partes = [Path(certifi.where()).read_text(encoding="ascii").rstrip() + "\n"]
    partes += [Path(p).read_text(encoding="ascii", errors="ignore").rstrip() + "\n" for p in _bundles_entorno()]
    ok, urls = 0, CERTS_FNMT + CERTS_EXTRA
    for url in urls:
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout)
            r.raise_for_status()
            partes.append(f"# FNMT {url.rsplit('/', 1)[-1]}\n{_pem(r.content).rstrip()}\n")
            ok += 1
        except (requests.RequestException, ssl.SSLError, ValueError) as exc:
            print(f"fuentes_publicas: no descargado {url}: {exc}", file=sys.stderr)
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("".join(partes), encoding="ascii")
    return destino, ok, len(urls)


def bundle(generar: bool = True) -> str | bool:
    """Ruta del bundle con FNMT: CA_BUNDLE, ca-age.pem en el directorio actual o en la raíz del repo, o el de la caché,
    que se genera la primera vez (uno por combinación de bundles del entorno). Sin red ni caché, True (certifi)."""
    for cand in (os.environ.get("CA_BUNDLE"), "ca-age.pem", Path(__file__).resolve().parents[2] / "ca-age.pem"):
        if cand and Path(cand).is_file():
            return str(cand)
    clave = hashlib.sha1("|".join(_bundles_entorno()).encode()).hexdigest()[:8]
    cache = CACHE / f"ca-age-{clave}.pem"
    if cache.is_file():
        return str(cache)
    if not generar:
        return True
    _, ok, _ = generar_bundle(cache)
    return str(cache) if ok else True


def bloqueo(r: requests.Response) -> tuple[str, bool] | None:
    """(motivo, reintentable) si la respuesta es una página de bloqueo de WAF o antibots; None si no lo parece."""
    if "html" not in r.headers.get("Content-Type", ""):
        return None
    largo = r.headers.get("Content-Length")
    if largo and largo.isdigit() and int(largo) > 3_000_000:
        return None
    cuerpo = r.content[:200_000].decode("utf-8", "replace")
    for marca, motivo, reintentable in BLOQUEOS:
        if marca in cuerpo and (r.status_code >= 400 or not reintentable):
            return motivo, reintentable
    return None


class Sesion(requests.Session):
    """requests.Session que pasa su verify en cada petición (si no, REQUESTS_CA_BUNDLE del entorno manda), repite los
    403 intermitentes y convierte las páginas de bloqueo en la excepción Bloqueado."""

    timeout: float = 120
    reintentos_403: int = 3
    espera: float = 1.5
    detectar_bloqueos: bool = True

    def request(self, method, url, **kwargs):
        kwargs.setdefault("verify", self.verify)
        kwargs.setdefault("timeout", self.timeout)
        repetible = method.upper() in ("GET", "HEAD", "OPTIONS")
        for intento in range(self.reintentos_403 + 1):
            r = super().request(method, url, **kwargs)
            b = bloqueo(r) if self.detectar_bloqueos and not kwargs.get("stream") else None
            if b and not b[1]:
                break  # bloqueo por IP o reto: repetir solo alarga el bloqueo
            if not (repetible and (r.status_code == 403 or b)) or intento == self.reintentos_403:
                break
            time.sleep(self.espera * 2 ** intento)
        if b:
            raise Bloqueado(f"{r.status_code} {urlparse(r.url).netloc}: {b[0]}", response=r)
        return r


def sesion(accept: str = ACCEPT, reintentos: int = 4, espera: float = 1.5, reintentar_403: bool = True,
           detectar_bloqueos: bool = True, timeout: float = 120, verify: str | bool | None = None) -> Sesion:
    """Sesión con User-Agent de navegador, bundle FNMT, reintentos con espera exponencial (429 con Retry-After, 5xx,
    cortes de conexión y 403 intermitentes) y excepción Bloqueado ante páginas de WAF. Reintenta solo GET, HEAD y
    OPTIONS; un bloqueo por IP (Catastro, Incapsula, F5) no se reintenta."""
    s = Sesion()
    s.timeout, s.espera, s.detectar_bloqueos = timeout, espera, detectar_bloqueos
    s.reintentos_403 = min(reintentos, 3) if reintentar_403 else 0
    s.headers.update({"User-Agent": UA, "Accept": accept, "Accept-Language": "es-ES,es;q=0.9"})
    s.verify = bundle() if verify is None else verify
    retry = Retry(total=reintentos, connect=reintentos, read=reintentos, status=reintentos, backoff_factor=espera,
                  status_forcelist=[429, 500, 502, 503, 504], allowed_methods=frozenset({"GET", "HEAD", "OPTIONS"}),
                  respect_retry_after_header=True, raise_on_status=False)
    adaptador = HTTPAdapter(max_retries=retry)
    s.mount("https://", adaptador)
    s.mount("http://", adaptador)
    return s


def contenido(r: requests.Response | bytes, descomprimir: bool = True) -> bytes:
    """Bytes del cuerpo; si llegan en gzip sin Content-Encoding (gzip-unannounced) y no es un .gz pedido, descomprime."""
    datos = r if isinstance(r, bytes) else r.content
    if descomprimir and datos[:2] == b"\x1f\x8b":
        ruta = "" if isinstance(r, bytes) else urlparse(r.url).path.lower()
        tipo = "" if isinstance(r, bytes) else r.headers.get("Content-Type", "")
        if not ruta.endswith((".gz", ".tgz")) and "gzip" not in tipo:
            return gzip.decompress(datos)
    return datos


def texto(r: requests.Response | bytes, encoding: str | None = None) -> str:
    """Texto con la codificación real: BOM UTF-8, UTF-8 válido aunque la cabecera diga ISO-8859-15 (CSV de PC-Axis de
    Educación, Cultura e Interior) y, si no es UTF-8, la declarada o windows-1252."""
    datos = contenido(r)
    if datos.startswith(codecs.BOM_UTF8):
        return datos[3:].decode("utf-8")
    try:
        return datos.decode("utf-8")
    except UnicodeDecodeError:
        declarada = encoding or (None if isinstance(r, bytes) else r.encoding)
        if not declarada or declarada.lower().replace("-", "") in ("iso88591", "latin1", "usascii", "ascii"):
            declarada = "cp1252"  # superconjunto de Latin-1 con €, comillas y guiones de Windows
        return datos.decode(declarada, errors="replace")


def json(r: requests.Response | bytes):
    """JSON tras quitar gzip sin anunciar y BOM; los errores en HTML con 200 (soft-errors-200) dan ValueError claro."""
    t = texto(r).lstrip()
    if t[:1] not in "[{\"0123456789-tfn":
        raise ValueError(f"no es JSON: {t[:120]!r}")
    return _json.loads(t)


_POR_DEFECTO: Sesion | None = None


def get(url: str, **kwargs) -> requests.Response:
    """GET con una sesión compartida (sesion() con los valores por defecto)."""
    global _POR_DEFECTO
    if _POR_DEFECTO is None:
        _POR_DEFECTO = sesion()
    return _POR_DEFECTO.get(url, **kwargs)
