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
    """Id interno del INE (el que exige tv=19:{Id}) a partir del código INE de 5 dígitos. Para la operación 22 sale de
    datos/municipios.csv (columna ine_tempus_id); si no, una llamada lenta (30 s o más), cacheada."""
    key = str(operacion)
    if key == "22" and key not in _cache:
        try:
            try:
                from .consulta import municipios
            except ImportError:
                from consulta import municipios
            ids = {f["ine"]: int(f["ine_tempus_id"]) for f in municipios() if f.get("ine_tempus_id")}
            if ids:
                _cache[key] = ids
        except Exception:  # noqa: BLE001  (sin CSV ni red a GitHub: se pide al INE)
            pass
    if key not in _cache:
        s = session()
        _cache[key] = mapa_ids(s.get(f"{BASE}/VALORES_VARIABLEOPERACION/19/{operacion}", timeout=120, verify=s.verify).json())
    try:
        return _cache[key][codigo_ine]
    except KeyError:
        raise KeyError(f"código INE {codigo_ine} no está en la variable 19 de la operación {operacion}") from None


def mapa_ids(valores: list[dict]) -> dict[str, int]:
    """Código INE (Codigo) a Id interno, a partir de VALORES_VARIABLEOPERACION/19/{operacion}."""
    return {v["Codigo"]: v["Id"] for v in valores}


def limpiar_tabla(o, id_tabla: int | str = "") -> list[dict]:
    """Respuesta de DATOS_TABLA sin periodos vacíos; una tabla grande sin filtros devuelve {"status": ...} con HTTP 200."""
    if isinstance(o, dict) and "status" in o:
        raise RuntimeError(f"INE tabla {id_tabla}: {o['status']} (añadir filtros tv)")
    for serie in o:
        serie["Data"] = [d for d in serie["Data"] if d.get("Valor") is not None]
    return o


def datos_tabla(id_tabla: int, tv: dict[int, int] | None = None, nult: int = 2) -> list[dict]:
    """DATOS_TABLA con tip=AM (fechas ISO y metadatos). nult=2 por defecto: con 1, el último periodo puede venir vacío."""
    s = session()
    params = [("nult", nult), ("tip", "AM")] + [("tv", f"{var}:{val}") for var, val in (tv or {}).items()]
    return limpiar_tabla(s.get(f"{BASE}/DATOS_TABLA/{id_tabla}", params=params, timeout=120, verify=s.verify).json(), id_tabla)


def ultimo_valor(serie: dict) -> tuple[str, float]:
    """Dato más reciente por Fecha: DATOS_TABLA devuelve Data del periodo más reciente al más antiguo."""
    d = max(serie["Data"], key=lambda d: d["Fecha"])
    return d["Fecha"][:10], d["Valor"]


if __name__ == "__main__":
    cod = sys.argv[1] if len(sys.argv) > 1 else "02001"
    mid = id_municipio(cod)
    padron = datos_tabla(29005, tv={19: mid}, nult=2)
    renta = datos_tabla(30824, tv={19: mid, 482: 284048}, nult=1)
    print(cod, "Id", mid, "| padrón", ultimo_valor(padron[0]), "| renta neta media por persona", ultimo_valor(renta[0]))
