"""SEPE: paro registrado, contratos y demandantes de empleo de todos los municipios, mes a mes, desde los CSV anuales de
datos abiertos (ficha sepe-estadisticas). Desde 2006; el del año en curso se reescribe cada mes en la misma URL.

Trampas que resuelve:
- Llega en windows-1252 aunque Content-Type diga UTF-8, con una línea de título antes de la cabecera y espacios
  sobrantes en los nombres de columna.
- «<5» es secreto estadístico (de 1 a 4), no cero: numero() da None.
- Códigos anteriores a dos fusiones: Oza-Cesuras (15902) sale con ceros y su dato va en Cesuras (15026) y Oza dos Ríos
  (15063); Cerdedo-Cotobade (36902) no tiene fila y su dato va en Cerdedo (36011) y Cotobade (36012). municipio() suma
  los antiguos bajo el código vigente (None en un campo si alguna parte es «<5»).
- Descarga condicional: el servidor responde 304 a If-None-Match, así que la copia en caché solo se renueva si cambió.

Uso: python scripts/clientes/sepe.py [codigo_ine] [paro|contratos|demandantes] [año]
"""
from __future__ import annotations

import csv
import io
import json
import os
import re
import sys
import unicodedata
from datetime import date

try:
    from .sesion import CACHE, sesion
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    from sesion import CACHE, sesion

BASE = "https://sede.sepe.gob.es/es/portaltrabaja/resources/sede/datos_abiertos/datos"
CONJUNTOS = {"paro": "Paro", "contratos": "Contratos", "demandantes": "Dtes_empleo"}
FUSIONES = {"15902": ("15026", "15063"), "36902": ("36011", "36012")}  # código vigente: códigos que usa el SEPE


def url(conjunto: str = "paro", anio: int | None = None) -> str:
    return f"{BASE}/{CONJUNTOS[conjunto]}_por_municipios_{anio or date.today().year}_csv.csv"


def numero(v: str) -> int | None:
    v = v.strip()
    return None if v in ("<5", "") else int(v)


def _clave(nombre: str) -> str:
    s = nombre.strip().replace(">=", " mayor_igual ").replace("<", " menor ")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def leer(contenido: bytes) -> list[dict]:
    """Filas del CSV: mes (AAAA-MM), ccaa, cpro, ine (5 dígitos), municipio y las medidas como enteros o None."""
    lineas = contenido.decode("cp1252").splitlines()
    inicio = next(i for i, l in enumerate(lineas) if l.lower().startswith("código mes"))  # tras la línea de título
    lector = csv.reader(io.StringIO("\n".join(lineas[inicio:])), delimiter=";")
    cab = [_clave(c) for c in next(lector)]
    out = []
    for f in lector:
        if len(f) < 9 or not f[0].strip().isdigit():
            continue
        m = f[0].strip()
        fila = {"mes": f"{m[:4]}-{m[4:6]}", "ccaa": f[2].strip().zfill(2), "cpro": f[4].strip().zfill(2),
                "ine": f[6].strip().zfill(5), "municipio": f[7].strip()}
        fila.update({c: numero(v) for c, v in zip(cab[8:], f[8:])})
        out.append(fila)
    return out


def descargar(conjunto: str = "paro", anio: int | None = None) -> bytes:
    """CSV del año (por defecto el actual) con caché en disco y descarga condicional por ETag."""
    u = url(conjunto, anio)
    ruta = CACHE / "sepe" / u.rsplit("/", 1)[1]
    meta = ruta.with_suffix(".etag")
    cab = {"If-None-Match": meta.read_text()} if ruta.exists() and meta.exists() else {}
    r = sesion().get(u, headers=cab, timeout=180)
    if r.status_code == 304:
        return ruta.read_bytes()
    if r.status_code == 404:
        raise FileNotFoundError(f"el SEPE no tiene {u.rsplit('/', 1)[1]} (hay desde 2006; el del año nuevo sale con el dato de enero)")
    r.raise_for_status()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_bytes(r.content)
    if r.headers.get("ETag"):
        meta.write_text(r.headers["ETag"])
    return r.content


def filas(conjunto: str = "paro", anio: int | None = None) -> list[dict]:
    """Todas las filas del año; si el del año en curso aún no existe (enero), las del anterior."""
    try:
        return leer(descargar(conjunto, anio))
    except FileNotFoundError:
        if anio:
            raise
        return leer(descargar(conjunto, date.today().year - 1))


def municipio(ine: str, conjunto: str = "paro", anio: int | None = None, datos: list[dict] | None = None) -> list[dict]:
    """Serie mensual de un municipio por código INE; en Oza-Cesuras y Cerdedo-Cotobade suma los códigos antiguos."""
    ine = str(ine).zfill(5)
    datos = datos if datos is not None else filas(conjunto, anio)
    codigos = FUSIONES.get(ine, (ine,))
    por_mes: dict[str, dict] = {}
    for f in datos:
        if f["ine"] not in codigos:
            continue
        if f["mes"] not in por_mes:
            por_mes[f["mes"]] = dict(f, ine=ine)
        else:
            acum = por_mes[f["mes"]]
            acum["municipio"] += " + " + f["municipio"]
            for k, v in f.items():
                if k not in ("mes", "ccaa", "cpro", "ine", "municipio"):
                    acum[k] = None if v is None or acum[k] is None else acum[k] + v
    return [por_mes[m] for m in sorted(por_mes)]


if __name__ == "__main__":
    a = sys.argv[1:]
    cod, conj = (a[0] if a else "28005"), (a[1] if len(a) > 1 else "paro")
    serie = municipio(cod, conj, int(a[2]) if len(a) > 2 else None)
    total = next(k for k in serie[-1] if k.startswith("total"))
    print(serie[-1]["municipio"], cod, conj, total, json.dumps({f["mes"]: f[total] for f in serie}))
    oza = municipio("15902", conj, datos=filas(conj, int(a[2]) if len(a) > 2 else None))
    print("Oza-Cesuras 15902 (suma de 15026 y 15063):", oza[-1]["mes"], oza[-1][total])
