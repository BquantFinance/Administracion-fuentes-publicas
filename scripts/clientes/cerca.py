#!/usr/bin/env python3
"""Qué hay cerca de un punto: puntos de recarga eléctrica (toda España, DGT con datos del MITERD), centros docentes
(Cataluña, Madrid, Comunitat Valenciana y Andalucía) y centros sanitarios públicos de atención primaria y hospitales
(Cataluña, Madrid y Comunitat Valenciana). Fichas dgt-datex-trafico, centros-docentes-ccaa y centros-sanitarios-ccaa.

Uso: python scripts/clientes/cerca.py 40.4818 -3.3635 [radio_m]

Trampas que resuelve: en Cataluña geo_1 pierde el punto decimal ([1929887, 414736]) y within_circle sobre él da 0 sin
error, y el directorio repite cada centro en cada curso; Madrid da coordenadas UTM y mezcla centros de baja (3.552 de
7.757) y repite cada centro sanitario por especialidad (45.961 filas, 15.867 centros); Andalucía escribe las coordenadas
con coma decimal; el fichero de recarga pesa 83 MB, da la potencia en vatios y el código postal sin el cero inicial.
"""
from __future__ import annotations

import csv
import io
import json
import math
import re
import sys

try:
    from .sesion import sesion
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from sesion import sesion

RECARGA = "https://infocar.dgt.es/datex2/v3/miterd/EnergyInfrastructureTablePublication/electrolineras.xml"
CAT = "https://analisi.transparenciacatalunya.cat/resource/{}.json"
MAD = "https://datos.comunidad.madrid/api/3/action"
GVA = "https://dadesobertes.gva.es/api/3/action"
GVA_SALUD = ("https://terramapas.icv.gva.es/15_SistemaValencianoSalud?request=GetFeature&service=WFS&version=2.0.0"
             "&typename=CentrosSanitarios.{}&outputformat=csv")
AND = "https://www.juntadeandalucia.es/datosabiertos/portal"
MAD_SALUD = ("Hospital general", "Hospital especializado", "Hospital de media y larga estancia",
             "Hospital de salud mental y tratamiento de toxicomanías", "Centro de salud", "Consultorio de atención primaria")
CCAA = {"cat": ("08", "17", "25", "43"), "mad": ("28",), "gva": ("03", "12", "46"),
        "and": ("04", "11", "14", "18", "21", "23", "29", "41")}


def comunidad(cpro: str) -> str | None:
    return next((k for k, v in CCAA.items() if cpro in v), None)


def utm_a_geo(x: float, y: float, huso: int = 30) -> tuple[float, float]:
    """UTM ETRS89 (EPSG:258{huso}) a latitud y longitud, con la serie de Krüger habitual (error de centímetros)."""
    a, f, k0 = 6378137.0, 1 / 298.257222101, 0.9996
    e2 = f * (2 - f)
    ep2 = e2 / (1 - e2)
    x -= 500000.0
    mu = y / k0 / (a * (1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256))
    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))
    p = (mu + (3 * e1 / 2 - 27 * e1 ** 3 / 32) * math.sin(2 * mu) + (21 * e1 ** 2 / 16 - 55 * e1 ** 4 / 32) * math.sin(4 * mu)
         + (151 * e1 ** 3 / 96) * math.sin(6 * mu) + (1097 * e1 ** 4 / 512) * math.sin(8 * mu))
    n = a / math.sqrt(1 - e2 * math.sin(p) ** 2)
    t, c = math.tan(p) ** 2, ep2 * math.cos(p) ** 2
    r = a * (1 - e2) / (1 - e2 * math.sin(p) ** 2) ** 1.5
    d = x / (n * k0)
    lat = p - (n * math.tan(p) / r) * (d ** 2 / 2 - (5 + 3 * t + 10 * c - 4 * c ** 2 - 9 * ep2) * d ** 4 / 24
                                       + (61 + 90 * t + 298 * c + 45 * t ** 2 - 252 * ep2 - 3 * c ** 2) * d ** 6 / 720)
    lon = (d - (1 + 2 * t + c) * d ** 3 / 6 + (5 - 2 * c + 28 * t - 3 * c ** 2 + 8 * ep2 + 24 * t ** 2) * d ** 5 / 120) / math.cos(p)
    return round(math.degrees(lat), 6), round((huso - 1) * 6 - 180 + 3 + math.degrees(lon), 6)


def metros(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 2 * 6371008.8 * math.asin(math.sqrt(h))


def _num(v) -> float | None:
    try:
        x = float(str(v).strip().replace(",", "."))
    except (TypeError, ValueError):
        return None
    return x if x else None  # 0 es «sin coordenada» en los equipamientos de Cataluña


def parse_recarga(xml: bytes) -> list[dict]:
    """electrolineras.xml (DATEX II 3, energyInfrastructureSite) a un emplazamiento por fila: nombre, operador, lat, lon,
    código postal con cero, puntos de recarga, potencia máxima en kW (el fichero da vatios) y tipos de conector."""
    import xml.etree.ElementTree as ET
    out = []
    for _, el in ET.iterparse(io.BytesIO(xml), events=("end",)):
        if not el.tag.endswith("}energyInfrastructureSite"):
            continue
        s: dict = {"nombre": None, "operador": None, "lat": None, "lon": None, "cp": None, "puntos": 0, "kw": 0.0}
        conectores = set()
        for x in el.iter():
            k, v = x.tag.rsplit("}", 1)[-1], (x.text or "").strip()
            if k == "latitude":
                s["lat"] = float(v)
            elif k == "longitude":
                s["lon"] = float(v)
            elif k == "postcode":
                s["cp"] = v.zfill(5)
            elif k == "refillPoint":
                s["puntos"] += 1
            elif k == "maxPowerAtSocket" and v:
                s["kw"] = max(s["kw"], float(v) / 1000)
            elif k == "connectorType":
                conectores.add(v)
            elif k == "value" and s["nombre"] is None:
                s["nombre"] = v  # el primer value es fac:name, a menudo un código del operador (C6E06BCC22ZMPMAKWJ)
            elif k == "value" and v.startswith("Dirección: ") and "direccion" not in s:
                s["direccion"] = v[11:]
        op = el.find(".//{*}operator//{*}value")
        s["operador"] = op.text.strip() if op is not None and op.text else None
        s["conectores"] = sorted(conectores)
        if s["lat"] is not None:
            out.append(s)
        el.clear()
    return out


def colegios_cataluna(filas: list[dict]) -> list[dict]:
    return [{"nombre": f.get("denominaci_completa"), "tipo": f.get("nom_naturalesa"), "lat": _num(f.get("coordenades_geo_y")),
             "lon": _num(f.get("coordenades_geo_x")),
             "ensenanzas": [k.upper() for k in ("einf1c", "einf2c", "epri", "eso", "batx", "cfpm", "cfps") if f.get(k)]}
            for f in filas]


def colegios_madrid(registros: list[dict]) -> list[dict]:
    out = []
    for r in registros:
        if r.get("SITUACIÓN") != "ALTA" or not r.get("UTM_X") or not r.get("UTM_Y"):
            continue  # 3.552 de 7.757 son bajas; 185 activos sin coordenadas
        lat, lon = utm_a_geo(float(r["UTM_X"]), float(r["UTM_Y"]), 30)
        out.append({"nombre": f"{r.get('TIPO_ABRV')} {r.get('CENTRO')}".strip(), "tipo": r.get("TITULARIDAD"), "lat": lat, "lon": lon})
    return out


def colegios_valencia(registros: list[dict]) -> list[dict]:
    return [{"nombre": r.get("denominacion"), "tipo": r.get("regimen"), "lat": _num(r.get("latitud")), "lon": _num(r.get("longitud"))}
            for r in registros]


def colegios_andalucia(texto: str) -> list[dict]:
    return [{"nombre": f"{r.get('D_DENOMINA')} {r.get('D_ESPECIFICA')}".strip(), "tipo": r.get("D_TIPO"),
             "lat": _num(r.get("N_LATITUD")), "lon": _num(r.get("N_LONGITUD"))}  # coma decimal: 37,1408963
            for r in csv.DictReader(io.StringIO(texto), delimiter=";")]


def salud_cataluna(filas: list[dict]) -> list[dict]:
    """categoria lleva varias separadas por «||» (3.214 equipamientos): el tipo es el de la parte de Salut."""
    def tipo(cat: str) -> str | None:
        m = re.search(r"Salut\|Centres sanitaris\|[\d. ]*([^|]+)", cat or "")
        return m.group(1).strip() if m else None
    return [{"nombre": f.get("nom"), "tipo": tipo(f.get("categoria")), "lat": _num(f.get("latitud")),
             "lon": _num(f.get("longitud"))} for f in filas]


def salud_madrid(registros: list[dict]) -> list[dict]:
    """Una fila por centro y especialidad: se queda una por centro_nro_registro. No hay nombre del centro: tipo y calle."""
    vistos, out = set(), []
    for r in registros:
        if r.get("centro_nro_registro") in vistos or not r.get("localizacion_coordenada_x"):
            continue
        vistos.add(r.get("centro_nro_registro"))
        lat, lon = utm_a_geo(float(r["localizacion_coordenada_x"]), float(r["localizacion_coordenada_y"]), 30)
        calle = " ".join(str(r.get(k) or "") for k in ("direccion_vial_tipo", "direccion_vial_nombre", "direccion_vial_nro")).strip()
        out.append({"nombre": calle, "tipo": r.get("centro_tipo"), "lat": lat, "lon": lon})
    return out


def salud_valencia(texto: str) -> list[dict]:
    out = []
    for r in csv.DictReader(io.StringIO(texto)):
        x, y = _num(r.get("x_coord")), _num(r.get("y_coord"))
        if x and y:
            lat, lon = utm_a_geo(x, y, 30)
            out.append({"nombre": r.get("cen_desclar"), "tipo": r.get("tipo"), "lat": lat, "lon": lon})
    return out


def cercanos(puntos: list[dict], lat: float, lon: float, radio: float, n: int = 3) -> dict:
    """Cuántos hay a menos de radio metros y los n más cercanos de esos, con la distancia en metros."""
    dentro = []
    for p in puntos:
        if p.get("lat") is None or p.get("lon") is None or abs(p["lat"] - lat) > radio / 90000 or abs(p["lon"] - lon) > radio / 60000:
            continue
        d = metros(lat, lon, p["lat"], p["lon"])
        if d <= radio:
            dentro.append((d, p))
    dentro.sort(key=lambda t: t[0])
    return {"en_radio": len(dentro), "cercanos": [{"m": round(d), **{k: v for k, v in p.items() if k not in ("lat", "lon")}}
                                                  for d, p in dentro[:n]]}


# Cargas completas (las cachea quien llama): cada una devuelve la lista de puntos de una fuente.
def cargar_recarga() -> list[dict]:
    r = sesion().get(RECARGA, timeout=180)
    r.raise_for_status()
    return parse_recarga(r.content)


def cargar_colegios(ccaa: str) -> list[dict]:
    s = sesion()
    if ccaa == "cat":
        curs = s.get(CAT.format("kvmv-ahh4"), params={"$select": "max(curs) AS c"}, timeout=60).json()[0]["c"]
        filas = s.get(CAT.format("kvmv-ahh4"), timeout=120, params={
            "$where": f"curs='{curs}'", "$limit": 20000, "$select": "denominaci_completa,nom_naturalesa,coordenades_geo_x,"
            "coordenades_geo_y,einf1c,einf2c,epri,eso,batx,cfpm,cfps"}).json()
        return colegios_cataluna(filas)
    if ccaa == "mad":
        r = s.get(f"{MAD}/datastore_search", params={"resource_id": "28d60557-1d73-4281-ab08-6cfd3b2f5f83", "limit": 20000}, timeout=120)
        return colegios_madrid(r.json()["result"]["records"])
    if ccaa == "gva":
        r = s.get(f"{GVA}/datastore_search", params={"resource_id": "1aa53c3a-4639-41aa-ac85-d58254c428c0", "limit": 20000}, timeout=120)
        return colegios_valencia(r.json()["result"]["records"])
    if ccaa == "and":  # el recurso cambia cada curso: el último del conjunto, por la ruta pública (la de package_show no responde)
        p = s.get(f"{AND}/api/3/action/package_show", params={"id": "directorio-de-centros-docentes-de-andalucia"}, timeout=60).json()
        res = max((r for r in p["result"]["resources"] if re.search(r"Curso \d{4}/\d{4}", r.get("name") or "")),
                  key=lambda r: re.search(r"\d{4}/\d{4}", r["name"]).group(0))
        url = re.sub(r"^https://[^/]+/datosabiertos/portal", AND, res["url"])
        r = s.get(url, timeout=180)
        r.raise_for_status()
        return colegios_andalucia(r.content.decode("utf-8-sig"))
    return []


def cargar_salud(ccaa: str) -> list[dict]:
    s = sesion()
    if ccaa == "cat":
        filas = s.get(CAT.format("8gmd-gz7i"), timeout=120, params={
            "$where": "categoria like '%Salut|Centres sanitaris|1.%' OR categoria like '%Salut|Centres sanitaris|3.%'",
            "$select": "nom,categoria,latitud,longitud", "$limit": 20000}).json()
        return salud_cataluna(filas)
    if ccaa == "mad":  # filters y no SQL: datastore_search_sql da 500 con tildes en un literal («atención»)
        r = s.get(f"{MAD}/datastore_search", timeout=120, params={
            "resource_id": "2948b4da-8b39-42b7-b667-779a5284f39d", "limit": 20000,
            "filters": json.dumps({"centro_tipo": list(MAD_SALUD)}, ensure_ascii=False),
            "fields": "centro_nro_registro,centro_tipo,direccion_vial_tipo,direccion_vial_nombre,direccion_vial_nro,"
                      "localizacion_coordenada_x,localizacion_coordenada_y"})
        return salud_madrid(r.json()["result"]["records"])
    if ccaa == "gva":
        out = []
        for capa in ("CentrosSalud", "Hospitales"):
            r = s.get(GVA_SALUD.format(capa), timeout=120)
            r.raise_for_status()
            out += salud_valencia(r.content.decode("utf-8-sig"))
        return out
    return []


if __name__ == "__main__":
    lat, lon = float(sys.argv[1]), float(sys.argv[2])
    radio = float(sys.argv[3]) if len(sys.argv) > 3 else 1000
    print(json.dumps({"recarga": cercanos(cargar_recarga(), lat, lon, radio)}, ensure_ascii=False, indent=1))
