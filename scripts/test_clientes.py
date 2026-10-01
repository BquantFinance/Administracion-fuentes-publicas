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
import bdns  # noqa: E402
import boe  # noqa: E402
import datacomex  # noqa: E402
import ine_tempus  # noqa: E402
import placsp  # noqa: E402
import saiku  # noqa: E402


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
