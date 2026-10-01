"""CKAN de los portales autonómicos, municipales y de organismos: paginación sin topes silenciosos y contraste del
datastore con el fichero (fichas comunidad-madrid-datos-abiertos, ayuntamiento-madrid-datos-abiertos,
ayuntamiento-barcelona-datos-abiertos, gva-dadesobertes-api, junta-andalucia-datos-abiertos, cnmc-data, renfe-datos-abiertos).

Trampas que resuelve:
- rows (package_search) y limit (datastore_search) se recortan sin aviso a 1000 y 32000 según el portal: se pagina
  avanzando tantas filas como llegan y hasta total, sin fiarse del limit pedido.
- _links.next llega sin host o sin el prefijo del portal (//api/3/..., /api/3/... sin /data o /datosabiertos/portal),
  y en la GVA sigue apareciendo tras la última página: no se usa.
- El datastore puede tener menos filas que el CSV (5.000 de 18.718 en el padrón de la Comunidad de Madrid):
  comparar() cuenta las dos.
- Los recursos subidos a la Junta de Andalucía apuntan a un host interno sin DNS: url_descarga() lo corrige.
- filters y q por campo van como JSON en la URL y fl como parámetro repetido; los errores llegan con success false y código 400, 403, 404 o 409.

Uso: python scripts/clientes/ckan.py                                  padrón de la Comunidad de Madrid: datastore y CSV
     python scripts/clientes/ckan.py PORTAL TEXTO                     busca conjuntos (PORTAL: clave de PORTALES o URL)
     python scripts/clientes/ckan.py PORTAL --recurso ID              total del datastore, primeras filas y fichero
"""
from __future__ import annotations

import csv
import io
import json as _json
import os
import sys
from typing import Iterator
from urllib.parse import urlparse, urlunparse

try:
    from .sesion import Bloqueado, contenido, json, sesion, texto
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    from sesion import Bloqueado, contenido, json, sesion, texto

PORTALES = {
    "comunidad-madrid": "https://datos.comunidad.madrid/api/3/action",
    "madrid": "https://datos.madrid.es/api/3/action",
    "barcelona": "https://opendata-ajuntament.barcelona.cat/data/api/3/action",
    "gva": "https://dadesobertes.gva.es/api/3/action",
    "andalucia": "https://www.juntadeandalucia.es/datosabiertos/portal/api/3/action",
    "cnmc": "https://catalogodatos.cnmc.es/api/3/action",
    "renfe": "https://data.renfe.com/api/3/action",
}
# Host interno que aparece en la url de los recursos subidos y su equivalente público
HOSTS_INTERNOS = {"gdc-pdpopendata-ckan.paas.junta-andalucia.es": "www.juntadeandalucia.es"}
_S = None


class ErrorCkan(RuntimeError):
    """La acción respondió success false (recurso inexistente, filtro mal formado, acción no disponible)."""


def _sesion():
    global _S
    if _S is None:
        _S = sesion()
    return _S


def base(portal: str) -> str:
    return PORTALES.get(portal, portal).rstrip("/")


def resultado(cuerpo: dict, accion: str = "") -> dict:
    """result de una respuesta CKAN; ErrorCkan con el mensaje si success es false."""
    if not isinstance(cuerpo, dict) or not cuerpo.get("success"):
        error = cuerpo.get("error") if isinstance(cuerpo, dict) else cuerpo
        raise ErrorCkan(f"{accion}: {error}")
    return cuerpo["result"]


def accion(portal: str, nombre: str, **params) -> dict | list:
    """Llama a /api/3/action/{nombre}. Los dict (filters, q por campo) van como JSON y las list se repiten
    (fl=name&fl=title): el CKAN 2.8 de Renfe rechaza fl separado por comas con «No es una lista»."""
    params = {k: (_json.dumps(v, ensure_ascii=False) if isinstance(v, dict) else v)
              for k, v in params.items() if v is not None}
    r = _sesion().get(f"{base(portal)}/{nombre}", params=params)
    try:
        cuerpo = json(r)
    except ValueError:
        raise ErrorCkan(f"{nombre}: HTTP {r.status_code} sin JSON ({r.headers.get('Content-Type')}); "
                        "la acción no existe en este portal o la URL base no es la de la API") from None
    return resultado(cuerpo, nombre)


def paginar(portal: str, nombre: str, clave: str, total: str, inicio: str, tam: str, por_pagina: int,
            params: dict) -> Iterator[dict]:
    """Avanza tantas filas como llegan (no las pedidas: el portal recorta sin aviso) hasta total o una página vacía."""
    pos = 0
    while True:
        res = accion(portal, nombre, **{**params, inicio: pos, tam: por_pagina})
        lote = res[clave]
        yield from lote
        pos += len(lote)
        if not lote or (res.get(total) is not None and pos >= res[total]):
            return


def buscar(portal: str, q: str = "*:*", fq: str | None = None, por_pagina: int = 1000, **params) -> Iterator[dict]:
    """Conjuntos de package_search (q y fq en sintaxis Solr: title:paro, organization:estadistica), todos."""
    return paginar(portal, "package_search", "results", "count", "start", "rows", por_pagina,
                   {"q": q, "fq": fq, **params})


def paquete(portal: str, nombre: str) -> dict:
    """package_show: el conjunto con sus resources (id, format, url, datastore_active)."""
    return accion(portal, "package_show", id=nombre)


def filas(portal: str, resource_id: str, filters: dict | None = None, por_pagina: int = 10000, sort: str = "_id",
          **params) -> Iterator[dict]:
    """Todas las filas de datastore_search con filtros; ordena por _id para que la paginación sea estable.
    Ojo: los campos pueden venir todos como texto (Ayuntamiento de Madrid) y los códigos sin ceros a la izquierda."""
    return paginar(portal, "datastore_search", "records", "total", "offset", "limit", por_pagina,
                   {"resource_id": resource_id, "filters": filters, "sort": sort, **params})


def total_datastore(portal: str, resource_id: str) -> int:
    """Filas en el datastore; si la versión de CKAN no da total (2.6 en Barcelona), COUNT(*) por SQL."""
    res = accion(portal, "datastore_search", resource_id=resource_id, limit=1)
    if res.get("total") is not None:
        return res["total"]
    sql = accion(portal, "datastore_search_sql", sql=f'SELECT COUNT(*) AS n FROM "{resource_id}"')
    return int(sql["records"][0]["n"])


def url_descarga(recurso: dict | str) -> str:
    """url del recurso con el host interno de la Junta de Andalucía cambiado por el público."""
    url = recurso if isinstance(recurso, str) else recurso["url"]
    p = urlparse(url)
    if p.hostname in HOSTS_INTERNOS:
        p = p._replace(netloc=HOSTS_INTERNOS[p.hostname])
    return urlunparse(p)


def descargar(recurso: dict | str) -> bytes:
    """Bytes del fichero original del recurso (lo que el datastore puede no tener entero)."""
    return contenido(_sesion().get(url_descarga(recurso)))


def contar_csv(datos: bytes | str) -> int:
    """Filas de datos de un CSV (sin cabecera), con separador detectado y codificación real."""
    t = datos if isinstance(datos, str) else texto(datos)
    muestra = t[:20000]
    sep = max(";,\t|", key=muestra.count)
    return max(sum(1 for fila in csv.reader(io.StringIO(t), delimiter=sep) if any(fila)) - 1, 0)


def comparar(portal: str, recurso: dict) -> dict:
    """Total del datastore frente a las filas del CSV original; completo es False si el datastore se queda corto."""
    datastore = total_datastore(portal, recurso["id"]) if recurso.get("datastore_active") else None
    fichero = contar_csv(descargar(recurso)) if str(recurso.get("format", "")).upper() == "CSV" else None
    return {"datastore": datastore, "fichero": fichero,
            "completo": None if None in (datastore, fichero) else datastore >= fichero}


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        if len(args) >= 3 and args[1] == "--recurso":
            portal, rid = args[0], args[2]
            print(rid, "total del datastore", total_datastore(portal, rid))
            for f in filas(portal, rid, por_pagina=3):
                print(" ", f)
                break
        elif len(args) >= 2:
            for i, p in enumerate(buscar(args[0], " ".join(args[1:]), fl=["name", "title"], por_pagina=100)):
                print(p["name"], "|", p["title"])
                if i >= 19:
                    break
        else:
            p = paquete("comunidad-madrid", "padron_por_sexo")
            csv_ = next(r for r in p["resources"] if r["format"].upper() == "CSV")
            c = comparar("comunidad-madrid", csv_)
            n = sum(1 for _ in filas("comunidad-madrid", csv_["id"], por_pagina=2000))
            print(p["title"], "| datastore", c["datastore"], "filas (leídas paginando:", n, ") | CSV", c["fichero"],
                  "filas |", "completo" if c["completo"] else "el datastore NO tiene todo: usar el CSV")
    except Bloqueado as e:
        sys.exit(f"bloqueado: {e}")
