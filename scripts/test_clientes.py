#!/usr/bin/env python3
"""Prueba los parsers de scripts/clientes/ contra las respuestas reales recortadas de scripts/clientes/muestras/, sin red.

Uso: python scripts/test_clientes.py   (código 1 si algo falla; corre en CI)
Cualquier intento de petición HTTP durante la prueba es un fallo: los parsers no deben tocar la red.
"""
from __future__ import annotations

import json
import sys
import traceback
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

import requests

DIR = Path(__file__).resolve().parent / "clientes"
M = DIR / "muestras"
sys.path.insert(0, str(DIR))

import aemet  # noqa: E402
import arcgis  # noqa: E402
import bdns  # noqa: E402
import boe  # noqa: E402
import ckan  # noqa: E402
import datacomex  # noqa: E402
import ine_tempus  # noqa: E402
import ogc  # noqa: E402
import pcaxis  # noqa: E402
import placsp  # noqa: E402
import saiku  # noqa: E402
import sesion  # noqa: E402
import socrata  # noqa: E402


def _sin_red(*a, **k):
    raise AssertionError("petición HTTP durante una prueba sin red")


requests.Session.request = _sin_red
TESTS = []


def test(f):
    TESTS.append(f)
    return f


def js(nombre):
    return json.loads((M / nombre).read_text(encoding="utf-8"))


def xml(nombre):
    return ET.parse(M / nombre).getroot()


def _contar_items(nodo) -> int:
    """Cuenta los item del sumario sin el recorrido del cargador, para contrastar."""
    if isinstance(nodo, list):
        return sum(_contar_items(x) for x in nodo)
    if not isinstance(nodo, dict):
        return 0
    return sum((len(v) if isinstance(v, list) else 1) if k == "item" else _contar_items(v) for k, v in nodo.items())


@test
def boe_sumario_extraordinario_y_texto():
    s = js("boe-sumario-20260930.json")["data"]["sumario"]
    its = list(boe.items(s))
    assert len(its) == _contar_items(s) == 9, len(its)
    ext = its[0]  # número extraordinario: seccion.texto.departamento.texto.epigrafe
    assert (ext["diario_numero"], ext["seccion_codigo"], ext["departamento_nombre"]) == ("242", "3", "PRESIDENCIA DEL GOBIERNO"), ext
    assert ext["epigrafe_nombre"].startswith("Situación de interés") and ext["fecha"] == "20260930"
    c5 = [i for i in its if i["seccion_codigo"] == "5C"]
    assert c5 and all(i["departamento_nombre"] == "ANUNCIOS PARTICULARES" and "epigrafe_nombre" not in i for i in c5)
    assert all(i["url_pdf"].endswith(".pdf") and isinstance(i["pdf_bytes"], int) for i in its)


@test
def boe_sumario_seccion_4_y_objeto_o_lista():
    s = js("boe-sumario-20240102.json")["data"]["sumario"]
    its = list(boe.items(s))
    assert len(its) == _contar_items(s), len(its)
    s4 = [i for i in its if i["seccion_codigo"] == "4"]
    assert s4 and s4[0]["departamento_nombre"].startswith("JUZGADOS") and s4[0]["identificador"].startswith("BOE-B-2024-")
    assert any(i["identificador"] == "BOE-A-2024-87" and i["control"] == "2023/26904" for i in its)


@test
def boe_errores_en_xml():
    assert boe.error_api((M / "boe-error-404.xml").read_bytes()) == "404 La información solicitada no existe"
    assert xml("boe-documento-error.xml").tag == "error"  # xml.php con id inexistente: HTTP 200


@test
def boe_documento():
    d = boe.parse_documento(xml("boe-documento-BOE-A-2026-20264.xml"))
    assert (d["identificador"], d["rango"], d["rango_codigo"], d["departamento_codigo"]) == ("BOE-A-2026-20264", "Real Decreto-ley", "1320", "7723")
    assert d["url_epub"].startswith("https://www.boe.es/diario_boe/epub.php") and d["fecha_vigencia"] == "20261001"
    assert "Subvenciones" in d["materias"] and d["anteriores"][0]["id"] == "BOE-A-2003-23186" and d["anteriores"][0]["relacion_codigo"] == "440"
    assert d["texto"].startswith("I\n") and len(d["texto"].splitlines()) == 3


@test
def boe_consolidada_bloque_y_vigencia():
    versiones = boe.parse_bloque(xml("boe-lc-bloque-a135.xml"))
    assert [v["id_norma"] for v in versiones] == ["BOE-A-1978-31229", "BOE-A-2011-15210"]
    assert boe.version_vigente(versiones, date(2026, 10, 1))["id_norma"] == "BOE-A-2011-15210"
    assert boe.version_vigente(versiones, "20000101")["id_norma"] == "BOE-A-1978-31229"
    assert boe.version_vigente(versiones, "19000101") is None
    assert "estabilidad presupuestaria" in versiones[1]["texto"]
    assert js("boe-lc-vacio.json")["data"] == ""  # sin resultados data es cadena vacía, no lista
    assert js("boe-lc-metadatos.json")["data"][0]["url_eli"] == "https://www.boe.es/eli/es/c/1978/12/27/(1)"


@test
def borme_sumario_y_empresas():
    its = list(boe.items(js("borme-sumario-20260930.json")["data"]["sumario"]))
    assert any(i["identificador"].endswith("-99") for i in its)  # índice alfabético del día, no una provincia
    assert any(i["seccion_codigo"] == "C" and i.get("apartado_nombre") for i in its)
    emp = boe.parse_borme_a(xml("borme-A-2026-189-28.xml"))
    assert len(emp) == 6 and all(e["datos_registrales"].startswith("S 8") for e in emp)
    mamey = next(e for e in emp if e["denominacion"] == "MA5 MAMEY SL")
    assert [a["tipo"] for a in mamey["actos"]] == ["Constitución", "Nombramientos"] and "Capital: 3.000,00 Euros" in mamey["actos"][0]["texto"]
    assert any(e["denominacion"] == "CALLE MUNTANER 210 S.L." for e in emp)  # el punto de S.L. no se quita
    assert any(a["tipo"] == "Fe de erratas" for e in emp for a in e["actos"])


@test
def bdns_fechas_y_ventanas():
    assert bdns.fecha_bdns(date(2026, 9, 1)) == bdns.fecha_bdns("2026-09-01") == bdns.fecha_bdns("01/09/2026") == "01/09/2026"
    v = list(bdns.ventanas("2026-01-01", "2026-03-15"))
    assert v[0][0] == "01/01/2026" and v[-1][1] == "15/03/2026" and len(v) == 3
    assert js("bdns-error-400.json")["codigo"] == "ERR_VALIDACION"


@test
def bdns_beneficiario():
    filas = js("bdns-concesiones-busqueda.json")["content"] + js("bdns-ayudasestado-busqueda.json")["content"]
    pares = [bdns.separar_beneficiario(f["beneficiario"]) for f in filas]
    assert all(nif and nombre and not nombre.startswith("-") for nif, nombre in pares), pares
    assert any("*" in nif for nif, _ in pares)  # persona física con DNI enmascarado
    assert bdns.separar_beneficiario("A02066116 - BODEGAS PIQUERAS SA") == ("A02066116", "BODEGAS PIQUERAS SA")
    assert {f["nivel1"] for f in js("bdns-convocatorias-busqueda.json")["content"]} <= {"ESTADO", "AUTONOMICA", "LOCAL", "OTROS"}


@test
def bdns_csv_windows_1252():
    filas = bdns.leer_csv((M / "bdns-concesiones-exportar.csv").read_bytes())
    assert len(filas) == 3 and "Código BDNS" in filas[0] and filas[0]["Administración"] == "AUTONOMICA"
    assert all(float(f["Importe"]) > 0 for f in filas)


@test
def aemet_respuesta_intermedia():
    for status, cuerpo, exc in ((401, (M / "aemet-error-401.json").read_bytes(), RuntimeError), (200, b"", PermissionError)):
        try:
            aemet.url_datos(status, cuerpo)
        except exc:
            pass
        else:
            raise AssertionError(f"AEMET {status} no lanzó {exc.__name__}")


@test
def ine_ids_y_tablas():
    ids = ine_tempus.mapa_ids(js("ine-valores-variable-19-22.json"))
    assert ids["02001"] == 6124 and ids["28079"] == 2813
    tabla = ine_tempus.limpiar_tabla(js("ine-datos-tabla-29005.json"), 29005)
    assert ine_tempus.ultimo_valor(tabla[0]) == ("2025-01-01", 753.0)  # Data llega del más reciente al más antiguo
    try:
        ine_tempus.limpiar_tabla(js("ine-error-volumen.json"), 30824)
    except RuntimeError as e:
        assert "restricciones de volumen" in str(e)
    else:
        raise AssertionError("la tabla sin filtros no lanzó error")


@test
def datacomex_codigos_y_numeros():
    paises = {p["Id"]: p["Pais"] for p in js("datacomex-paises.json")}
    assert paises["003"] == "Países Bajos" and "3" not in paises  # código de 3 dígitos con ceros
    assert datacomex.numero("29164,8") == datacomex.numero("29.164,8") == 29164.8
    assert datacomex.limpiar_token('"token:abc.def.ghi"') == "abc.def.ghi"
    assert "denegado" in js("datacomex-error-401.json")["Message"]


@test
def saiku_cellset():
    filas = saiku.filas(js("saiku-flattened.json"))
    assert filas[0] == ["Año", "Llamadas pertinentes"] and ["2024", "106196"] in filas


@test
def placsp_feed_y_anulaciones():
    entradas, siguiente = placsp.parse_feed((M / "placsp-feed-643.atom").read_bytes())
    assert siguiente and siguiente.endswith(".atom") and "_2026" in siguiente
    anuladas = [e for e in entradas if e.get("deleted")]
    assert len(anuladas) == 1 and anuladas[0]["motivo"] == "ANULADA"
    vivas = [e for e in entradas if not e.get("deleted")]
    assert len(vivas) == 2 and all(e["expediente"] and e["organo"] and e["cpv"] for e in vivas)
    obra = next(e for e in vivas if e["cpv"][0].startswith("45"))
    assert obra["importe_sin_iva"] == "98030.3" and obra["organo_dir3"]
    fechas = [e["updated"] for e in entradas]
    assert fechas == sorted(fechas, reverse=True)


def respuesta(cuerpo: bytes, tipo: str = "application/json", estado: int = 200, url: str = "https://x.gob.es/a"):
    r = requests.Response()
    r.status_code, r._content, r.url = estado, cuerpo, url
    r.headers["Content-Type"] = tipo
    return r


@test
def sesion_texto_bloqueos_y_gzip():
    import gzip
    csv_ = (M / "pcaxis-ine-24077.csv").read_bytes()
    r = respuesta(csv_, "text/plain;charset=ISO-8859-15")
    r.encoding = "ISO-8859-15"
    assert sesion.texto(r).startswith("Grupos COICOP 2011;") and "Índice general" in sesion.texto(r)  # BOM fuera, UTF-8
    assert "Año;" in sesion.texto((M / "ckan-comunidad-madrid-padron.csv").read_bytes())  # Latin-1 real
    assert sesion.contenido(respuesta(gzip.compress(b"[1]"))) == b"[1]"  # gzip sin Content-Encoding
    assert sesion.contenido(respuesta(gzip.compress(b"x"), url="https://x.es/f.csv.gz")).startswith(b"\x1f\x8b")
    assert sesion.json(respuesta(b'\xef\xbb\xbf{"a": 1}')) == {"a": 1}
    try:
        sesion.json(respuesta(b"<html>Error</html>", "text/html"))
    except ValueError as e:
        assert "no es JSON" in str(e)
    else:
        raise AssertionError("HTML con 200 tomado por JSON")
    assert sesion.bloqueo(respuesta(b'<script src="/_Incapsula_Resource?x">', "text/html")) == (
        sesion.BLOQUEOS[0][1], False)
    assert sesion.bloqueo(respuesta("<h1>Acceso denegado</h1>".encode(), "text/html", 403))[1] is True
    assert sesion.bloqueo(respuesta("<p>Acceso denegado a la sede</p>".encode(), "text/html", 200)) is None
    assert sesion.bloqueo(respuesta(b'{"x": "Access Denied"}', "application/json", 403)) is None


@test
def ckan_errores_y_tope_silencioso():
    for nombre, tipo in (("ckan-error-404.json", "Not Found Error"), ("ckan-renfe-fl-409.json", "Validation Error")):
        try:
            ckan.resultado(js(nombre), "x")
        except ckan.ErrorCkan as e:
            assert tipo in str(e)
        else:
            raise AssertionError(nombre)
    res = ckan.resultado(js("ckan-cnmc-datastore-tope.json"))
    assert res["limit"] == 32000 and res["total"] == 75553 and res["_links"]["next"].startswith("//api/3/")
    # paginar con un portal falso que recorta a 3 filas lo que se pida: hay que llegar a total sin perder filas
    datos = list(range(10))
    original = ckan.accion

    def falso(portal, nombre, **params):
        lote = datos[params["offset"]:params["offset"] + min(params["limit"], 3)]
        return {"records": [{"_id": i} for i in lote], "total": len(datos)}
    ckan.accion = falso
    try:
        assert [f["_id"] for f in ckan.filas("x", "r", por_pagina=50)] == datos
    finally:
        ckan.accion = original


@test
def ckan_host_interno_y_csv():
    r = js("ckan-andalucia-package-show.json")["result"]["resources"][0]
    assert "gdc-pdpopendata" in r["url"] and ckan.url_descarga(r).startswith("https://www.juntadeandalucia.es/datosabiertos/portal/")
    assert ckan.contar_csv((M / "ckan-comunidad-madrid-padron.csv").read_bytes()) == 3  # Latin-1, ; y CRLF


@test
def socrata_tipos_y_errores():
    m = js("socrata-gn9e-3qhr.json")
    filas = socrata.tipar(m["body"], dict(zip(m["x-soda2-fields"], m["x-soda2-types"])))
    assert filas[0]["nivell_absolut"] == 210.93 and isinstance(filas[0]["dia"], str)
    assert socrata.tipar([{"n": "90751"}], {"n": "number"})[0]["n"] == 90751
    assert socrata._soql({"where": "a=1", "limit": 5, "estaci": "x"}) == {"$where": "a=1", "$limit": 5, "estaci": "x"}
    assert js("socrata-error-404.json")["code"] == "dataset.missing"


@test
def pcaxis_urls_numeros_y_csv():
    ed = "https://estadisticas.educacion.gob.es/EducaJaxiPx"
    assert pcaxis.url_csv(24077) == "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/24077.csv?nocab=1"
    assert pcaxis.url_csv("https://www.ine.es/jaxiT3/Tabla.htm?t=24077&L=0") == pcaxis.url_csv("24077")
    assert pcaxis.url_csv(f"{ed}/Tabla.htm?path=/no-universitaria/adultos/l0/&amp;file=adul_01.px&amp;L=0") == (
        f"{ed}/files/_px/es/csv_bdsc/no-universitaria/adultos/l0/adul_01.px?nocab=1")
    assert pcaxis.url_csv("https://www.ine.es/jaxi/Tabla.htm?path=/t20/e245/p08/l0/&file=01002.px") == (
        "https://www.ine.es/jaxi/files/_px/es/csv_bdsc/t20/e245/p08/l0/01002.px?nocab=1")
    assert pcaxis.url_csv(pcaxis.url_csv(24077), "px").endswith("/px/24077.px?nocab=1")
    assert pcaxis.numero("197.079") == 197079 and pcaxis.numero("926,6") == 926.6 and pcaxis.numero("..") is None
    assert pcaxis.periodo_iso("2026M09") == "2026-09" and pcaxis.periodo_iso("2025T3") == "2025-Q3"
    ine = pcaxis.leer((M / "pcaxis-ine-24077.csv").read_bytes())
    assert ine[0]["Total"] is None and ine[1]["Total"] == 104.638 and ine[0]["Grupos COICOP 2011"] == "Índice general"
    cul = pcaxis.leer((M / "pcaxis-cultura-T1FM1001.csv").read_bytes())
    assert cul[0]["Total"] == 926.6 and cul[0]["periodo"].startswith("De 2025-3T")


@test
def arcgis_oid_fechas_y_error_200():
    info = js("arcgis-igme-capa.json")
    assert info["objectIdField"] is None and arcgis.campo_oid(info) == "FID"
    assert info["advancedQueryCapabilities"]["supportsPagination"] is False
    assert js("arcgis-igme-sin-paginacion.json")["error"]["message"] == "Pagination is not supported."
    c = js("arcgis-cobertura-28079.json")
    a = arcgis.fechas_iso(dict(c["features"][0]["attributes"]), c)
    assert a["cod_munici"] == "28079" and a["fecha"].startswith("2025-06-30")


@test
def ogc_next_y_tope():
    p = js("ogc-sigpac-recintos-tope.json")
    nxt = ogc.siguiente(p)
    assert p["numberReturned"] == 250 and "limit=250" in nxt and "offset=250" in nxt  # se pidió limit=1000
    paginas = {"u0": {"features": [1, 2], "links": [{"rel": "next", "href": "u1"}]},
               "u1": {"features": [3], "links": [{"rel": "next", "href": "u1"}]}}  # next repetido: parar
    original = ogc.json
    ogc._S = type("S", (), {"get": lambda self, url, params=None: url})()
    ogc.json = paginas.__getitem__
    try:
        assert list(ogc.entidades("u0")) == [1, 2, 3]
    finally:
        ogc.json, ogc._S = original, None


def main() -> int:
    fallos = 0
    for t in TESTS:
        try:
            t()
            print(f"ok    {t.__name__}")
        except Exception:  # noqa: BLE001
            fallos += 1
            print(f"FALLO {t.__name__}\n{traceback.format_exc()}")
    print(f"{len(TESTS) - fallos}/{len(TESTS)} pruebas sin red correctas")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
