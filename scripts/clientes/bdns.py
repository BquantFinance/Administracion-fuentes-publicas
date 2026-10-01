"""BDNS: Accept JSON, fechas dd/mm/aaaa, páginas de Spring con tope de 10000 y exportación paginada (ficha bdns-api).

Uso: python scripts/clientes/bdns.py [NIF]
"""
from __future__ import annotations

import csv
import io
import os
import re
import sys
from datetime import date, datetime, timedelta
from typing import Iterator

try:
    from ._http import session
except ImportError:  # ejecutado por ruta
    sys.path.insert(0, os.path.dirname(__file__))
    from _http import session

BASE = "https://www.infosubvenciones.es/bdnstrans/api"
TOPE = 10000  # pageSize mayor se recorta a 10000 sin aviso, también al exportar
COLECCIONES = ("convocatorias", "concesiones", "ayudasestado", "minimis", "grandesbeneficiarios", "sanciones", "planesestrategicos", "partidospoliticos")


def fecha_bdns(f) -> str:
    """Los filtros de fecha van en dd/mm/aaaa; en ISO la API responde 400 ERR_VALIDACION."""
    if isinstance(f, str) and re.fullmatch(r"\d{2}/\d{2}/\d{4}", f):
        return f
    d = f if isinstance(f, date) else datetime.strptime(str(f)[:10], "%Y-%m-%d").date()
    return d.strftime("%d/%m/%Y")


def _params(filtros: dict) -> dict:
    fechas = ("fechaDesde", "fechaHasta", "fechaRegInicio", "fechaRegFin")
    return {k: fecha_bdns(v) if k in fechas else v for k, v in filtros.items() if v is not None}


def _get(ruta: str, params: dict):
    """Accept application/json explícito: con el de un navegador responde XML (raíz ObjectNode)."""
    s = session(accept="application/json")
    r = s.get(f"{BASE}/{ruta}", params=params, timeout=180, verify=s.verify)
    if r.status_code != 200:  # 400 con JSON {codigo, errores}; 404 con HTML de Tomcat
        detalle = r.json().get("errores") if r.headers.get("Content-Type", "").startswith("application/json") else r.text[:80]
        raise RuntimeError(f"BDNS {r.status_code} en {ruta}: {detalle}")
    return r


def pagina(coleccion: str, page: int = 0, page_size: int = 1000, **filtros) -> dict:
    """Una página: {content, totalElements, totalPages, number, last, advertencia}. Filtros habituales: fechaDesde,
    fechaHasta, numeroConvocatoria, nifCif (concesiones, minimis, ayudasestado), beneficiario (idPersona, no NIF),
    tipoAdministracion (C estatal), descripcion, order, direccion."""
    return _get(f"{coleccion}/busqueda", dict(_params(filtros), page=page, pageSize=min(page_size, TOPE))).json()


def buscar(coleccion: str, page_size: int = TOPE, **filtros) -> Iterator[dict]:
    """Recorre todas las páginas. Para volúmenes grandes, trocear por fechas con ventanas() y mirar totalElements antes."""
    n = 0
    while True:
        o = pagina(coleccion, n, page_size, **filtros)
        yield from o["content"]
        if o.get("last", True) or not o["content"]:
            return
        n += 1


def convocatoria(numero: str | int) -> dict:
    """Detalle por número BDNS (codigoBDNS): órgano, instrumentos, presupuestoTotal, bases, documentos, regiones."""
    return _get("convocatorias", {"numConv": numero}).json()


def separar_beneficiario(texto: str | None) -> tuple[str | None, str | None]:
    """El campo beneficiario lleva NIF y nombre juntos: 'B13284336 NOMBRE' en concesiones y minimis, 'A02066116 - NOMBRE'
    en ayudasestado. Las personas físicas llevan el DNI enmascarado (***0456**, ****7918*, ***0647)."""
    if not texto:
        return None, None
    nif, _, nombre = texto.strip().partition(" ")
    return nif, nombre.removeprefix("- ").strip() or None


def exportar(coleccion: str, tipo: str = "csv", page: int = 0, page_size: int = TOPE, **filtros) -> list[dict] | bytes:
    """Exportación con los filtros de la búsqueda. Pagina igual: sin pageSize devuelve 50 filas sin aviso, con tope de
    10000. Exige vpd (GE, portal general). El CSV llega en windows-1252, separado por comas; xlsx se devuelve en bytes."""
    r = _get(f"{coleccion}/exportar", dict(_params(filtros), vpd="GE", tipoDoc=tipo, page=page, pageSize=min(page_size, TOPE)))
    return leer_csv(r.content) if tipo == "csv" else r.content


def leer_csv(contenido: bytes) -> list[dict]:
    """Columnas con nombre en castellano (Código BDNS, Beneficiario, Importe...); fechas dd/mm/aaaa y punto decimal."""
    return list(csv.DictReader(io.StringIO(contenido.decode("cp1252"))))


def altas(desde, hasta=None, coleccion: str = "concesiones") -> Iterator[dict]:
    """Lo dado de alta entre desde y hasta, ambos incluidos (por defecto un solo día), sea cual sea su fecha de
    concesión: la vía para sincronizar. fechaRegInicio y fechaRegFin no están documentados y el fin es exclusivo
    (29/09 a 29/09 da 0; 29/09 a 30/09, lo del 29). Vale en concesiones, minimis y ayudasestado; convocatorias lo ignora.
    Filtrar por fechaDesde y fechaHasta pierde las tardías: las concesiones del 15/01/2025 se dieron de alta hasta agosto
    de 2026."""
    d = desde if isinstance(desde, date) else datetime.strptime(fecha_bdns(desde), "%d/%m/%Y").date()
    h = d if hasta is None else hasta if isinstance(hasta, date) else datetime.strptime(fecha_bdns(hasta), "%d/%m/%Y").date()
    yield from buscar(coleccion, fechaRegInicio=d, fechaRegFin=h + timedelta(days=1))


def ventanas(desde, hasta, dias: int = 31) -> Iterator[tuple[str, str]]:
    """Ventanas de fechas (dd/mm/aaaa) para trocear descargas que superan las 10000 filas por petición."""
    d = desde if isinstance(desde, date) else datetime.strptime(fecha_bdns(desde), "%d/%m/%Y").date()
    fin = hasta if isinstance(hasta, date) else datetime.strptime(fecha_bdns(hasta), "%d/%m/%Y").date()
    while d <= fin:
        h = min(d + timedelta(days=dias - 1), fin)
        yield fecha_bdns(d), fecha_bdns(h)
        d = h + timedelta(days=1)


if __name__ == "__main__":
    nif = sys.argv[1] if len(sys.argv) > 1 else "Q1132001G"
    o = pagina("concesiones", 0, 5, nifCif=nif)
    print(nif, o["totalElements"], "concesiones; las más recientes:")
    for c in o["content"]:
        print(" ", c["fechaConcesion"], c["numeroConvocatoria"], separar_beneficiario(c["beneficiario"])[1], c["importe"], c["nivel1"])
    ayer = date.today() - timedelta(days=1)
    total = pagina("convocatorias", 0, 1, fechaDesde=ayer, fechaHasta=ayer)["totalElements"]
    filas = exportar("concesiones", fechaDesde=ayer, fechaHasta=ayer)
    print(ayer, total, "convocatorias registradas;", len(filas), "concesiones exportadas en CSV")
    nuevas = sum(1 for _ in altas(ayer, coleccion="minimis"))
    print(ayer, nuevas, "minimis dadas de alta (cualquier fecha de concesión)")
