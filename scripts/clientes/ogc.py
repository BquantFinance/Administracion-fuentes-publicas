"""OGC API Features (SIGPAC, IDEE, IGN, INE geoserver): todas las entidades de una consulta siguiendo rel=next (fichas
mapa-sigpac, idee-servicios, ine-cartografia-censal).

Trampas que resuelve:
- limit se recorta sin aviso (250 en SIGPAC aunque se pidan 1.000): se sigue el enlace next, que ya lleva el limit
  y el offset reales, en vez de calcular offset con el limit pedido.
- numberMatched no es fiable (IDEE dio 0 y 988 para la misma consulta): solo se para cuando falta next o llega una
  página vacía.
- El next de SIGPAC añade bbox-crs EPSG:4258 y pierde f=json; se pide GeoJSON por cabecera Accept para que las páginas
  siguientes sigan en JSON. bbox va siempre en lon,lat.

Uso: python scripts/clientes/ogc.py                                   recintos SIGPAC de un bbox (4.938, páginas de 250)
     python scripts/clientes/ogc.py URL_ITEMS [clave=valor ...]         cualquier colección; bbox=..., limit=..., filtros
"""
from __future__ import annotations

import os
import sys
from typing import Iterator

try:
    from .sesion import Bloqueado, json, sesion
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    from sesion import Bloqueado, json, sesion

SIGPAC = "https://sigpac-hubcloud.es/ogcapi"
_S = None


def _sesion():
    global _S
    if _S is None:
        _S = sesion(accept="application/geo+json, application/json;q=0.9")
    return _S


def colecciones(base: str) -> list[dict]:
    """id y title de las colecciones de un servicio (base sin /collections)."""
    c = json(_sesion().get(f"{base.rstrip('/')}/collections"))
    return [{"id": x["id"], "title": x.get("title")} for x in c["collections"]]


def siguiente(pagina: dict) -> str | None:
    return next((l["href"] for l in pagina.get("links", []) if l.get("rel") == "next"), None)


def paginas(url_items: str, max_paginas: int | None = None, **params) -> Iterator[dict]:
    """Cada FeatureCollection de la consulta, siguiendo next; para en una página vacía o si next se repite."""
    url, vistas, n = url_items, set(), 0
    while url and url not in vistas:
        vistas.add(url)
        pagina = json(_sesion().get(url, params=params if n == 0 else None))
        yield pagina
        n += 1
        if not pagina.get("features") or (max_paginas and n >= max_paginas):
            return
        url = siguiente(pagina)


def entidades(url_items: str, limit: int = 1000, **params) -> Iterator[dict]:
    """Todas las features de /collections/{id}/items con los filtros dados (bbox lon,lat, propiedades, CQL...)."""
    for pagina in paginas(url_items, limit=limit, **params):
        yield from pagina.get("features", [])


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        if args:
            url, params = args[0], dict(a.split("=", 1) for a in args[1:])
        else:
            url, params = f"{SIGPAC}/collections/recintos/items", {"bbox": "-4.10,39.80,-4.00,39.90"}
        primera = None
        tam, ids = [], set()
        for p in paginas(url, **{"limit": 1000, **params}):
            primera = primera or p
            tam.append(len(p.get("features", [])))
            ids |= {f.get("id") for f in p.get("features", [])}
        print("numberMatched", primera.get("numberMatched"), "| páginas", len(tam), "de", sorted(set(tam), reverse=True)[:2],
              "| entidades", sum(tam), "| ids distintos", len(ids))
    except Bloqueado as e:
        sys.exit(f"bloqueado: {e}")
