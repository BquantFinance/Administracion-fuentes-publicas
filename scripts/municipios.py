#!/usr/bin/env python3
"""Genera datos/municipios.csv: una fila por municipio con los códigos que exigen las distintas fuentes.

Columnas: ine (5 dígitos), dc (dígito de control), nombre (INE), cpro, ccaa (código INE), provincia (DIR3), nuts3 (IGN),
ine_tempus_id (Id interno que exige el INE Tempus en tv=19:Id, de VALORES_VARIABLEOPERACION/19/22),
sigpac (código de municipio de SIGPAC, que es el del Catastro: capitales 900), sigpac_cruce (cómo se emparejó con el
INE), dir3 (ayuntamiento, L01 + ine + dc), nif (del ayuntamiento, DIR3), lat y lon (núcleo capital del municipio, IGN,
ETRS89), nucleo (su nombre).

Fuentes, todas sin clave ni CAPTCHA: diccionario de municipios del INE (ine-codigos-territoriales), listas
codigossigpac/municipio{pr}.json de SIGPAC (mapa-sigpac), Listado Unidades EELL de DIR3 (dir3-directorio), colecciones
administrativeunit y nuc de api-features.ign.es (idee-servicios). SIGPAC solo publica nombres, así que se empareja por
nombre normalizado dentro de la provincia (sigpac_cruce nombre o parecido); lo que no casa, y lo emparejado por
parecido, se resuelve consultando SIGPAC en el punto del núcleo capital (punto). Una muestra de 200 emparejados por
nombre se contrasta también por punto y el resultado se imprime.

Uso: python scripts/municipios.py [--out datos/municipios.csv]   (necesita red; unos minutos)
"""
from __future__ import annotations

import argparse
import collections
import csv
import difflib
import io
import random
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

import openpyxl

from clientes import ogc
from clientes.sesion import json, sesion
from common import ROOT

IGN = "https://api-features.ign.es/collections"
DIR3_EELL = ("https://administracionelectronica.gob.es/ctt/resources/Soluciones/238/Descargas/"
             "Listado%20Unidades%20EELL.xlsx?idIniciativa=238&idElemento=2744")
ARTICULOS = ("el", "la", "los", "las", "l", "o", "a", "os", "as", "es", "sa", "ses", "s", "lo", "els", "les", "en", "na")
S = sesion(accept="application/json, */*;q=0.8")


def norm(nombre: str) -> str:
    """Minúsculas sin tildes ni signos, con el artículo pospuesto delante: «ACEBEDA (LA)» y «Acebeda, La» dan «la acebeda»."""
    n = unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode().lower().strip()
    m = re.fullmatch(r"(.+?)\s*[,(]\s*(\w+)\s*\)?", n)
    if m and m.group(2) in ARTICULOS:
        n = f"{m.group(2)} {m.group(1)}"
    return re.sub(r"[^a-z0-9]+", " ", n).strip()


def variantes(nombre: str) -> list[str]:
    """Formas a comparar: el nombre entero y cada parte de los bilingües (Alicante/Alacant, Donostia/San Sebastián)."""
    partes = [nombre] + [p for p in re.split(r"\s*/\s*|\s+-\s+", nombre) if p != nombre]
    return list(dict.fromkeys(norm(p) for p in partes))


def xlsx(datos: bytes, fila_cabecera: int, hoja: int = 0) -> list[dict]:
    wb = openpyxl.load_workbook(io.BytesIO(datos), read_only=True)
    ws = wb.worksheets[hoja]
    ws.reset_dimensions()  # algunos xlsx declaran A1:A1 y openpyxl en modo read_only no leería más
    filas = list(ws.iter_rows(values_only=True))
    cab = filas[fila_cabecera]
    return [dict(zip(cab, f)) for f in filas[fila_cabecera + 1:] if any(f)]


def ine() -> tuple[list[dict], str]:
    for anio in (date.today().year, date.today().year - 1):
        url = f"https://www.ine.es/daco/daco42/codmun/diccionario{anio % 100:02d}.xlsx"
        r = S.get(url)
        if r.ok and r.content[:2] == b"PK":
            filas = xlsx(r.content, 1)
            return [{"ine": f"{f['CPRO']}{f['CMUN']}", "dc": f["DC"], "nombre": f["NOMBRE"], "cpro": f["CPRO"],
                     "ccaa": f["CODAUTO"]} for f in filas if f.get("CMUN")], url
    raise RuntimeError("no encuentro el diccionario de municipios del INE de este año ni del anterior")


def tempus() -> dict[str, int]:
    """Código INE -> Id interno del INE Tempus (variable 19); la llamada tarda de 30 s a varios minutos."""
    r = S.get("https://servicios.ine.es/wstempus/js/ES/VALORES_VARIABLEOPERACION/19/22", timeout=600)
    return {v["Codigo"]: v["Id"] for v in json(r)}


def sigpac(cpros: list[str]) -> dict[str, list[tuple[int, str]]]:
    out = {}
    for p in cpros:
        r = S.get(f"https://sigpac-hubcloud.es/codigossigpac/municipio{int(p)}.json")
        out[p] = [(c["codigo"], c["descripcion"]) for c in json(r)["codigos"]] if r.ok else []
    return out


def emparejar(munis: list[dict], lista: list[tuple[int, str]]) -> dict[str, tuple[int, str]]:
    """INE -> (código SIGPAC, método): nombre exacto normalizado, una parte del bilingüe o parecido único (>= 0,92)."""
    por_nombre = collections.defaultdict(list)
    for cod, nom in lista:
        for v in variantes(nom):
            por_nombre[v].append(cod)
    res, usados = {}, collections.Counter()
    for m in munis:
        cands = {c for v in variantes(m["nombre"]) for c in por_nombre.get(v, [])}
        if len(cands) == 1:
            res[m["ine"]] = (cands.pop(), "nombre")
    libres = [(c, n) for c, n in lista if c not in {v[0] for v in res.values()}]
    for m in munis:
        if m["ine"] in res:
            continue
        mejor = sorted(((max(difflib.SequenceMatcher(None, a, b).ratio() for a in variantes(m["nombre"])
                             for b in variantes(n)), c) for c, n in libres), reverse=True)[:2]
        if mejor and mejor[0][0] >= 0.92 and (len(mejor) == 1 or mejor[1][0] < mejor[0][0] - 0.05):
            res[m["ine"]] = (mejor[0][1], "parecido")
    for cod, _ in res.values():
        usados[cod] += 1
    return {k: v for k, v in res.items() if usados[v[0]] == 1}  # un código para dos municipios: no fiable


def por_punto(lat: float, lon: float) -> str | None:
    """provincia:municipio del recinto SIGPAC que contiene el punto (None si no hay recinto)."""
    c = json(S.get(f"https://sigpac-hubcloud.es/servicioconsultassigpac/query/recinfobypoint/4326/{lon}/{lat}.json"))
    return f"{c[0]['provincia']}:{c[0]['municipio']}" if c else None


def dir3() -> tuple[dict[str, dict], dict[str, str]]:
    r = S.get(DIR3_EELL)
    filas = xlsx(r.content, 1)
    ay = {f["C_ID_UD_ORGANICA"]: f for f in filas
          if f.get("C_ID_TIPO_ENT_PUBLICA") == "AY" and str(f.get("N_NIVEL_JERARQUICO")) == "1"
          and str(f.get("C_ID_UD_ORGANICA", "")).startswith("L01")}
    prov = {str(f["C_ID_AMB_PROVINCIA"]).zfill(2): str(f["C_DESC_PROV"]).strip() for f in filas
            if f.get("C_ID_AMB_PROVINCIA") and f.get("C_DESC_PROV")}
    return ay, prov


def ign() -> tuple[dict[str, str], dict[str, dict]]:
    nuts = {}
    for f in ogc.entidades(f"{IGN}/administrativeunit/items", limit=1000, nationallevelname="Municipio",
                           skipGeometry="true", f="json"):
        p = f["properties"]
        nuts[p["nationalcode"][-5:]] = p.get("codnut3")
    nucleos = collections.defaultdict(list)
    for f in ogc.entidades(f"{IGN}/nuc/items", limit=1000, skipGeometry="true", f="json"):
        p = f["properties"]
        nucleos[p["codine"][:5]].append(p)
    capital = {m: sorted(l, key=lambda p: (str(p.get("capital", "0000"))[3:4] != "1", -(p.get("habitantes") or 0)))[0]
               for m, l in nucleos.items()}
    return nuts, capital


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "datos" / "municipios.csv"))
    a = ap.parse_args()
    munis, url_ine = ine()
    cpros = sorted({m["cpro"] for m in munis})
    listas = sigpac(cpros)
    ay, prov = dir3()
    nuts, capital = ign()
    ids_tempus = tempus()
    por_prov = collections.defaultdict(list)
    for m in munis:
        por_prov[m["cpro"]].append(m)
    cruce = {}
    for p, lista in listas.items():
        cruce.update(emparejar(por_prov[p], lista))
    filas = []
    for m in sorted(munis, key=lambda m: m["ine"]):
        cod = f"L01{m['ine']}{m['dc']}"
        c = capital.get(m["ine"])
        sp = cruce.get(m["ine"])
        sigpac_cod, metodo = (f"{int(m['cpro'])}:{sp[0]}", sp[1]) if sp else ("", "sin lista" if not listas.get(m["cpro"]) else "sin casar")
        if metodo in ("parecido", "sin casar") and c:
            punto = por_punto(c["latitud"], c["longitud"])
            if punto and punto.split(":")[0] == str(int(m["cpro"])):
                sigpac_cod, metodo = punto, "punto"
        filas.append({
            "ine": m["ine"], "dc": m["dc"], "nombre": m["nombre"], "cpro": m["cpro"], "ccaa": m["ccaa"],
            "provincia": prov.get(m["cpro"], ""), "nuts3": nuts.get(m["ine"]) or "", "ine_tempus_id": ids_tempus.get(m["ine"], ""),
            "sigpac": sigpac_cod, "sigpac_cruce": metodo,
            "dir3": cod if cod in ay else "", "nif": (ay[cod].get("NIF_CIF") or "").strip() if cod in ay else "",
            "lat": round(c["latitud"], 6) if c else "", "lon": round(c["longitud"], 6) if c else "",
            "nucleo": c["nombre"] if c else "",
        })
    out = ROOT / a.out if not a.out.startswith("/") else a.out

    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(filas)

    muestra = random.Random(1).sample([f for f in filas if f["sigpac_cruce"] == "nombre" and f["lat"] != ""], 200)
    iguales = sum(1 for f in muestra if por_punto(f["lat"], f["lon"]) == f["sigpac"])
    distintos = sum(1 for f in filas if f["sigpac"] and not f["sigpac"].endswith(":900")
                    and int(f["sigpac"].split(":")[1]) != int(f["ine"][2:]))
    print(f"contraste por punto: {iguales}/200 emparejados por nombre coinciden; SIGPAC distinto del INE fuera de las "
          f"capitales en {distintos} municipios")
    cuenta = collections.Counter(f["sigpac_cruce"] for f in filas)
    print(f"{out}: {len(filas)} municipios ({url_ine}); sigpac {dict(cuenta)}; dir3 {sum(1 for f in filas if f['dir3'])}; "
          f"nuts3 {sum(1 for f in filas if f['nuts3'])}; tempus {sum(1 for f in filas if f['ine_tempus_id'] != '')}; coordenadas {sum(1 for f in filas if f['lat'] != '')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
