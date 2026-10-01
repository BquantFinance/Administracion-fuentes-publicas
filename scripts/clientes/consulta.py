"""Consultas que devuelven datos listos para un agente (dict JSON compacto): la capa que usan las herramientas de datos
del servidor MCP y que también se puede llamar desde Python.

- descargar(url): cualquier URL pública con las reglas de sesion.py (CA de FNMT, User-Agent, reintentos, bloqueos de
  WAF, codificación real, gzip sin anunciar) y un resumen según el tipo: columnas y primeras filas de un CSV, claves de
  un JSON, ficheros de un ZIP. Es donde fallan los fetch de los agentes con servidores .gob.es.
- tabla_pcaxis(tabla, filtro): tablas del INE, Interior, Educación y Cultura en filas con números ya convertidos.
- boe_sumario(fecha), subvenciones_nif(nif), ckan_buscar / ckan_filas, socrata_filas.

Uso: python scripts/clientes/consulta.py URL     (imprime el JSON de descargar)
"""
from __future__ import annotations

import csv
import io
import ipaddress
import json as _json
import os
import socket
import sys
import threading
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse

try:
    from . import bdns, boe, ckan, pcaxis, socrata
    from .sesion import BLOQUEOS, CACHE, contenido, sesion, texto
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    import bdns, boe, ckan, pcaxis, socrata  # noqa: E401
    from sesion import BLOQUEOS, CACHE, contenido, sesion, texto

TOPE_BYTES = 25_000_000
MUNICIPIOS_URL = "https://raw.githubusercontent.com/BquantFinance/Administracion-fuentes-publicas/main/datos/municipios.csv"
_S = None
_MUNICIPIOS: list[dict] = []


def _sesion():
    global _S
    if _S is None:
        _S = sesion(accept="application/json, text/csv, text/html;q=0.9, */*;q=0.8")
    return _S


def _publica(url: str) -> None:
    """Solo http(s) a hosts públicos: nada de localhost, redes privadas ni metadatos de nube."""
    u = urlparse(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        raise ValueError("solo URLs http o https")
    host = u.hostname.lower()
    if host == "localhost" or host.endswith((".local", ".internal", ".localhost")):
        raise ValueError(f"host no público: {host}")
    try:
        direcciones = {ai[4][0] for ai in socket.getaddrinfo(host, u.port or 443)}
    except socket.gaierror:
        return  # sin DNS local (proxy): decide el proxy
    for d in direcciones:
        ip = ipaddress.ip_address(d.split("%")[0])
        ip = getattr(ip, "ipv4_mapped", None) or ip  # ::ffff:127.0.0.1 es 127.0.0.1 (Python < 3.13 no lo ve)
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast
                or ip.is_unspecified or not ip.is_global):  # is_global deja fuera también 100.64.0.0/10 (CGNAT)
            raise ValueError(f"{host} resuelve a una dirección no pública ({ip})")


MAX_REDIRECCIONES = 10


def _get_publica(url: str):
    """GET en streaming que sigue las redirecciones a mano y pasa cada salto por _publica: requests las sigue solo y
    una URL pública que redirige a 127.0.0.1 o a 169.254.169.254 se saltaba la comprobación."""
    s = _sesion()
    for _ in range(MAX_REDIRECCIONES + 1):
        _publica(url)
        r = s.get(url, stream=True, allow_redirects=False)
        destino = s.get_redirect_target(r)
        if not destino:
            return r
        r.close()
        url = urljoin(r.url, destino)
    raise ValueError(f"más de {MAX_REDIRECCIONES} redirecciones")


def _bloqueo(cuerpo: bytes, tipo: str, estado: int) -> str | None:
    if "html" not in tipo:
        return None
    t = cuerpo[:200_000].decode("utf-8", "replace")
    for marca, motivo, reintentable in BLOQUEOS:
        if marca in t and (estado >= 400 or not reintentable):
            return motivo
    return None


def resumen_csv(t: str, filas: int = 5) -> dict:
    muestra = t[:20000]
    sep = max(";,\t|", key=muestra.count)
    lector = list(csv.reader(io.StringIO(t), delimiter=sep))
    lector = [f for f in lector if any(c.strip() for c in f)]
    if not lector:
        return {"separador": sep, "filas": 0}
    return {"separador": sep, "columnas": lector[0], "filas": len(lector) - 1, "primeras": lector[1:1 + filas]}


def resumen_json(o) -> dict:
    if isinstance(o, list):
        r = {"tipo": "lista", "longitud": len(o)}
        if o and isinstance(o[0], dict):
            r["claves_primer_elemento"] = list(o[0])[:40]
        return r
    if isinstance(o, dict):
        r = {"tipo": "objeto", "claves": list(o)[:40]}
        for k, v in o.items():
            if isinstance(v, list):
                r[f"longitud_{k}"] = len(v)
        return r
    return {"tipo": type(o).__name__}


def descargar(url: str, max_caracteres: int = 20000, desde: int = 0) -> dict:
    """GET con las reglas del catálogo. Devuelve estado, tipo, bytes, resumen según formato y el texto desde el
    carácter `desde` hasta `max_caracteres` (truncado dice si queda más). Los binarios no traen texto."""
    r = _get_publica(url)
    partes, total = [], 0
    for trozo in r.iter_content(1 << 16):
        partes.append(trozo)
        total += len(trozo)
        if total >= TOPE_BYTES:
            break
    r.close()
    bruto = contenido(b"".join(partes)) if not urlparse(r.url).path.lower().endswith((".gz", ".tgz")) else b"".join(partes)
    tipo = r.headers.get("Content-Type", "")
    out = {"url": r.url, "estado": r.status_code, "tipo": tipo, "bytes": len(bruto), "completo": total < TOPE_BYTES}
    motivo = _bloqueo(bruto, tipo, r.status_code)
    if motivo:
        out["bloqueado"] = motivo
        return out
    ruta = urlparse(r.url).path.lower()
    if bruto[:2] == b"PK":
        try:
            z = zipfile.ZipFile(io.BytesIO(bruto))
            nombres = z.infolist()
            es_office = any(n.filename.startswith(("xl/", "word/", "ppt/")) for n in nombres)
            out["formato"] = "xlsx" if es_office and any(n.filename.startswith("xl/") for n in nombres) else "zip"
            if out["formato"] == "zip":
                out["ficheros"] = [{"nombre": n.filename, "bytes": n.file_size} for n in nombres[:200]]
            else:
                out["hojas"] = _hojas_xlsx(bruto)
        except zipfile.BadZipFile:
            out["formato"] = "zip incompleto (supera el tope de bytes)"
        return out
    if bruto[:4] == b"%PDF" or bruto[:4] in (b"\xd0\xcf\x11\xe0",):
        out["formato"] = "pdf" if bruto[:4] == b"%PDF" else "xls (BIFF, léelo con pandas y xlrd o calamine)"
        return out
    t = texto(bruto, r.encoding if r.encoding and "charset" in tipo.lower() else None)
    if "json" in tipo or t.lstrip()[:1] in "[{":
        try:
            out["formato"], out["resumen"] = "json", resumen_json(_json.loads(t))
        except ValueError:
            pass
    if "formato" not in out and ("csv" in tipo or ruta.endswith((".csv", ".px")) and "csv" in ruta or
                                 ("text/plain" in tipo and t.count(";") + t.count(",") > t.count("\n") > 1)):
        out["formato"], out["resumen"] = "csv", resumen_csv(t)
    out.setdefault("formato", "xml" if t.lstrip().startswith("<?xml") else "html" if "html" in tipo else "texto")
    out["texto"] = t[desde:desde + max_caracteres]
    out["caracteres"] = len(t)
    out["truncado"] = desde + max_caracteres < len(t)
    return out


def _hojas_xlsx(datos: bytes, filas: int = 5) -> list[dict] | str:
    try:
        import openpyxl
    except ImportError:
        return "instala openpyxl para ver hojas y primeras filas"
    wb = openpyxl.load_workbook(io.BytesIO(datos), read_only=True, data_only=True)
    hojas = []
    for ws in wb.worksheets[:20]:
        ws.reset_dimensions()
        primeras = []
        for fila in ws.iter_rows(values_only=True):
            if any(c is not None for c in fila):
                primeras.append([c if isinstance(c, (int, float, str)) or c is None else str(c) for c in fila][:30])
            if len(primeras) >= filas:
                break
        hojas.append({"hoja": ws.title, "primeras": primeras})
    return hojas


_MEMO: dict = {}
_MEMO_LOCK = threading.Lock()


def _memo(clave, ttl: float, fn):
    """Caché en memoria del proceso (el servidor MCP vive toda la sesión) para ficheros grandes que cambian poco: una
    tabla de criminalidad son 2,3 MB y antes se bajaba en cada perfil de municipio."""
    with _MEMO_LOCK:
        hit = _MEMO.get(clave)
        if hit and time.time() - hit[0] < ttl:
            return hit[1]
    valor = fn()
    with _MEMO_LOCK:
        _MEMO[clave] = (time.time(), valor)
    return valor


def tabla_pcaxis(tabla: str | int, filtro: str | None = None, max_filas: int = 200) -> dict:
    """Tabla PC-Axis en csv_bdsc (id del INE, Tabla.htm o URL de fichero) con números convertidos; filtro deja las
    filas en las que algún campo contiene el texto (un código INE, un nombre, un periodo)."""
    url = pcaxis.url_csv(tabla)
    filas = _memo(("pcaxis", url), 6 * 3600, lambda: pcaxis.leer(texto(_sesion().get(url))))
    if filtro:
        f = filtro.lower()
        filas = [x for x in filas if any(f in str(v).lower() for v in x.values())]
    return {"url": url, "columnas": list(filas[0]) if filas else [], "filas_total": len(filas), "filas": filas[:max_filas],
            "nota": "None es dato no disponible o secreto, no cero"}


def boe_sumario(fecha: str, diario: str = "boe", seccion: str | None = None, texto_titulo: str | None = None,
                max_items: int = 200) -> dict:
    """Disposiciones de un día del BOE o del BORME (fecha AAAA-MM-DD o AAAAMMDD), filtrables por código de sección
    (1, 2A, 3, 5A...) y por texto en el título."""
    s = boe.sumario(fecha, diario)
    if s is None:
        return {"fecha": fecha, "diario": diario, "items": [], "nota": "sin boletín ese día (404)"}
    its = list(boe.items(s))
    if seccion:
        its = [i for i in its if str(i.get("seccion_codigo")) == seccion]
    if texto_titulo:
        t = texto_titulo.lower()
        its = [i for i in its if t in (i.get("titulo") or "").lower()]
    campos = ("identificador", "seccion_codigo", "departamento_nombre", "epigrafe_nombre", "titulo", "url_pdf", "url_xml")
    return {"fecha": fecha, "diario": diario, "total": len(its),
            "items": [{k: i.get(k) for k in campos if i.get(k)} for i in its[:max_items]]}


def subvenciones_nif(nif: str, max_filas: int = 20) -> dict:
    """Concesiones, ayudas de Estado, minimis y grandes beneficiarios de un NIF en la BDNS, con totales y las más
    recientes. El NIF va en nifCif; beneficiario trae NIF y nombre juntos."""
    out = {"nif": nif.upper()}
    for col, orden in (("concesiones", "fechaConcesion"), ("ayudasestado", "fechaConcesion"), ("minimis", "fechaConcesion"),
                       ("grandesbeneficiarios", None)):
        o = bdns.pagina(col, 0, min(max_filas, 1000), nifCif=nif.upper(), **({"order": orden, "direccion": "desc"} if orden else {}))
        filas = o.get("content", [])
        out[col] = {"total": o.get("totalElements", len(filas)), "filas": filas[:max_filas]}
        importes = [f.get("importe") or f.get("ayudaETotal") or 0 for f in filas]
        if o.get("totalElements", 0) <= len(filas):
            out[col]["importe_total"] = round(sum(x for x in importes if isinstance(x, (int, float))), 2)
    return out


def ckan_buscar(portal: str, texto_busqueda: str, limite: int = 10) -> dict:
    res = ckan.accion(portal, "package_search", q=texto_busqueda, rows=limite)
    return {"portal": ckan.base(portal), "total": res["count"], "conjuntos": [
        {"name": p["name"], "title": p.get("title"), "recursos": [
            {"id": r["id"], "format": r.get("format"), "datastore": r.get("datastore_active"), "url": ckan.url_descarga(r)}
            for r in p.get("resources", [])]} for p in res["results"]]}


def ckan_filas(portal: str, recurso: str, filtros: dict | None = None, limite: int = 100) -> dict:
    total = ckan.total_datastore(portal, recurso)
    filas = []
    for f in ckan.filas(portal, recurso, filters=filtros, por_pagina=min(max(limite, 1), 10000)):
        filas.append(f)
        if len(filas) >= limite:
            break
    return {"total_datastore": total, "filas": filas, "aviso": "el datastore puede tener menos filas que el fichero; "
            "compara total_datastore con el CSV original (ckan.comparar) antes de dar una cifra total"}


def socrata_filas(conjunto: str, where: str | None = None, select: str | None = None, order: str | None = None,
                  limite: int = 100) -> dict:
    filas = socrata.consulta(conjunto, where=where, select=select, order=order or (None if select else ":id"),
                             limit=limite)
    return {"conjunto": conjunto, "filas": filas, "nota": "sin $limit Socrata da 1.000 filas; aquí limit es explícito"}


def municipios() -> list[dict]:
    """datos/municipios.csv del repo (o descargado de GitHub y cacheado): una fila por municipio con ine, dc, nombre,
    cpro, ccaa, provincia, nuts3, ine_tempus_id, sigpac, dir3, nif, lat, lon y nucleo (caché de 30 días)."""
    if not _MUNICIPIOS:
        from pathlib import Path
        locales = [Path(__file__).resolve().parents[2] / "datos" / "municipios.csv"]
        if os.environ.get("CATALOGO_DIR"):  # como catalog.json en mcp_catalogo.locate (la imagen Docker lo copia ahí)
            locales.insert(0, Path(os.environ["CATALOGO_DIR"]) / "datos" / "municipios.csv")
        local = next((p for p in locales if p.is_file()), locales[-1])
        cache = CACHE / "municipios.csv"
        if local.is_file():
            t = local.read_text(encoding="utf-8")
        elif cache.is_file() and time.time() - cache.stat().st_mtime < 30 * 86400:
            t = cache.read_text(encoding="utf-8")
        else:
            t = texto(_sesion().get(MUNICIPIOS_URL))
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(t, encoding="utf-8")
        _MUNICIPIOS.extend(csv.DictReader(io.StringIO(t)))
    return _MUNICIPIOS


def buscar_municipio(consulta: str, limite: int = 5, filas: list[dict] | None = None) -> list[dict]:
    """Por código INE (28079 o 280796), SIGPAC (28:900), DIR3 (L01280796), NIF del ayuntamiento o nombre (sin tildes,
    con artículo pospuesto o no: «Coruña, A», «A Coruña»)."""
    import difflib
    import unicodedata

    def norm(s: str) -> str:
        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
        partes = [p.strip() for p in s.split(",")]
        if len(partes) == 2 and len(partes[1].split()) == 1:
            s = f"{partes[1]} {partes[0]}"  # «Coruña, A» -> «a coruña»
        return " ".join("".join(c if c.isalnum() else " " for c in s).split())

    filas = filas if filas is not None else municipios()
    q = consulta.strip()
    exactos = [f for f in filas if q.upper() in (f["ine"], f["ine"] + f["dc"], f["sigpac"], f["dir3"], f["nif"])]
    if exactos:
        return exactos[:limite]
    nq = norm(q)
    iguales = [f for f in filas if nq == norm(f["nombre"]) or nq in [norm(p) for p in f["nombre"].split("/")]]
    if iguales:
        return iguales[:limite]
    contienen = sorted((f for f in filas if nq and nq in norm(f["nombre"])), key=lambda f: len(f["nombre"]))
    if contienen:
        return contienen[:limite]
    nombres = {norm(f["nombre"]): f for f in filas}
    return [nombres[n] for n in difflib.get_close_matches(nq, list(nombres), n=limite, cutoff=0.75)]


INVENTE = "https://www.pap.hacienda.gob.es/Invente2/api/EntidadesSPI_ConFiltros"
AEI_CSV = "https://www.aei.gob.es/ayudas-concedidas/buscador-ayudas-concedidas/download-unlimit/All/All/All/All"
PROHIBICIONES = "https://visor.registrodelicitadores.gob.es/svcr/controller/prohibiciones"
FORMAS = r"\b(S ?L ?U?|S ?A ?U?|S ?L ?L|S ?COOP(?: ?AND| ?V)?|SOCIEDAD (?:LIMITADA|ANONIMA)(?: UNIPERSONAL)?|SLNE|S ?C ?P?|C ?B)\b"


def normalizar_nombre(s: str) -> str:
    """Denominación comparable: sin tildes ni signos y sin forma jurídica (S.L., SA, S. COOP...)."""
    import re
    import unicodedata
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().upper()
    s = re.sub(r"[^A-Z0-9 ]+", " ", s)
    s = re.sub(FORMAS, " ", " ".join(s.split()))
    return " ".join(s.split())


def _numero_es(v: str) -> float:
    return float(v.replace(".", "").replace(",", ".")) if v and v.strip() else 0.0


def empresa_nif(nif: str, max_filas: int = 10) -> dict:
    """Lo que las fuentes públicas dicen de un NIF sin certificado: si es sector público (Invente), subvenciones,
    ayudas de Estado y minimis (BDNS), ayudas de la AEI y prohibiciones de contratar vigentes (por denominación, porque
    el XML oculta el NIF). Contratos y actos del BORME no tienen consulta por NIF: salen del almacén local si existe
    (FUENTES_ALMACEN o ./almacen, clave almacen) y si no, no_cubierto dice cómo cargarlos."""
    import xml.etree.ElementTree as ET
    nif = nif.upper().strip()
    out: dict = {"nif": nif}
    r = _sesion().get(INVENTE, params={"nif": nif})
    entes = _json.loads(texto(r)).get("EntidadesSPI", []) if r.status_code == 200 and r.content.strip() else []
    out["sector_publico"] = entes[0] if entes else None
    out["subvenciones"] = subvenciones_nif(nif, max_filas)
    nombre = entes[0]["DenominacionSocial"] if entes else None
    for col in ("concesiones", "ayudasestado", "minimis"):
        filas = out["subvenciones"][col]["filas"]
        if not nombre and filas and filas[0].get("beneficiario"):
            nombre = bdns.separar_beneficiario(filas[0]["beneficiario"])[1]
    aei = list(csv.DictReader(io.StringIO(texto(_sesion().get(AEI_CSV, params={"cif": nif}))), delimiter=";"))
    aei = [f for f in aei if (f.get("C.I.F.") or "").strip().upper() == nif]
    if not nombre and aei:
        nombre = aei[0].get("Entidad")
    out["nombre"] = nombre
    out["aei"] = {"total": len(aei), "importe_total": round(sum(_numero_es(f.get("€ Conced.", "")) for f in aei), 2),
                  "filas": sorted(aei, key=lambda f: f.get("Año") or "", reverse=True)[:max_filas]}  # el CSV va del más antiguo
    prohibiciones = []
    if nombre:
        clave = normalizar_nombre(nombre)
        raiz = ET.fromstring(_memo("prohibiciones", 6 * 3600, lambda: contenido(_sesion().get(PROHIBICIONES))))
        for p in raiz:
            d = {c.tag: (c.text or "").strip() for c in p}
            if normalizar_nombre(d.get("denominacionSocial", "")) == clave:
                prohibiciones.append({k: d.get(k) for k in ("denominacionSocial", "causaProhibicion", "ambitoProhibicion",
                                                            "autoridad", "fechaInicioProhibicion", "fechaFinProhibicion")})
    out["prohibiciones_contratar"] = prohibiciones
    try:
        from . import almacen
    except ImportError:
        import almacen
    cargar = "cargarlo en el almacén local: python scripts/clientes/almacen.py sync --fuentes placsp,borme --desde AAAA-MM-DD (guides/almacen.md)"
    d = almacen.existe()
    if d:
        try:
            out["almacen"] = almacen.empresa(nif, d, nombre, max_filas)
        except ImportError as exc:
            out["almacen"] = {"error": str(exc)}
    out["no_cubierto"] = {
        "contratos": ("solo lo cargado en el almacén (almacen.cobertura)" if d else
                      "PLACSP no tiene búsqueda por NIF: " + cargar),
        "borme": ("solo lo cargado en el almacén, por denominación" if d else
                  "el BORME no trae NIF ni búsqueda por denominación: " + cargar),
        "concursos": "publicidadconcursal.es busca por NIF, pero exige resolver un CAPTCHA",
        "deudores_aeat": "la lista del art. 95 bis LGT (deudas de más de 600.000 €) solo es accesible tres meses tras publicarse, en junio",
    }
    return out


CRIMINALIDAD = "https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_bdsc/DatosBalanceAct/l0/{}.px?nocab=1"


def perfil_municipio(municipio: str) -> dict:
    """Un municipio en una llamada: códigos en cada sistema (INE, SIGPAC y Catastro, DIR3, NIF, NUTS3, coordenadas),
    población del padrón, renta neta media por persona, paro registrado y contratos del año por mes y criminalidad. Cada
    bloque falla por separado (clave error) sin tumbar el resto. None en una cifra es secreto o sin dato, no cero."""
    try:
        from . import ine_tempus, sepe
    except ImportError:
        import ine_tempus
        import sepe
    cand = buscar_municipio(municipio, 1)
    if not cand:
        return {"error": f"no encuentro el municipio {municipio!r}", "pista": "nombre, código INE (28079), SIGPAC (28:900), DIR3 o NIF"}
    m = cand[0]
    out: dict = {"municipio": m}

    def bloque(clave, fn):
        try:
            out[clave] = fn()
        except Exception as exc:  # noqa: BLE001
            out[clave] = {"error": f"{type(exc).__name__}: {str(exc)[:200]}"}

    mid = int(m["ine_tempus_id"]) if m.get("ine_tempus_id") else ine_tempus.id_municipio(m["ine"])

    def poblacion():
        fecha, v = ine_tempus.ultimo_valor(ine_tempus.datos_tabla(29005, tv={19: mid}, nult=2)[0])
        return {"padron_a": fecha, "habitantes": v, "fuente": "ine-api-tempus, tabla 29005"}

    def renta():
        fecha, v = ine_tempus.ultimo_valor(ine_tempus.datos_tabla(30824, tv={19: mid, 482: 284048}, nult=1)[0])
        return {"anio": fecha[:4], "renta_neta_media_por_persona": v, "fuente": "ine-api-tempus, Atlas de renta, tabla 30824"}

    def empleo(conjunto):
        serie = sepe.municipio(m["ine"], conjunto, datos=_memo(("sepe", conjunto), 3600, lambda: sepe.filas(conjunto)))
        total = next(k for k in serie[-1] if k.startswith("total"))
        return {"mes": serie[-1]["mes"], total: serie[-1][total], "serie": {f["mes"]: f[total] for f in serie},
                "ultimo_desglose": serie[-1], "fuente": "sepe-estadisticas, CSV de datos abiertos"}

    def criminalidad():
        for fichero in ("09009", "09006", "09003"):  # del trimestre más reciente al primero; el que aún no existe redirige
            try:
                t = tabla_pcaxis(CRIMINALIDAD.format(fichero), f"{m['ine']} ", 200)
            except Exception:  # noqa: BLE001
                continue
            tot = [r for r in t["filas"] if "TOTAL INFRACCIONES" in str(r.get("Tipología penal")) and not str(r.get("Periodos:")).startswith("Vari")]
            if tot:
                return {"infracciones_penales": {r["Periodos:"]: r["Total"] for r in tot},
                        "nota": "acumulado desde enero, no trimestral; balance de Interior", "fuente": "interior-criminalidad"}
        return {"nota": "Interior solo publica municipios de más de 20.000 habitantes"}

    tareas = {"poblacion": poblacion, "renta": renta, "paro_registrado": lambda: empleo("paro"),
              "contratos": lambda: empleo("contratos"), "criminalidad": criminalidad}
    with ThreadPoolExecutor(len(tareas)) as ex:  # bloques independientes: el perfil tarda lo que el más lento
        futuros = {k: ex.submit(bloque, k, f) for k, f in tareas.items()}
    for k in tareas:
        futuros[k].result()
    out = {"municipio": out["municipio"], **{k: out[k] for k in tareas}}  # orden fijo, no el de llegada
    out["notas"] = ["paro registrado (SEPE) no es el desempleo de la EPA (INE)",
                    "None en paro o contratos es «<5», secreto estadístico de 1 a 4"]
    return out


# Indicadores de coyuntura: (clave, fuente, serie, descripción, nota). Códigos verificados el 2026-10-01 (indices/codigos.yaml).
INDICADORES = (
    ("ipc_variacion_anual", "ine", "IPC290750", "IPC, variación anual del índice general (%)", "base 2025; el último mes suele ser avance"),
    ("ipc_variacion_mensual", "ine", "IPC290752", "IPC, variación mensual del índice general (%)", "base 2025"),
    ("paro_epa", "ine", "EPA452434", "Tasa de paro EPA, total nacional (%)", "trimestral; no es el paro registrado"),
    ("pib_variacion_trimestral", "ine", "CNTR6653", "PIB, variación trimestral en volumen, corregida de estacionalidad y calendario (%)",
     "la serie sin corregir (CNTR6722) da otra cifra"),
    ("pib_variacion_anual", "ine", "CNTR6654", "PIB, variación anual en volumen, corregida de estacionalidad y calendario (%)", ""),
    ("paro_registrado", "bde", "D_1JA0D000", "Paro registrado (personas)", "el BdE pone unidad «m pers.», pero son personas"),
    ("euribor_12m", "bde", "D_1NBAF472", "Euríbor a un año, media mensual (%)", ""),
    ("dolar_por_euro", "bde", "DTCCBCEUSDEUR.B", "Dólares estadounidenses por euro", "diario"),
    ("deuda_pde_pib", "bde", "DTNPDE2010_P0000P_PS_APU", "Deuda PDE de las AAPP (% del PIB)", "trimestral"),
    ("bono_10_anios", "bde", "D_G2B1I0ZP", "Rendimiento del bono del Estado a 10 años, media mensual (%)", ""),
    ("bono_aleman_10_anios", "bde", "D_1NBBO308", "Rendimiento de la deuda alemana a 10 años, media mensual (%)", "suele ir un mes por detrás"),
)
TIPO_DATO_INE = {1: "definitivo", 2: "provisional", 3: "avance"}
BDE_API = "https://app.bde.es/bierest/resources/srdatosapp"


def ine_ultimo(serie: dict) -> dict:
    """Último dato con valor de un DATOS_SERIE con tip=AM: periodo (2026-09, 2026T2, 2025), valor y tipo (definitivo,
    provisional o avance; el IPC del último mes suele ser avance y se revisa)."""
    d = max((x for x in serie.get("Data", []) if x.get("Valor") is not None), key=lambda x: x["Fecha"])
    p = d.get("T3_Periodo") or ""
    periodo = f"{d['Anyo']}-{p[1:]}" if p.startswith("M") else f"{d['Anyo']}{p}" if p.startswith("T") else str(d["Anyo"])
    tipo = d.get("T3_TipoDato") or TIPO_DATO_INE.get(d.get("FK_TipoDato"), "")
    return {"periodo": periodo, "valor": d["Valor"], "tipo": tipo.lower()}


def bde_periodo(fecha_valor: str, frecuencia: str) -> str:
    """El BdE fecha cada periodo por su primer día: 2026-04-01 con frecuencia Q es 2026T2, 2026-09-01 con M es 2026-09."""
    f = (fecha_valor or "")[:10]
    if frecuencia == "M":
        return f[:7]
    if frecuencia == "Q":
        return f"{f[:4]}T{(int(f[5:7]) - 1) // 3 + 1}"
    if frecuencia == "A":
        return f[:4]
    return f


def coyuntura() -> dict:
    """Como _coyuntura, con media hora de caché en memoria."""
    return _memo("coyuntura", 1800, _coyuntura)


def _coyuntura() -> dict:
    """Último dato de los indicadores de coyuntura de España en una llamada (INE y Banco de España), cada uno con su
    periodo, tipo de dato, serie y fuente, y la prima de riesgo calculada en el último mes común (bono español menos
    alemán, en puntos básicos). Un indicador que falle trae error sin tumbar el resto."""
    out: dict = {}
    s = _sesion()
    bde_codigos = [c for _, f, c, _, _ in INDICADORES if f == "bde"]
    try:
        bde = {x["serie"]: x for x in s.get(f"{BDE_API}/favoritas", params={"idioma": "es", "series": ",".join(bde_codigos)}).json()}
    except Exception as exc:  # noqa: BLE001
        bde = {"_error": str(exc)[:200]}
    for clave, fuente, cod, desc, nota in INDICADORES:
        try:
            if fuente == "ine":
                r = s.get(f"https://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/{cod}", params={"nult": 2, "tip": "AM"}).json()
                dato = ine_ultimo(r)
                fuente_id = "ine-api-tempus"
            else:
                x = bde[cod]
                if x.get("errNum"):
                    raise KeyError(f"{cod}: {x.get('errNum')}")
                dato = {"periodo": bde_periodo(x.get("fechaValor"), x.get("codFrecuencia")), "valor": x.get("valor")}
                fuente_id = "bde-estadisticas"
            out[clave] = dict(dato, descripcion=desc, serie=cod, fuente=fuente_id, **({"nota": nota} if nota else {}))
        except Exception as exc:  # noqa: BLE001
            out[clave] = {"error": f"{type(exc).__name__}: {str(exc)[:200]}", "serie": cod}
    try:
        series = s.get(f"{BDE_API}/listaSeries", params={"idioma": "es", "series": "D_G2B1I0ZP,D_1NBBO308", "rango": "30M"}).json()
        v = {x["serie"]: dict(zip((f[:7] for f in x["fechas"]), x["valores"])) for x in series}
        comun = max(set(v["D_G2B1I0ZP"]) & set(v["D_1NBBO308"]))
        out["prima_riesgo"] = {"periodo": comun, "valor": round((v["D_G2B1I0ZP"][comun] - v["D_1NBBO308"][comun]) * 100),
                               "descripcion": "Prima de riesgo frente a Alemania a 10 años (puntos básicos), medias mensuales",
                               "nota": "calculada en el último mes con los dos datos; el alemán suele ir un mes por detrás",
                               "fuente": "bde-estadisticas"}
    except Exception as exc:  # noqa: BLE001
        out["prima_riesgo"] = {"error": f"{type(exc).__name__}: {str(exc)[:200]}"}
    return out


def en_lote(fn, valores: list, paralelo: int = 4) -> list:
    """Aplica fn a varios valores a la vez (perfiles de municipio, empresas por NIF); un fallo queda en su posición."""
    def uno(v):
        try:
            return fn(v)
        except Exception as exc:  # noqa: BLE001
            return {"consulta": v, "error": f"{type(exc).__name__}: {str(exc)[:200]}"}
    with ThreadPoolExecutor(max(1, min(paralelo, len(valores)))) as ex:
        return list(ex.map(uno, valores))


if __name__ == "__main__":
    print(_json.dumps(descargar(sys.argv[1], 2000), ensure_ascii=False, indent=1, default=str))
