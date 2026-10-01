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
import zipfile
from urllib.parse import urlparse

try:
    from . import bdns, boe, ckan, pcaxis, socrata
    from .sesion import BLOQUEOS, contenido, sesion, texto
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    import bdns, boe, ckan, pcaxis, socrata  # noqa: E401
    from sesion import BLOQUEOS, contenido, sesion, texto

TOPE_BYTES = 25_000_000
_S = None


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


if __name__ == "__main__":
    print(_json.dumps(descargar(sys.argv[1], 2000), ensure_ascii=False, indent=1, default=str))
