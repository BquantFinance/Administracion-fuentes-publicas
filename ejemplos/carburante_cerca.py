#!/usr/bin/env python3
"""Gasolineras más baratas en un radio alrededor de un municipio (MINETUR, ficha minetur-precios-carburantes).

Uso: python ejemplos/carburante_cerca.py "Alcalá de Henares" [gasoleo|gasolina95|gasolina98|glp] [radio_km]

Trampas que resuelve: el municipio de MINETUR no es el código INE (se filtra por provincia, que sí lo es, y por
distancia a la capital del municipio de datos/municipios.csv); precios y coordenadas con coma decimal; precio vacío
es que no vende ese producto; algunas estaciones traen coordenadas 0 o intercambiadas; el servidor corta conexiones
a ratos (la sesión reintenta).
"""
import importlib
import math
import sys

import _ruta

consulta = importlib.import_module(f"{_ruta.PAQUETE}.consulta")
sesion = importlib.import_module(f"{_ruta.PAQUETE}.sesion")

API = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes"
PRODUCTOS = {"gasoleo": "Precio Gasoleo A", "gasolina95": "Precio Gasolina 95 E5",
             "gasolina98": "Precio Gasolina 98 E5", "glp": "Precio Gases licuados del petróleo"}


def num(v: str) -> float | None:
    return float(v.replace(",", ".")) if v and v.strip() else None


def km(lat1, lon1, lat2, lon2) -> float:
    p = math.pi / 180
    a = 0.5 - math.cos((lat2 - lat1) * p) / 2 + math.cos(lat1 * p) * math.cos(lat2 * p) * (1 - math.cos((lon2 - lon1) * p)) / 2
    return 12742 * math.asin(math.sqrt(a))


def main(nombre: str, producto: str = "gasoleo", radio: float = 10) -> None:
    m = consulta.buscar_municipio(nombre, 1)[0]
    lat, lon = float(m["lat"]), float(m["lon"])
    datos = sesion.json(sesion.get(f"{API}/EstacionesTerrestres/FiltroProvincia/{m['cpro']}"))
    clave = PRODUCTOS[producto]
    cerca = []
    for e in datos["ListaEESSPrecio"]:
        precio, la, lo = num(e.get(clave)), num(e["Latitud"]), num(e["Longitud (WGS84)"])
        if precio is None or not la or not lo or not (27 < la < 44.5 and -19 < lo < 5):  # fuera de España: dato malo
            continue
        d = km(lat, lon, la, lo)
        if d <= radio:
            cerca.append((precio, d, e["Rótulo"].strip(), e["Dirección"].strip(), e["Localidad"].strip()))
    print(f"{m['nombre']} ({m['ine']}) · {producto} · {radio:g} km · datos de {datos['Fecha']} · {len(cerca)} estaciones")
    for precio, d, rotulo, dir_, loc in sorted(cerca)[:10]:
        print(f"  {precio:.3f} €/l  {d:4.1f} km  {rotulo} · {dir_}, {loc}")


if __name__ == "__main__":
    a = sys.argv[1:] or ["Alcalá de Henares"]
    main(a[0], a[1] if len(a) > 1 else "gasoleo", float(a[2]) if len(a) > 2 else 10)
