#!/usr/bin/env python3
"""Detecta fuentes que cambian de forma sin avisar: compara los campos de hoy de cada sonda de scripts/formas.yaml con
los guardados en scripts/formas-base.json. Un campo que falta es un fallo (el cliente que lo lee daría None sin error,
como cuando la Comunidad de Madrid sacó padron_por_sexo del datastore); uno nuevo solo se informa.

Uso: python scripts/check_formas.py [--only id1,id2] [--report] [--actualizar [id1,id2]]
  --report      informe en markdown (para el issue de la verificación semanal)
  --actualizar  guarda en la base la forma de hoy (todas o las indicadas), tras comprobar que el cambio es real
Sale con 1 si a alguna sonda le falta un campo de la base; un error de red o una página HTML (WAF) se informa pero
no cuenta como cambio.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "clientes"))
from sesion import sesion  # noqa: E402

SONDAS = RAIZ / "formas.yaml"
BASE = RAIZ / "formas-base.json"


def _recorre(dato, ruta: list[str]) -> list:
    """Sigue una ruta con puntos; * recorre los elementos de una lista, y un objeto suelto cuenta como lista de uno
    (el BOE da item como lista o como objeto según haya uno o varios)."""
    actuales = [dato]
    for paso in ruta:
        siguientes = []
        for x in actuales:
            if paso == "*":
                siguientes += x if isinstance(x, list) else [x] if isinstance(x, dict) else []
            elif isinstance(x, dict) and paso in x:
                siguientes.append(x[paso])
            elif isinstance(x, list) and paso.isdigit() and int(paso) < len(x):
                siguientes.append(x[int(paso)])
        actuales = siguientes
    return actuales


def campos_json(dato, rutas: list[str], clave: str | None = None) -> list[str]:
    """Campos de los registros a los que llevan las rutas: sus claves, o el valor de `clave` en cada uno (CKAN fields,
    Socrata columns). Con varias rutas, cada campo lleva delante la ruta (salvo la primera) para distinguirlos."""
    out = set()
    for i, r in enumerate(rutas):
        registros = _recorre(dato, r.split("."))
        for reg in registros[:200]:
            if not isinstance(reg, dict):
                continue
            nombres = [str(reg[clave])] if clave and clave in reg else ([] if clave else list(reg))
            out |= {n if i == 0 else f"{r}:{n}" for n in nombres}
    return sorted(out)


def campos_csv(texto: str, salta: int = 0) -> list[str]:
    lineas = texto.splitlines()[salta:salta + 5]
    muestra = "\n".join(lineas)
    try:
        sep = csv.Sniffer().sniff(muestra, delimiters=";,|\t").delimiter
    except csv.Error:
        sep = ";" if muestra.count(";") > muestra.count(",") else ","
    cabecera = next(csv.reader(io.StringIO(lineas[0] if lineas else ""), delimiter=sep), [])
    return [c.strip() for c in cabecera if c.strip()]


def campos_xml(contenido, registro: str) -> list[str]:
    """Nombres locales de los descendientes del primer elemento `registro` (lee en flujo y para ahí)."""
    for _, el in ET.iterparse(contenido, events=("end",)):
        if el.tag.rsplit("}", 1)[-1] == registro:
            return sorted({x.tag.rsplit("}", 1)[-1] for x in el.iter()} - {registro})
    return []


def campos_xls(contenido: bytes, hoja: int, filas: list[int]) -> list[str]:
    import xlrd
    libro = xlrd.open_workbook(file_contents=contenido)
    s = libro.sheet_by_index(hoja if hoja >= 0 else libro.nsheets + hoja)
    return sorted({" ".join(str(c).split()) for f in filas if f < s.nrows for c in s.row_values(f) if str(c).strip()})


def _html(inicio: bytes) -> bool:
    """Una página HTML donde se esperaba otro formato es un bloqueo o una página de error (el WAF de PLACSP responde
    200 con su página), no un cambio de forma."""
    return inicio.lstrip()[:15].lower().startswith((b"<!doctype html", b"<html"))


def forma(sonda: dict) -> list[str]:
    s = sesion()
    tipo = sonda["tipo"]
    if tipo == "xml":  # en flujo: electrolineras.xml pesa 83 MB y basta el primer registro
        with s.get(sonda["url"], headers=sonda.get("cabeceras"), timeout=180, stream=True) as r:
            r.raise_for_status()
            r.raw.decode_content = True
            flujo = io.BufferedReader(r.raw, 1 << 16)
            if _html(flujo.peek(512)):
                raise RuntimeError("HTML en vez de XML: bloqueo o página de error")
            return campos_xml(flujo, sonda["registro"])
    r = s.get(sonda["url"], headers=sonda.get("cabeceras"), timeout=180)
    r.raise_for_status()
    if _html(r.content[:512]):
        raise RuntimeError(f"HTML en vez de {tipo.upper()}: bloqueo o página de error")
    if tipo == "json":
        return campos_json(r.json(), sonda["rutas"], sonda.get("clave"))
    if tipo == "csv":
        cod = sonda.get("codificacion")
        texto = r.content.decode(cod) if cod else r.content.decode("utf-8-sig", errors="replace")
        return campos_csv(texto, sonda.get("salta", 0))
    if tipo == "xls":
        return campos_xls(r.content, sonda.get("hoja", 0), sonda["filas"])
    raise ValueError(f"tipo desconocido: {tipo}")


def comparar(base: list[str], hoy: list[str]) -> dict:
    return {"faltan": sorted(set(base) - set(hoy)), "nuevos": sorted(set(hoy) - set(base))}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--only", help="ids separados por comas")
    p.add_argument("--report", action="store_true")
    p.add_argument("--actualizar", nargs="?", const="*", help="guarda la forma de hoy en la base")
    a = p.parse_args(argv)
    sondas = yaml.safe_load(SONDAS.read_text(encoding="utf-8"))
    if a.only:
        ids = set(a.only.split(","))
        sondas = [x for x in sondas if x["id"] in ids]
    base = json.loads(BASE.read_text(encoding="utf-8")) if BASE.is_file() else {}
    filas, cambios = [], 0
    for sonda in sondas:
        t0 = time.time()
        try:
            hoy = forma(sonda)
        except Exception as exc:  # noqa: BLE001
            filas.append((sonda, "error", f"{type(exc).__name__}: {str(exc)[:150]}", time.time() - t0))
            continue
        if a.actualizar and (a.actualizar == "*" or sonda["id"] in a.actualizar.split(",")):
            base[sonda["id"]] = hoy
            filas.append((sonda, "guardada", f"{len(hoy)} campos", time.time() - t0))
            continue
        if sonda["id"] not in base:
            filas.append((sonda, "sin base", f"{len(hoy)} campos; --actualizar {sonda['id']}", time.time() - t0))
            continue
        c = comparar(base[sonda["id"]], hoy)
        if not hoy:
            estado, detalle = "cambio", "ningún campo: la respuesta ya no tiene la forma esperada"
            cambios += 1
        elif c["faltan"]:
            estado, detalle = "cambio", "faltan " + ", ".join(c["faltan"][:12]) + (f"; nuevos {', '.join(c['nuevos'][:8])}" if c["nuevos"] else "")
            cambios += 1
        elif c["nuevos"]:
            estado, detalle = "ok", "nuevos " + ", ".join(c["nuevos"][:12])
        else:
            estado, detalle = "ok", f"{len(hoy)} campos"
        filas.append((sonda, estado, detalle, time.time() - t0))
    if a.actualizar:
        BASE.write_text(json.dumps(base, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    cuenta = {e: sum(1 for f in filas if f[1] == e) for e in ("ok", "cambio", "error", "sin base", "guardada")}
    if a.report:
        print(f"# Forma de las fuentes · {time.strftime('%Y-%m-%d')}\n")
        print(f"{len(filas)} sondas: " + ", ".join(f"{k} {v}" for k, v in cuenta.items() if v) + ".\n")
        print("| sonda | ficha | lo usa | resultado | detalle |\n|---|---|---|---|---|")
        for s_, e, d, _ in filas:
            print(f"| {s_['id']} | {s_['ficha']} | {s_.get('usa', '')} | {e} | {d} |")
    else:
        for s_, e, d, t in filas:
            print(f"{e:9} {s_['id']:24} {t:5.1f}s  {d}")
        print(f"\n{len(filas)} sondas: {cuenta}")
    return 1 if cambios else 0


if __name__ == "__main__":
    sys.exit(main())
