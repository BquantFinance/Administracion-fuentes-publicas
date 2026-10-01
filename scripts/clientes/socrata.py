"""Socrata (SODA 2) de la Generalitat de Catalunya, analisi.transparenciacatalunya.cat (ficha gencat-dades-obertes).

Trampas que resuelve:
- Sin $limit devuelve 1.000 filas sin avisar: filas() pagina con $limit, $offset y $order=:id (el orden por defecto
  lo fija la vista y no es único, así que paginar sin :id repite o salta filas).
- El JSON trae todo como texto ('98.33', '90751'): tipar() convierte con la cabecera x-soda2-types de la respuesta.
- Los errores llegan en JSON con código (400 query.soql.no-such-column, 404 dataset.missing): ErrorSocrata.
- La API de catálogo sin domains= mezcla datos de toda la red Socrata: conjuntos() filtra siempre por dominio.

Uso: python scripts/clientes/socrata.py                 embalses (gn9e-3qhr): recuento, última fila tipada
     python scripts/clientes/socrata.py ID [WHERE]      recuento y primeras filas de un conjunto
     python scripts/clientes/socrata.py --buscar TEXTO  conjuntos del dominio (buscar en catalán: municipi, no municipio)
"""
from __future__ import annotations

import json as _json
import os
import sys
from typing import Iterator

try:
    from .sesion import Bloqueado, json, sesion
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    from sesion import Bloqueado, json, sesion

DOMINIO = "analisi.transparenciacatalunya.cat"
_S = None


class ErrorSocrata(RuntimeError):
    """Error de SODA: columna inexistente, tipo que no casa en $where, conjunto inexistente o token inválido."""


def _sesion():
    global _S
    if _S is None:
        _S = sesion()
    return _S


def _soql(params: dict) -> dict:
    """where='...' pasa a $where='...'; los que ya llevan $ o son filtros simples (campo=valor) se dejan."""
    soql = {"select", "where", "order", "group", "having", "q", "limit", "offset"}
    return {(f"${k}" if k in soql else k): v for k, v in params.items() if v is not None}


def _get(ruta: str, params: dict, dominio: str):
    r = _sesion().get(f"https://{dominio}{ruta}", params=params)
    cuerpo = json(r) if r.content.strip() else None
    if r.status_code >= 400 or (isinstance(cuerpo, dict) and cuerpo.get("error")):
        msg = cuerpo.get("message", "") if isinstance(cuerpo, dict) else r.text[:200]
        raise ErrorSocrata(f"HTTP {r.status_code} {cuerpo.get('code', '') if isinstance(cuerpo, dict) else ''} "
                           f"{msg[:300]}".strip())
    return r, cuerpo


def tipar(filas: list[dict], tipos: dict[str, str]) -> list[dict]:
    """Convierte los textos según el tipo de cada campo: number a int o float, checkbox a bool; el resto igual."""
    numericos = {c for c, t in tipos.items() if t in ("number", "double", "money", "percent")}
    for f in filas:
        for c in numericos & f.keys():
            v = f[c]
            if isinstance(v, str):
                n = float(v)
                f[c] = int(n) if n.is_integer() and "." not in v and "e" not in v.lower() else n
        for c, t in tipos.items():
            if t == "checkbox" and isinstance(f.get(c), str):
                f[c] = f[c] == "true"
    return filas


def tipos_respuesta(r) -> dict[str, str]:
    """Campo a tipo SoQL desde las cabeceras x-soda2-fields y x-soda2-types (vienen en cada respuesta JSON)."""
    campos, tipos = r.headers.get("x-soda2-fields"), r.headers.get("x-soda2-types")
    return dict(zip(_json.loads(campos), _json.loads(tipos))) if campos and tipos else {}


def consulta(id_conjunto: str, dominio: str = DOMINIO, tipado: bool = True, **params) -> list[dict]:
    """Una llamada a /resource/{id}.json con SoQL (select, where, order, group, limit...). Pon limit: sin él, 1.000."""
    r, filas = _get(f"/resource/{id_conjunto}.json", _soql(params), dominio)
    return tipar(filas, tipos_respuesta(r)) if tipado else filas


def filas(id_conjunto: str, where: str | None = None, select: str | None = None, por_pagina: int = 50000,
          dominio: str = DOMINIO, tipado: bool = True, **params) -> Iterator[dict]:
    """Todas las filas, paginando con $order=:id; avanza tantas como llegan y para con una página vacía."""
    offset = 0
    while True:
        lote = consulta(id_conjunto, dominio, tipado, where=where, select=select, order=":id", limit=por_pagina,
                        offset=offset, **params)
        yield from lote
        offset += len(lote)
        if not lote:
            return


def contar(id_conjunto: str, where: str | None = None, dominio: str = DOMINIO) -> int:
    """Filas que cumplen where con $select=count(*). Sin filtro en conjuntos de decenas de millones tarda minutos."""
    return int(consulta(id_conjunto, dominio, False, select="count(*) AS n", where=where)[0]["n"])


def columnas(id_conjunto: str, dominio: str = DOMINIO) -> list[dict]:
    """fieldName (el que va en SoQL, sin caracteres no ASCII: estaci por Estació), name visible y dataTypeName."""
    _, vista = _get(f"/api/views/{id_conjunto}.json", {}, dominio)
    return [{"fieldName": c["fieldName"], "name": c["name"], "dataTypeName": c["dataTypeName"]}
            for c in vista["columns"] if not c["fieldName"].startswith(":")]


def conjuntos(q: str, dominio: str = DOMINIO, limite: int = 100) -> list[dict]:
    """Conjuntos del dominio que casan con q (id, name, updatedAt); siempre con domains= para no mezclar otras redes."""
    _, c = _get("/api/catalog/v1", {"domains": dominio, "only": "dataset", "q": q, "limit": limite}, dominio)
    return [{"id": x["resource"]["id"], "name": x["resource"]["name"], "updatedAt": x["resource"].get("updatedAt")}
            for x in c["results"]]


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        if args[:1] == ["--buscar"]:
            for c in conjuntos(" ".join(args[1:]), limite=20):
                print(c["id"], "|", c["name"])
        else:
            ident = args[0] if args else "gn9e-3qhr"
            where = args[1] if len(args) > 1 else None
            print(ident, "filas:", contar(ident, where))
            orden = "dia DESC" if not args else None
            for f in consulta(ident, where=where, order=orden, limit=3):
                print(" ", f)
    except Bloqueado as e:
        sys.exit(f"bloqueado: {e}")
