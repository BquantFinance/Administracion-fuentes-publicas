"""ArcGIS REST (FeatureServer y MapServer): todas las entidades de una capa sin quedarse en maxRecordCount (fichas
mtdfp-cobertura-banda-ancha, igme-geologia).

Trampas que resuelve:
- Una consulta devuelve como mucho maxRecordCount (2.000 en la cobertura de banda ancha, 1.000 en el IGME) y solo
  avisa con exceededTransferLimit: entidades() pagina con resultOffset y orden por el campo OID.
- Los MapServer del IGME no admiten paginación («Pagination is not supported», con HTTP 200): se piden los
  objectIds (returnIdsOnly) y se consultan por lotes, por POST porque en la URL superan el límite de IIS.
- Los errores llegan con HTTP 200 y {"error": {...}} en el cuerpo: ErrorArcgis.
- La capa no siempre declara objectIdField (null en el IGME); se toma el campo de tipo esriFieldTypeOID.
- Fechas en milisegundos desde 1970 (esriFieldTypeDate): fechas_iso().

Uso: python scripts/clientes/arcgis.py                     cobertura FTTH de todos los municipios (8.132 filas)
     python scripts/clientes/arcgis.py URL_CAPA [WHERE]      recuento y primera entidad de cualquier capa
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from typing import Iterator

try:
    from .sesion import Bloqueado, json, sesion
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    from sesion import Bloqueado, json, sesion

COBERTURA_FTTH = ("https://services-eu1.arcgis.com/3LqdsBPalJaUFvo1/arcgis/rest/services/"
                  "cobertura_municipios_2025_hogar_ftth/FeatureServer/0")
_S = None


class ErrorArcgis(RuntimeError):
    """Error devuelto dentro del JSON (campo inexistente, consulta mal formada, paginación no admitida)."""


def _sesion():
    global _S
    if _S is None:
        _S = sesion()
    return _S


def _get(url: str, post: bool = False, **params) -> dict:
    datos = {"f": "json", **params}
    c = json(_sesion().post(url, data=datos) if post else _sesion().get(url, params=datos))
    if isinstance(c, dict) and "error" in c:
        e = c["error"]
        raise ErrorArcgis(f"{e.get('code')} {e.get('message')} {' '.join(e.get('details') or [])}".strip())
    return c


def capa(url: str) -> dict:
    """Descripción de la capa: fields, maxRecordCount, advancedQueryCapabilities.supportsPagination..."""
    return _get(url.rstrip("/"))


def campo_oid(info: dict) -> str:
    return info.get("objectIdField") or next(f["name"] for f in info["fields"] if f["type"] == "esriFieldTypeOID")


def contar(url: str, where: str = "1=1") -> int:
    return _get(f"{url.rstrip('/')}/query", where=where, returnCountOnly="true")["count"]


def entidades(url: str, where: str = "1=1", out_fields: str = "*", geometria: bool = False, out_sr: int | None = 4326,
              **params) -> Iterator[dict]:
    """Todas las entidades (attributes y, con geometria=True, geometry en out_sr) que cumplen where."""
    url = url.rstrip("/")
    info = capa(url)
    oid = campo_oid(info)
    lote = int(info.get("maxRecordCount") or 1000)
    base = {"where": where, "outFields": out_fields, "returnGeometry": str(geometria).lower(), **params}
    if geometria and out_sr:
        base["outSR"] = out_sr
    if info.get("advancedQueryCapabilities", {}).get("supportsPagination"):
        offset = 0
        while True:
            c = _get(f"{url}/query", **base, orderByFields=oid, resultOffset=offset, resultRecordCount=lote)
            feats = c.get("features", [])
            yield from feats
            offset += len(feats)
            if not feats or not c.get("exceededTransferLimit"):
                return
    else:
        ids = sorted(_get(f"{url}/query", where=where, returnIdsOnly="true").get("objectIds") or [])
        for i in range(0, len(ids), lote):
            trozo = ids[i:i + lote]
            # por POST: 1.000 ids en la URL superan el límite de IIS y la respuesta es una página HTML de error
            yield from _get(f"{url}/query", post=True, **{**base, "where": "1=1"},
                            objectIds=",".join(map(str, trozo)))["features"]


def fechas_iso(attrs: dict, info: dict) -> dict:
    """Cambia los campos esriFieldTypeDate (milisegundos desde 1970, UTC) por fecha ISO."""
    for f in info["fields"]:
        v = attrs.get(f["name"])
        if f["type"] == "esriFieldTypeDate" and isinstance(v, (int, float)):
            attrs[f["name"]] = datetime.fromtimestamp(v / 1000, tz=timezone.utc).isoformat()
    return attrs


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        url = args[0] if args else COBERTURA_FTTH
        where = args[1] if len(args) > 1 else "1=1"
        info = capa(url)
        print(info.get("name"), "| maxRecordCount", info.get("maxRecordCount"), "| entidades", contar(url, where))
        filas = [fechas_iso(f["attributes"], info) for f in entidades(url, where)]
        print("leídas", len(filas), "| primera", filas[0] if filas else None)
    except Bloqueado as e:
        sys.exit(f"bloqueado: {e}")
