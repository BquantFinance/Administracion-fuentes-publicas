#!/usr/bin/env python3
"""Prueba los parsers de scripts/clientes/ contra las respuestas reales recortadas de scripts/clientes/muestras/, sin red.

Uso: python scripts/test_clientes.py   (código 1 si algo falla; corre en CI)
Cualquier intento de petición HTTP durante la prueba es un fallo: los parsers no deben tocar la red.
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import traceback
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

import requests

DIR = Path(__file__).resolve().parent / "clientes"
M = DIR / "muestras"
sys.path.insert(0, str(DIR))

import aemet  # noqa: E402
import almacen  # noqa: E402
import arcgis  # noqa: E402
import bdns  # noqa: E402
import boe  # noqa: E402
import cerca  # noqa: E402
import ckan  # noqa: E402
import consulta  # noqa: E402
import datacomex  # noqa: E402
import ine_tempus  # noqa: E402
import mivau  # noqa: E402
import ogc  # noqa: E402
import pcaxis  # noqa: E402
import placsp  # noqa: E402
import radar  # noqa: E402
import saiku  # noqa: E402
import sepe  # noqa: E402
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
    try:
        placsp.parse_feed(b"<html><title>Error</title><body>The Web Application Firewall has denied</body></html>")
    except ValueError as e:
        assert "no devolvió un feed" in str(e)
    else:
        raise AssertionError("página del WAF tomada por un feed vacío")
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


@test
def placsp_adjudicaciones_y_organo():
    entradas, _ = placsp.parse_feed((M / "placsp-feed-643.atom").read_bytes())
    obra = next(e for e in entradas if not e.get("deleted") and e["cpv"][0].startswith("45"))
    assert obra["organo_nif"] == "P2807900B" and obra["organo_dir3"] == "LA0000765" and obra["valor_estimado"] == "98030.3"
    otras, _ = placsp.parse_feed((M / "placsp-sin-dir3-y-prorroga.atom").read_bytes())
    sin = next(e for e in otras if e["id"].endswith("20611333"))
    assert sin["organo_dir3"] is None and sin["organo_nif"] == "A81778243"  # antes devolvía el NIF como DIR3
    pro = next(e for e in otras if e["modificaciones"])
    assert pro["modificaciones"][0]["contrato"] == "2025-11" and pro["modificaciones"][0]["importe_final_sin_iva"] == "222791.62"
    con_contrato = [a for e in entradas for a in e.get("adjudicaciones", []) if a.get("contrato")]
    assert con_contrato and con_contrato[0]["contrato"] == "104/2026/01231_CB4_AM2938 L2" and con_contrato[0]["fecha_contrato"] == "2026-09-30"
    adj = obra["adjudicaciones"][0]
    assert adj["nif"] == "A27178789" and adj["importe_total"] == "118616.66" and adj["fecha_adjudicacion"] == "2026-09-30"
    assert placsp.nif_normal(" b-12.345.678 ") == "B12345678"
    assert placsp.es_persona_fisica("***1234**") and placsp.es_persona_fisica("X1234567L") and not placsp.es_persona_fisica("B12345678")



@test
def bdns_mantenimiento_con_200_no_es_pagina_vacia():
    # 2026-10-05: ayudasestado de un día respondió 200 con {codigo, error} y sin content tras 60 s
    respuestas = [{"codigo": "ERR_MANTENIMIENTO_BBDD", "error": "Aplicación en Mantenimiento."},
                  {"content": [{"id": 1}], "last": True}]

    class R:
        def __init__(self, d):
            self.d = d

        def json(self):
            return self.d
    viejo_get, viejo_sleep = bdns._get, bdns.time.sleep
    bdns._get, bdns.time.sleep = (lambda ruta, params: R(respuestas.pop(0))), (lambda s: None)
    try:
        assert list(bdns.buscar("ayudasestado", fechaRegInicio="01/10/2026")) == [{"id": 1}]  # reintenta
        respuestas[:] = [{"codigo": "OTRO", "error": "x"}]
        try:
            list(bdns.buscar("concesiones"))
            raise AssertionError("no lanzó")
        except RuntimeError as exc:
            assert "OTRO" in str(exc)
    finally:
        bdns._get, bdns.time.sleep = viejo_get, viejo_sleep


@test
def placsp_fecha_de_publicacion_es_la_del_anuncio_de_licitacion():
    # Entrada real del 643 (2026-10-01): DOC_CAN_ADJ del 01/10 delante del DOC_CN del 18/08
    entradas, _ = placsp.parse_feed((M / "placsp-entry-dos-anuncios.atom").read_bytes())
    e = [x for x in entradas if not x.get("deleted")][0]
    assert e["fecha_publicacion"] == "2026-08-18", e["fecha_publicacion"]
    e2 = [x for x in placsp.parse_feed((M / "placsp-feed-643.atom").read_bytes())[0] if not x.get("deleted")]
    assert all(x["fecha_publicacion"] is None for x in e2)  # solo traen DOC_CAN_ADJ: sin anuncio de licitación en el feed

@test
def almacen_filas_sin_datos_personales():
    entradas, _ = placsp.parse_feed((M / "placsp-feed-643.atom").read_bytes())
    t = almacen.filas_placsp(entradas, "643")
    assert all(f["updated"] and "+" not in f["updated"] for f in t["placsp"])  # UTC sin zona
    assert any(a["nif"] == "A27178789" and a["importe_sin_iva"] == 98030.3 for a in t["placsp_adjudicaciones"])
    f = almacen.fila_bdns({"idConcesion": 1, "beneficiario": "***5550** NOMBRE APELLIDO", "fechaRegistro": "2026-09-29",
                           "ayudaEquivalente": 7200, "idPersona": 5}, "minimis")
    assert f["persona_fisica"] and f["nif"] is None and f["beneficiario"] is None and f["id_persona"] is None
    assert f["fecha_alta"] == "2026-09-29" and f["ayuda_equivalente"] == 7200.0
    emp = boe.parse_borme_a(xml("borme-A-2026-189-28.xml"))
    filas = [almacen.fila_borme(e, "2026-09-30", "BORME-A-2026-189-28", "MADRID") for e in emp]
    con_nombres = [a["texto"] for e in emp for a in e["actos"] if a["tipo"] not in almacen.ACTOS_CON_TEXTO and a["texto"]]
    assert con_nombres and not any(x in (f["detalle"] or "") for x in con_nombres for f in filas)
    assert all(f["actos"] for f in filas)


@test
def almacen_volcado_y_solo_lectura():
    try:
        import duckdb  # noqa: F401
    except ImportError:
        print("      (sin duckdb: se omite)")
        return
    with tempfile.TemporaryDirectory() as d:
        alm = almacen.Almacen(d)
        alm.añadir({"boe": [{"fecha": "2026-09-30", "identificador": "BOE-A-2026-1", "titulo": "viejo"}]})
        alm.volcar()
        alm.añadir({"boe": [{"fecha": "2026-09-30", "identificador": "BOE-A-2026-1", "titulo": "nuevo"},
                            {"fecha": "2026-10-01", "identificador": "BOE-A-2026-2", "titulo": "x"}]})
        alm.volcar()
        r = almacen.sql("select identificador, titulo from boe order by 1", d)
        assert r["filas"] == [["BOE-A-2026-1", "nuevo"], ["BOE-A-2026-2", "x"]]
        assert sorted(p.name for p in Path(d, "boe").glob("*.parquet")) == ["2026-09.parquet", "2026-10.parquet"]
        try:
            almacen.sql("select * from read_csv('/etc/passwd')", d)
            raise AssertionError("leyó fuera del almacén")
        except duckdb.Error as exc:
            assert "disabled" in str(exc)
    with tempfile.TemporaryDirectory() as d:  # almacén de la versión 1: relee PLACSP y la cobertura avisa mientras tanto
        Path(d, "placsp").mkdir()
        Path(d, "estado.json").write_text(json.dumps({"version": 1, "placsp": {"paginas": {"643": ["u1"]}, "zips": ["643_202609"]}}))
        with contextlib.redirect_stderr(io.StringIO()):
            alm = almacen.Almacen(d)
        assert alm.estado["version"] == 2 and "paginas" not in alm.estado["placsp"]
        assert alm.estado["placsp"]["zips_por_releer"] == ["643_202609"] and "zips" not in alm.estado["placsp"]
        alm.añadir({"placsp": [{"feed": "643", "id": "X", "updated": "2026-09-30 10:00:00", "borrado": False}]})
        alm.volcar()
        alm.guardar_estado()
        assert almacen.cobertura(d)["placsp"]["aviso"] == almacen.AVISO_V1
    assert almacen.Almacen(tempfile.mkdtemp()).estado == {"version": 2}  # uno nuevo nace en la 2, sin aviso
    with tempfile.TemporaryDirectory() as d:  # solo BDNS, sin PLACSP: la vista empresas rompía toda consulta (tanda 6)
        alm = almacen.Almacen(d)
        alm.añadir({"bdns": [almacen.fila_bdns({"idConcesion": 7, "beneficiario": "B12345678 EJEMPLO SL", "importe": 100,
                                                "fechaConcesion": "2026-09-28", "fechaRegistro": "2026-09-29"}, "concesiones")]})
        alm.volcar()
        assert almacen.sql("select count(*) from bdns", d)["filas"] == [[1]]
        alm.añadir({"placsp": [  # A con dos versiones y anulada después; B vigente
            {"feed": "643", "id": "A", "updated": "2026-10-01 10:00:00", "borrado": False, "estado": "PUB", "importe_sin_iva": 100.0},
            {"feed": "643", "id": "A", "updated": "2026-10-01 12:00:00", "borrado": False, "estado": "PUB", "importe_sin_iva": 110.0},
            {"feed": "643", "id": "A", "updated": "2026-10-02 09:00:00", "borrado": True, "motivo": "ANULADA"},
            {"feed": "643", "id": "B", "updated": "2026-10-01 11:00:00", "borrado": False, "estado": "PUB", "importe_sin_iva": 50.0}]})
        alm.volcar()
        u = almacen.sql("select id, importe_sin_iva, anulada, motivo_baja from placsp_ultimo order by id", d)["filas"]
        p = almacen.sql("select count(*) from placsp", d)["pista"]  # séptima tanda: los tres feeds juntos y las versiones
        assert "feed '643'" in p and "una fila por versión" in p
        assert "pista" not in almacen.sql("select count(*) from placsp_ultimo where feed = '643'", d)
        assert u == [["A", 110.0, True, "ANULADA"], ["B", 50.0, False, None]], u
        r = almacen.sql("select * from range(5);", d, 3)  # truncado con el total, y no truncado si caben justas
        assert r["truncado"] and r["filas_totales"] == 5 and len(r["filas"]) == 3
        assert not almacen.sql("select * from range(3)", d, 3)["truncado"]
        assert almacen.sql("select nif, nombre, ayudas from empresas", d)["filas"] == [["B12345678", "EJEMPLO SL", 1]]


@test
def sepe_csv_secreto_y_fusiones():
    filas = sepe.leer((M / "sepe-paro-municipios-2026.csv").read_bytes())  # windows-1252 con línea de título
    alcala = sepe.municipio("28005", datos=filas)
    assert [f["mes"] for f in alcala] == ["2026-07", "2026-08"] and alcala[-1]["total_paro_registrado"] == 9107
    assert alcala[-1]["municipio"] == "Alcalá de Henares" and "paro_hombre_edad_menor_25" in alcala[-1]
    abengibre = sepe.municipio("02001", datos=filas)[-1]
    assert None in abengibre.values()  # «<5» es secreto, no cero
    assert sepe.municipio("15902", datos=filas)[-1]["total_paro_registrado"] == 141  # 46 + 95, no el 0 de 15902
    assert sepe.municipio("36902", datos=filas)[-1]["total_paro_registrado"] == 169  # sin fila propia: 35 + 134


@test
def coyuntura_avance_y_periodos():
    u = consulta.ine_ultimo(js("ine-datos-serie-IPC290750.json"))
    assert u == {"periodo": "2026-09", "valor": 4.9, "tipo": "avance"}, u  # el último mes del IPC es avance
    assert consulta.bde_periodo("2026-04-01T08:15:00Z", "Q") == "2026T2"
    assert consulta.bde_periodo("2026-09-01T08:15:00Z", "M") == "2026-09"
    assert consulta.bde_periodo("2026-09-30T08:15:00Z", "D") == "2026-09-30"


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
    waf = b"<html><title>Error</title><body>The Web Application Firewall has denied your transaction due to a violation of policy.<P>"
    assert "PLACSP" in sesion.bloqueo(respuesta(waf, "text/html; charset=UTF-8", 200))[0]  # 200, no 403


@test
def bundle_fnmt_no_cachea_si_falla():
    """Un primer arranque sin acceso a la sede de FNMT no debe dejar en caché, para siempre, un bundle sin sus CA."""
    import os
    import certifi
    if (sesion.Path(sesion.__file__).resolve().parents[2] / "ca-age.pem").is_file() or os.environ.get("CA_BUNDLE"):
        print("      (hay ca-age.pem o CA_BUNDLE: se omite)")
        return
    pem = sesion.PEM_RE.search(sesion.Path(certifi.where()).read_bytes()).group(0)
    llamadas, responde = [], {"n": 0}

    def get(url, **kw):
        llamadas.append(url)
        if len(llamadas) > responde["n"]:
            raise requests.ConnectionError("sin red")
        return respuesta(pem, "application/x-x509-ca-cert", url=url)

    original, cache, cwd = requests.get, sesion.CACHE, os.getcwd()
    with tempfile.TemporaryDirectory() as d:
        sesion.CACHE, sesion._SIN_BUNDLE = sesion.Path(d), {}
        sesion._VALIDOS.clear()
        requests.get = get
        os.chdir(d)  # sin ca-age.pem en el directorio actual
        silencio = contextlib.redirect_stderr(io.StringIO())  # los avisos de certificados no bajados son esperados
        silencio.__enter__()
        try:
            total = len(sesion.CERTS_FNMT + sesion.CERTS_EXTRA)
            clave = sesion.hashlib.sha1("|".join(sesion._bundles_entorno()).encode()).hexdigest()[:8]
            envenenado = sesion.CACHE / f"ca-age-{clave}.pem"
            envenenado.write_text("solo certifi\n")  # lo que dejaban versiones anteriores al fallar la descarga
            assert sesion.bundle() is True and not list(sesion.CACHE.iterdir())  # ninguno: nada en disco
            n = len(llamadas)
            assert sesion.bundle() is True and len(llamadas) == n  # no reintenta en cada sesión
            sesion._SIN_BUNDLE, llamadas[:], responde["n"] = {}, [], 5
            parcial = sesion.bundle()
            assert parcial.endswith(".parcial.pem") and sesion.Path(parcial).read_text().count("# FNMT") == 5, parcial
            assert sesion.bundle() == parcial  # se reutiliza mientras no caduque
            os.utime(parcial, (0, 0))  # caducado: se rehace y, completo, queda para siempre
            llamadas[:], responde["n"] = [], total
            completo = sesion.bundle()
            assert completo.endswith(".pem") and ".parcial" not in completo, completo
            assert sesion.Path(completo).read_text().count("# FNMT") == total
            assert not [p for p in sesion.CACHE.iterdir() if p.suffix in (".tmp", ".nuevo")]
        finally:
            silencio.__exit__(None, None, None)
            requests.get, sesion.CACHE, sesion._SIN_BUNDLE = original, cache, {}
            sesion._VALIDOS.clear()
            os.chdir(cwd)


@test
def descargar_comprueba_cada_redireccion():
    """Una URL pública que redirige a la red local o a los metadatos de la nube no debe seguirse."""
    import socket
    ips = {"publico.example": "93.184.215.14", "otro.example": "93.184.215.15", "interno.example": "10.0.0.5",
           "127.0.0.1": "127.0.0.1", "169.254.169.254": "169.254.169.254", "mapeado.example": "::ffff:127.0.0.1",
           "cgnat.example": "100.64.0.1"}
    saltos = {"https://publico.example/a": "http://169.254.169.254/latest/meta-data/",
              "https://publico.example/b": "/c", "https://publico.example/c": "https://otro.example/d",
              "https://publico.example/e": "https://interno.example/", "https://publico.example/bucle": "/bucle"}
    pedidas = []

    class S(requests.Session):
        def get(self, url, **kw):
            assert kw.get("allow_redirects") is False, "requests no debe seguir redirecciones por su cuenta"
            pedidas.append(url)
            if url in saltos:
                r = respuesta(b"", "text/html", 302, url)
                r.headers["Location"] = saltos[url]
            else:
                r = respuesta(b'{"ok": 1}', url=url)
            r.raw = io.BytesIO(r._content)  # stream=True lee de raw
            return r

    resolver = socket.getaddrinfo
    socket.getaddrinfo = lambda host, *a, **k: [(None, None, None, "", (ips[host], 0))]
    consulta._S = S()
    try:
        r = consulta.descargar("https://publico.example/b")
        assert r["url"] == "https://otro.example/d" and r["resumen"]["claves"] == ["ok"], r
        assert pedidas == ["https://publico.example/b", "https://publico.example/c", "https://otro.example/d"], pedidas
        for url, motivo in (("https://publico.example/a", "169.254.169.254"), ("https://publico.example/e", "10.0.0.5"),
                            ("https://mapeado.example/", "127.0.0.1"), ("https://cgnat.example/", "100.64.0.1"),
                            ("https://publico.example/bucle", "redirecciones")):
            pedidas.clear()
            try:
                consulta.descargar(url)
            except ValueError as e:
                assert motivo in str(e), (url, e)
            else:
                raise AssertionError(f"{url} debería rechazarse")
            assert not any(p.startswith(("http://169.254", "https://interno", "https://mapeado", "https://cgnat"))
                           for p in pedidas), pedidas
    finally:
        socket.getaddrinfo, consulta._S = resolver, None


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


@test
def ubicar_reconoce_direcciones_y_vias():
    for d in ("calle Alcalá 50, Madrid", "40.4185,-3.696", "-3.9, 40.3", "Rúa do Vilar 1, Santiago de Compostela"):
        assert consulta.es_ubicacion(d), d
    for m in ("Alcalá de Henares", "28079", "280796", "28:900", "L01280796", "P2800500G", "Coruña, A"):
        assert not consulta.es_ubicacion(m), m
    assert consulta._via("Carrer de Pelai 12") == consulta._via("CALLE") == "CALLE"
    assert consulta._via("Avda. de la Paz 3") == "AVENIDA" and consulta._via("Plaza Mayor 1") == "PLAZA"
    assert consulta._palabras("Rúa do Vilar 1") == {"vilar"}  # partículas y número fuera


@test
def bdns_terceros_directorio_nif_nombre():
    filas = js("bdns-terceros-universidad-de-cadiz.json")["terceros"]
    r = bdns.parse_terceros(filas + [{"id": 1, "descripcion": "***0747** - JUAN GARCIA LOPEZ"}])
    uca = next(e for e in r["empresas"] if e["nif"] == "Q1132001G")
    assert uca["id_persona"] == 5958646 and uca["nombres"] == ["UNIVERSIDAD DE CADIZ", "UNIVERSIDAD DE CÁDIZ"]  # 4 filas, espacios fuera
    assert r["personas_fisicas_omitidas"] == 1 and len(r["empresas"]) == 4 and not r["tope"]
    assert bdns.parse_terceros([{"id": i, "descripcion": f"B{i:08d} - X"} for i in range(150)])["tope"]


@test
def radar_filtros_y_salidas():
    import json as _j
    import tempfile
    import xml.etree.ElementTree as ET
    e, _ = placsp.parse_feed((M / "placsp-feed-643.atom").read_bytes())
    assert radar.filtrar_licitaciones(e, {}) == []  # por defecto solo en plazo (PUB) y las dos de la muestra están resueltas
    todas = radar.filtrar_licitaciones(e, {"estados": ["*"]})
    assert len(todas) == 2 and todas[0]["importe"] == 98030.3  # sin la anulación; ordenadas por importe
    assert [x["importe"] for x in radar.filtrar_licitaciones(e, {"estados": ["*"], "cpv": ["45"], "nuts": ["ES3"]})] == [98030.3]
    assert radar.filtrar_licitaciones(e, {"estados": ["*"], "importe_min": 100000}) == []
    s = js("boe-sumario-20260930.json")["data"]["sumario"]
    assert len(radar.filtrar_boe(list(boe.items(s)), {"secciones": ["1"]})) == 3
    convs = js("bdns-convocatorias-busqueda.json")["content"]
    assert [c["detalle"].split()[0] for c in radar.filtrar_ayudas(convs, {"nivel": ["estado"]})] == ["ESTADO"]
    assert radar.filtrar_ayudas(convs, {"palabras": ["sica"]})[0]["id"] == str(convs[0]["numeroConvocatoria"])
    emp = boe.parse_borme_a(ET.fromstring((M / "borme-A-2026-189-28.xml").read_bytes()))
    xs = [{"documento": "BORME-A-2026-189-28", "provincia": "MADRID", "fecha": "2026-09-30", "empresa": x} for x in emp]
    socs = radar.filtrar_sociedades(xs, {})
    assert len(socs) == 1 and socs[0]["titulo"] == "MA5 MAMEY SL" and socs[0]["importe"] == 3000.0
    assert "Nombramientos" not in socs[0]["detalle"]  # solo el acto de constitución, sin personas
    assert radar.casa("Subvenciones a pymes", ["subvención"]) and not radar.casa("Ayudas a pymes", ["subvención"])
    feed = radar.rss(todas, "x")
    assert len(ET.fromstring(feed.encode()).findall(".//item")) == 2
    with tempfile.TemporaryDirectory() as d:  # segunda pasada sin nada nuevo: el estado recuerda lo visto
        import unittest.mock as um
        with um.patch.object(radar, "recoger", lambda *a, **k: todas):
            r1 = radar.ejecutar({"licitaciones": {}}, Path(d, "e.json"), Path(d), 3)
            r2 = radar.ejecutar({"licitaciones": {}}, Path(d, "e.json"), Path(d), 3)
        assert r1["nuevos"] == 2 and r2["nuevos"] == 0 and _j.loads(Path(d, "ultimo.json").read_text())["nuevos"] == 0


@test
def borme_situacion_concursal_sin_personas():
    import xml.etree.ElementTree as ET
    emp = boe.parse_borme_a(ET.fromstring((M / "borme-A-2026-189-28.xml").read_bytes()))
    actos = [boe.parse_concursal(a["texto"]) for e in emp for a in e["actos"] if a["tipo"] == "Situación concursal"]
    assert [(a["resolucion"], a["fecha_resolucion"]) for a in actos] == [
        ("Auto de declaración de concurso", "2026-01-12"), ("Auto de conclusión del concurso", "2026-07-28")]
    assert actos[0]["clase"] == "Voluntario" and actos[0]["firme"] is True and actos[0]["procedimiento"] == "975/2025"
    assert all("PICAZO" not in str(a) for a in actos)  # el juez y demás nombres fuera
    fila = almacen.fila_borme(next(e for e in emp if any(a["tipo"] == "Situación concursal" for a in e["actos"])),
                              "2026-09-30", "BORME-A-2026-189-28", "MADRID")
    assert "Auto de conclusión del concurso" in fila["detalle"] and "PICAZO" not in fila["detalle"]
    xs = [{"documento": "BORME-A-2026-189-28", "provincia": "MADRID", "fecha": "2026-09-30", "empresa": x} for x in emp]
    assert len(radar.filtrar_concursos(xs, {})) == 2 and radar.filtrar_concursos(xs, {}, ["OTRA EMPRESA SL"]) == []


@test
def mivau_compraventas_y_valor_tasado():
    # Filas reales de 34010210 y 35103500 (T2A2026) recortadas a los dos últimos años, 2026-10-05
    c = mivau.parse_compraventas([
        ["", "Número total de transacciones inmobiliarias de viviendas por municipios."],
        ["", "", "", "Año 2025", "", "", "", "Año 2026", ""], ["", "", "", " (trimestre)", "", "", "", "(trimestre)", ""],
        ["", "", "", "1º", "2º", "3º", "4º", "1º", "2º (*)"],
        ["", "ANDALUCÍA", "", "", "", "", "", "", ""], ["", "Granada", "", "", "", "", "", "", ""],
        ["", "Almuñécar", "", 172.0, 177.0, 176.0, 195.0, 177.0, 161.0],
        ["", "Granada", "", 921.0, 996.0, 797.0, 1280.0, 853.0, 877.0],
        ["", "BALEARS (ILLES)", "", "", "", "", "", "", ""],
        ["", "Palma de Mallorca", "", 1378.0, 1287.0, 1182.0, 1287.0, 1080.0, 1152.0],
        ["", "Zamora", "", "", "", "", "", "", ""], ["", "Corrales", "", 1.0, 4.0, 4.0, 4.0, 6.0, 2.0],
        ["", "CATALUÑA", "", "", "", "", "", "", ""], ["", "Barcelona", "", "", "", "", "", "", ""],
        ["", "Barcelona", "", 4516.0, 4773.0, 3649.0, 4373.0, 4061.0, 4625.0], ["", "Font-rubí", "", 3.0, 4.0, 4.0, 5.0, 5.0, 5.0],
        ["", "Granada (La)", "", 2.0, 6.0, 8.0, 14.0, 6.0, 10.0], ["", "Rubí", "", 252.0, 315.0, 229.0, 289.0, 275.0, 254.0],
        ["", "MADRID (COMUNIDAD DE)", "", "", "", "", "", "", ""],
        ["", "Madrid", "", 11344.0, 11462.0, 9051.0, 10654.0, 10038.0, 10343.0],
        ["", "RIOJA (LA)", "", "", "", "", "", "", ""], ["", "CEUTA", "", 171.0, 197.0, 173.0, 192.0, 174.0, 165.0]])
    assert c["trimestres"] == ["2025-T1", "2025-T2", "2025-T3", "2025-T4", "2026-T1", "2026-T2"]
    assert len(c["municipios"]) == 10 and c["municipios"][("Barcelona", "Barcelona")]["2026-T2"] == 4625
    t = mivau.parse_valor_tasado([
        ["", "Provincia", "Municipio", "Valor tasado de vivienda", "", "", "", "Número de tasaciones", "", ""],
        ["", "Almería", "Nijar", "n.r", 1311.0, 1328.7, "", 3.0, 77.0, 80.0],
        ["", "Córdoba", "Córdoba", 2426.4, 1744.0, 1783.8, "", 117.0, 1085.0, 1202.0],
        ["", "", "Almuñecar", "n.r", 3020.7, 3015.8, "", 10.0, 134.0, 144.0],  # de Granada, antes de la fila «Granada»
        ["", "Granada", "Granada", 3010.2, 2429.8, 2446.5, "", 63.0, 726.0, 789.0],
        ["", "ILLES BALEARS", "Palma de Mallorca", 4410.9, 3791.6, 3814.5, "", 79.0, 1195.0, 1274.0],
        ["", "Santa Cruz de", "Adeje", "n.r", 3773.8, 3775.9, "", 6.0, 193.0, 199.0],
        ["", "Tenerife", "San Cristóbal Laguna", 2160.2, 2040.9, 2041.9, "", 25.0, 390.0, 415.0],
        ["", "", "Santa Cruz deTenerife", 2653.3, 2326.2, 2330.0, "", 54.0, 594.0, 648.0],
        ["", "n.r: el dato no es representativo o no existen observaciones"]], "T2A2026 ")
    assert t["trimestre"] == "2026-T2" and t["municipios"][("Almería", "Nijar")]["euros_m2_hasta_5_anios"] is None
    ms = [dict(zip(("ine", "nombre", "provincia"), x), cpro=x[0][:2]) for x in (
        ("04066", "Níjar", "Almería"), ("07040", "Palma", "Illes Balears"), ("08019", "Barcelona", "Barcelona"),
        ("08085", "Font-rubí", "Barcelona"), ("08094", "Granada, La", "Barcelona"), ("08184", "Rubí", "Barcelona"),
        ("14021", "Córdoba", "Córdoba"), ("18017", "Almuñécar", "Granada"), ("18087", "Granada", "Granada"),
        ("28079", "Madrid", "Madrid"), ("38001", "Adeje", "Santa Cruz de Tenerife"),
        ("38023", "San Cristóbal de La Laguna", "Santa Cruz de Tenerife"), ("38038", "Santa Cruz de Tenerife", "Santa Cruz de Tenerife"),
        ("49054", "Corrales del Vino", "Zamora"), ("51001", "Ceuta", "Ceuta"))]
    ic = mivau.indice(c, ms)
    assert {k: f["2026-T2"] for k, f in ic.items()} == {
        "18017": 161, "18087": 877, "07040": 1152, "49054": 2, "08019": 4625, "08085": 5, "08094": 10, "08184": 254,
        "28079": 10343, "51001": 165}  # Rubí no cae en Font-rubí ni Granada en La Granada; Ceuta sin provincia
    it = mivau.indice(t, ms)
    assert sorted(it) == ["04066", "07040", "14021", "18017", "18087", "38001", "38023", "38038"]
    assert it["18017"]["euros_m2"] == 3015.8 and it["38038"]["tasaciones"] == 648 and it["38023"]["euros_m2"] == 2041.9
    assert mivau.clave("Línea de la Concepción (La)") == mivau.clave("Línea de la Concepción, La") == "la linea de la concepcion"


@test
def certificados_energeticos_por_parcela():
    # Respuestas reales del 2026-10-05: Socrata del ICAEN (Aragó 201, Barcelona) y WFS valenciano (calle Colón 10, València)
    cat = consulta.cee_resumen("9723410DF2892D", consulta.cee_cataluna(js("icaen-cee-parcela.json")), "icaen")
    assert cat["certificados"] == 8 and cat["inmuebles"] == 8 and cat["consumo_por_letra"] == {"E": 6, "F": 1, "G": 1}
    assert cat["recientes"][0]["fecha"] == "2026-08-27" and cat["recientes"][0]["kwh_m2_anio"] == 191.1
    filas = consulta.cee_valencia((M / "gva-cee-wfs-parcela.xml").read_bytes())
    gva = consulta.cee_resumen("6021705YJ2762A", filas, "gva")
    assert len(filas) == 4 and gva["inmuebles"] == 3 and gva["consumo_por_letra"] == {"E": 3}  # un piso con dos certificados
    assert gva["recientes"][0]["valido_hasta"] == "2030-10-18" and gva["recientes"][0]["registro"].startswith("E2020")
    assert consulta.certificados_energeticos("05900570129", "01")["nota"].startswith("hace falta")  # catastro foral, sin red


@test
def cerca_recarga_colegios_y_salud():
    # Muestras reales del 2026-10-05: dos emplazamientos de electrolineras.xml y filas de cada directorio autonómico
    sitios = cerca.parse_recarga((M / "dgt-electrolineras-dos-sitios.xml").read_bytes())
    assert len(sitios) == 2 and sitios[0]["cp"] == "07011" and sitios[0]["kw"] == 350.0  # 7011 y 350000.0 W en origen
    assert sitios[0]["operador"] == "Motor Box Mallorca SL" and sitios[0]["direccion"] == "Camí dels Reis 166"
    lat, lon = cerca.utm_a_geo(410649, 4591896, 31)  # La Mercè (Martorell) trae UTM y geográficas: 41.4736, 1.929887
    assert abs(lat - 41.4736) < 1e-3 and abs(lon - 1.929887) < 1e-4
    d = js("cerca-directorios.json")
    cat = cerca.colegios_cataluna(d["colegios_cataluna"])
    assert cat[0]["lat"] == 41.4736 and d["colegios_cataluna"][0]["geo_1"]["coordinates"] == [1929887, 414736]  # sin punto
    mad = cerca.colegios_madrid(d["colegios_madrid"])
    assert len(mad) == 2 and all(abs(p["lat"] - 40.48) < 0.02 for p in mad)  # la baja de La Acebeda fuera; Alcalá en UTM
    assert len(cerca.colegios_valencia(d["colegios_valencia"])) == 2
    andalucia = cerca.colegios_andalucia(d["colegios_andalucia"])
    assert andalucia[0]["lat"] == 37.1408963  # «37,1408963» en origen
    sc = cerca.salud_cataluna(d["salud_cataluna"])
    assert {p["tipo"] for p in sc} <= {"Centres d'atenció primària (CAP)", "Hospitals"} and len(sc) == 2
    sm = cerca.salud_madrid(d["salud_madrid"])
    assert len(d["salud_madrid"]) == 4 and len(sm) == 1 and sm[0]["nombre"] == "CALLE de Arturo Soria 17"  # una fila por especialidad
    sv = cerca.salud_valencia(d["salud_valencia"])
    assert len(sv) == 2 and abs(sv[0]["lat"] - 38.018) < 0.01
    r = cerca.cercanos(cat + sc, 41.4736, 1.929887, 500)
    assert r["en_radio"] == 1 and r["cercanos"][0]["m"] == 0 and "lat" not in r["cercanos"][0]


@test
def radar_una_fuente_caida_no_tumba_las_demas():
    # Sin red, cada fuente lanza: el radar anota el error por fuente, no avanza la fecha y no sale con error parcial
    errores: dict = {}
    assert radar.recoger({"licitaciones": {}, "ayudas": {}}, date(2026, 10, 3), date(2026, 10, 5), lambda m: None, errores) == []
    assert set(errores) == {"licitaciones", "ayudas"} and "AssertionError" in errores["licitaciones"]
    with tempfile.TemporaryDirectory() as d:
        estado = Path(d, "estado.json")
        estado.write_text(json.dumps({"ultima": "2026-10-04", "vistos": {}, "recientes": []}), encoding="utf-8")
        r = radar.ejecutar({"ayudas": {}}, estado, Path(d, "salida"), hoy=date(2026, 10, 5), log=lambda m: None)
        assert r["errores"] and json.loads(estado.read_text(encoding="utf-8"))["ultima"] == "2026-10-04"
        assert "Fuentes con error" in Path(d, "salida", "ultimo.md").read_text(encoding="utf-8")
    assert "Fuentes con error" not in radar.markdown([], date(2026, 10, 5), {})


@test
def formas_de_las_fuentes():
    # check_formas.py: rutas con * (un objeto suelto cuenta como lista de uno), clave de CKAN y Socrata, cabecera CSV
    sys.path.insert(0, str(DIR.parent))
    import check_formas as cf
    boe_ = {"seccion": [{"item": {"id": "A", "titulo": "t"}}, {"item": [{"id": "B", "url_pdf": "u"}]}]}
    assert cf.campos_json(boe_, ["seccion.*.item.*"]) == ["id", "titulo", "url_pdf"]
    ckan_ = {"result": {"fields": [{"id": "_id", "type": "int"}, {"id": "municipio", "type": "text"}]}}
    assert cf.campos_json(ckan_, ["result.fields.*"], "id") == ["_id", "municipio"]
    ine = [{"Nombre": "x", "Data": [{"Valor": 1, "Anyo": 2025}]}]
    assert cf.campos_json(ine, ["*", "*.Data.*"]) == ["*.Data.*:Anyo", "*.Data.*:Valor", "Data", "Nombre"]
    assert cf.campos_csv("Título del fichero\nCódigo mes;Municipio;Paro total\n202608;Abegondo;214\n", 1) == ["Código mes", "Municipio", "Paro total"]
    assert cf.campos_xml(io.BytesIO(b'<f xmlns:a="u"><a:r><a:x/><a:y><a:z/></a:y></a:r><a:r/></f>'), "r") == ["x", "y", "z"]
    assert cf.comparar(["a", "b"], ["b", "c"]) == {"faltan": ["a"], "nuevos": ["c"]}
    assert cf._html(b"\n <!DOCTYPE html><html>") and not cf._html(b"<?xml version=\"1.0\"?><feed>")  # WAF: error, no cambio
    # Toda sonda cita una ficha que existe y tiene forma guardada en la base
    import yaml
    sondas = yaml.safe_load(cf.SONDAS.read_text(encoding="utf-8"))
    base = json.loads(cf.BASE.read_text(encoding="utf-8"))
    fichas = {f.stem for f in (DIR.parent.parent / "sources").rglob("*.yaml")}
    assert len({x["id"] for x in sondas}) == len(sondas)
    assert all(x["ficha"] in fichas for x in sondas), [x["ficha"] for x in sondas if x["ficha"] not in fichas]
    assert all(base.get(x["id"]) for x in sondas), [x["id"] for x in sondas if not base.get(x["id"])]


@test
def cifras_de_control():
    # check_cifras.py sin red: la ejecución del fragmento se sustituye por valores fijos o excepciones
    import ast
    import yaml
    sys.path.insert(0, str(DIR.parent))
    import check_cifras as cc
    assert cc.evaluar("x = 6\ny = [x * i for i in range(3)]\nsum(y) + x") == 24  # el valor es la última expresión
    try:
        cc.evaluar("x = 1")
        raise AssertionError("sin expresión final el valor sería None y cuadraría con esperado null")
    except ValueError:
        pass
    valores, ejecutar, cifras = {}, cc.ejecutar, cc.CIFRAS

    def falso(codigo, timeout):
        if isinstance(valores[codigo], Exception):
            raise valores[codigo]
        return valores[codigo]

    def estado(valor, esperado, tipo="exacto"):
        valores["v"] = valor
        return cc.comprobar({"id": "x", "python": "v", "esperado": esperado, "tipo": tipo})["estado"]
    cc.ejecutar = falso
    try:
        assert estado(753.0, 753) == "ok"  # el INE da 753.0 y el YAML dice 753
        assert estado("753", 753) == "cambio"  # el parser dejó de convertir: texto donde había número
        assert estado(None, 753) == "cambio"  # sin la fila, el fragmento da None en vez de lanzar
        assert estado(None, None) == "ok" and estado(0, None) == "cambio"  # «<5» es secreto: leído como 0 es un cambio
        assert estado("2357531666", "2357531666") == "ok" and estado(True, 1) == "cambio"  # un booleano no es un número
        assert [estado(v, 3, "minimo") for v in (3, 5, 2, None, "4")] == ["ok", "ok", "cambio", "cambio", "cambio"]
        assert estado(ConnectionError("sin red"), 753) == "error"  # la red se informa y no cuenta como cambio
        with tempfile.TemporaryDirectory() as d:  # main sale con 1 solo si alguna cifra no cuadra
            cc.CIFRAS = Path(d, "cifras.yaml")
            cc.CIFRAS.write_text('- {id: a, ficha: x, python: a, esperado: 1, tipo: exacto}\n'
                                 '- {id: b, ficha: x, python: b, esperado: 2, tipo: exacto, segunda_via: CSV crudo}\n',
                                 encoding="utf-8")
            valores.update(a=1, b=TimeoutError("más de 180 s"))
            with contextlib.redirect_stdout(io.StringIO()) as out:
                assert cc.main([]) == 0, out.getvalue()  # un error de red solo no hace fallar la verificación
            valores["b"] = 3
            with contextlib.redirect_stdout(io.StringIO()) as out:
                assert cc.main(["--report"]) == 1 and "| b | x |  | cambio | 3 | 2 |" in out.getvalue(), out.getvalue()
            assert "- b: CSV crudo" in out.getvalue()  # el informe dice cómo confirmar la cifra antes de tocarla
    finally:
        cc.ejecutar, cc.CIFRAS = ejecutar, cifras
    # Cada cifra cita una ficha que existe, tiene todos los campos y un fragmento de hasta 6 líneas que acaba en el valor
    fichas = {f.stem for f in (DIR.parent.parent / "sources").rglob("*.yaml")}
    campos = {"id", "ficha", "usa", "python", "esperado", "tipo", "por_que_estable", "segunda_via", "comprobado"}
    todas = yaml.safe_load(cc.CIFRAS.read_text(encoding="utf-8"))
    assert len({c["id"] for c in todas}) == len(todas)
    for c in todas:
        arbol = ast.parse(c["python"])
        assert campos <= set(c) and c["ficha"] in fichas and c["tipo"] in ("exacto", "minimo"), c["id"]
        assert len(c["python"].strip().splitlines()) <= 6 and isinstance(arbol.body[-1], ast.Expr), c["id"]
        assert {a.name for n in ast.walk(arbol) if isinstance(n, ast.Import) for a in n.names} <= {
            p.stem for p in DIR.glob("*.py")} | set(sys.stdlib_module_names), c["id"]  # un import mal escrito sería error cada lunes


@test
def borme_actos_encadenados_con_punto_y_guion():
    # BORME-A-2026-189-28 (2026-10-05): tres «Situación concursal» de una empresa, el segundo tras «.- »; con el corte solo
    # por «. » quedaban dos y el segundo se perdía dentro del texto del primero (8 actos concursales en el boletín, no 9)
    emp = boe.parse_borme_a(xml("borme-A-2026-189-28-concursal.xml"))
    actos = emp[0]["actos"]
    assert [a["tipo"] for a in actos] == ["Situación concursal"] * 3, [a["tipo"] for a in actos]
    assert actos[0]["texto"].endswith("sustituido por la administración concursal")  # sin el «.-» final
    r = [boe.parse_concursal(a["texto"]) for a in actos]
    assert [x["resolucion"].split(" ")[0] for x in r] == ["Auto", "Resoluciones", "Nombramiento"], [x["resolucion"] for x in r]
    assert r[0]["clase"] == "Necesario" and r[0]["firme"] is False and r[0]["procedimiento"] == "148/2026"

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


@test
def code_valida_llamadas_y_herramientas():
    # validate.py sobre code: las fichas reales solo prueban el caso bueno; esto comprueba que rechaza lo que debe
    sys.path.insert(0, str(DIR.parent))
    import validate
    from common import comandos_paquete, herramientas_mcp
    h, c = {x["name"] for x in herramientas_mcp()}, comandos_paquete()
    bueno = {"module": "fuentes_publicas.clientes.ckan", "mcp": ["ckan_filas"], "use": [
        "ckan.filas('gva', rid, filters={'a': 1}): filas", "fuentes-almacen sync --fuentes borme --desde 2026-10-02: tabla"]}
    assert validate.validate_code("f", bueno, h, c) == []
    malo = {"module": "fuentes_publicas.clientes.nada", "use": ["ckan.no_existe(1): x", "ckan.filas(1)"], "mcp": ["inventada"]}
    errores = " | ".join(validate.validate_code("f", malo, h, c))
    assert all(x in errores for x in ("clientes.nada", "ckan.no_existe", "sin «llamada", "'inventada'")), errores
    assert validate.partir_use("ckan.filas('gva', r, filters={'a': 1}): filas: todas") == ("ckan.filas('gva', r, filters={'a': 1})", "filas: todas")
    largo = {"module": "fuentes_publicas.clientes.boe", "use": ["boe.sumario('2026-10-05'): " + "x" * 130] * 4}
    assert "máximo 600" in " ".join(validate.validate_code("f", largo, h, c))


if __name__ == "__main__":
    sys.exit(main())
