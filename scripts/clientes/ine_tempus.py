"""INE Tempus: Id interno del municipio para tv, nult vacío y tablas grandes con filtro (ficha ine-api-tempus).

Uso: python scripts/clientes/ine_tempus.py 02001   (código INE de municipio)
"""
from __future__ import annotations

import os
import sys

try:
    from ._http import session
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    from _http import session

BASE = "https://servicios.ine.es/wstempus/js/ES"
_cache: dict[str, dict[str, int]] = {}


def id_municipio(codigo_ine: str, operacion: str | int = 22) -> int:
    """Id interno del INE (el que exige tv=19:{Id}) a partir del código INE de 5 dígitos; una llamada, cacheada."""
    key = str(operacion)
    if key not in _cache:
        s = session()
        valores = s.get(f"{BASE}/VALORES_VARIABLEOPERACION/19/{operacion}", timeout=120, verify=s.verify).json()
        _cache[key] = {v["Codigo"]: v["Id"] for v in valores}
    try:
        return _cache[key][codigo_ine]
    except KeyError:
        raise KeyError(f"código INE {codigo_ine} no está en la variable 19 de la operación {operacion}") from None


def datos_tabla(id_tabla: int, tv: dict[int, int] | None = None, nult: int = 2) -> list[dict]:
    """DATOS_TABLA con tip=AM (fechas ISO y metadatos). nult=2 por defecto: con 1, el último periodo puede venir vacío."""
    s = session()
    params = [("nult", nult), ("tip", "AM")] + [("tv", f"{var}:{val}") for var, val in (tv or {}).items()]
    r = s.get(f"{BASE}/DATOS_TABLA/{id_tabla}", params=params, timeout=120, verify=s.verify)
    o = r.json()
    if isinstance(o, dict) and "status" in o:
        raise RuntimeError(f"INE tabla {id_tabla}: {o['status']} (añadir filtros tv)")
    for serie in o:
        serie["Data"] = [d for d in serie["Data"] if d.get("Valor") is not None]
    return o


def ultimo_valor(serie: dict) -> tuple[str, float]:
    d = serie["Data"][-1]
    return d.get("T3_Periodo") or d["Fecha"][:10], d["Valor"]


if __name__ == "__main__":
    cod = sys.argv[1] if len(sys.argv) > 1 else "02001"
    mid = id_municipio(cod)
    padron = datos_tabla(29005, tv={19: mid}, nult=2)
    renta = datos_tabla(30824, tv={19: mid, 482: 284048}, nult=1)
    print(cod, "Id", mid, "| padrón", ultimo_valor(padron[0]), "| renta neta media por persona", ultimo_valor(renta[0]))
