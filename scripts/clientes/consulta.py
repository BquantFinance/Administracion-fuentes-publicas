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
import time
import zipfile
from urllib.parse import urlparse

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
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            raise ValueError(f"{host} resuelve a una dirección no pública ({ip})")


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
    _publica(url)
    r = _sesion().get(url, stream=True)
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


def tabla_pcaxis(tabla: str | int, filtro: str | None = None, max_filas: int = 200) -> dict:
    """Tabla PC-Axis en csv_bdsc (id del INE, Tabla.htm o URL de fichero) con números convertidos; filtro deja las
    filas en las que algún campo contiene el texto (un código INE, un nombre, un periodo)."""
    url = pcaxis.url_csv(tabla)
    filas = pcaxis.leer(texto(_sesion().get(url)))
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
        local = Path(__file__).resolve().parents[2] / "datos" / "municipios.csv"
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
                  "filas": aei[:max_filas]}
    prohibiciones = []
    if nombre:
        clave = normalizar_nombre(nombre)
        raiz = ET.fromstring(contenido(_sesion().get(PROHIBICIONES)))
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
        serie = sepe.municipio(m["ine"], conjunto)
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

    bloque("poblacion", poblacion)
    bloque("renta", renta)
    bloque("paro_registrado", lambda: empleo("paro"))
    bloque("contratos", lambda: empleo("contratos"))
    bloque("criminalidad", criminalidad)
    out["notas"] = ["paro registrado (SEPE) no es el desempleo de la EPA (INE)",
                    "None en paro o contratos es «<5», secreto estadístico de 1 a 4"]
    return out


if __name__ == "__main__":
    print(_json.dumps(descargar(sys.argv[1], 2000), ensure_ascii=False, indent=1, default=str))
