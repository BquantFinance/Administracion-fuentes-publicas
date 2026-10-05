#!/usr/bin/env python3
"""Ministerio de Vivienda: compraventas de vivienda por municipio (tabla 34010210) y valor tasado por municipio de más de
25.000 habitantes (35103500), del Boletín Online en XLS (ficha mivau-precios-vivienda-alquiler).

Uso: python scripts/clientes/mivau.py [municipio]        p. ej. "Alcalá de Henares"

Trampas que resuelve: las tablas no traen código INE, solo nombres bajo cabeceras de comunidad y provincia («Barcelona»
sale como provincia, con la fila vacía, y como municipio), y 79 de 8.131 no casan por nombre ni sin tildes («Palma de
Mallorca», «Villadecanes»); el valor tasado escribe los nombres de otra forma («Ejido (El)», «Santa Cruz deTenerife») y
pone la provincia en una fila cualquiera del grupo (Almuñécar queda bajo Córdoba); «n.r» es no representativo, no cero;
el último trimestre de las compraventas es provisional (*); el valor tasado va en una hoja por trimestre y la última es
la más reciente.
"""
from __future__ import annotations

import re
import sys
import unicodedata

try:
    from .sesion import sesion
except ImportError:
    import os
    sys.path.insert(0, os.path.dirname(__file__))
    from sesion import sesion

TABLA = "https://apps.fomento.gob.es/BoletinOnline2/sedal/{}.XLS"
COMPRAVENTAS, VALOR_TASADO = "34010210", "35103500"


def clave(nombre: str | None) -> str:
    """Nombre comparable entre el INE y el ministerio: sin tildes ni mayúsculas, con el artículo delante («Ejido (El)»,
    «Ejido, El» y «El Ejido» dan «el ejido») y sin la otra lengua tras la barra («Alicante/Alacant» da «alicante»)."""
    s = unicodedata.normalize("NFKD", (nombre or "").split("/")[0].replace("’", "'")).encode("ascii", "ignore")
    s = s.decode().lower().strip()
    m = re.fullmatch(r"(.*?)\s*[(,]\s*(el|la|los|las|l'|els|les|o|a|os|as|lo|sa|es)\s*\)?", s)
    if m:
        s = f"{m.group(2)} {m.group(1)}".replace("l' ", "l'")
    return " ".join(re.sub(r"[^a-z0-9' ]", " ", s).split())


def _num(v) -> float | None:
    if v in ("", None) or str(v).strip().lower() in ("n.r", "n.r.", "-", ".."):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _ent(v) -> int | None:
    x = _num(v)
    return None if x is None else int(x)


def parse_compraventas(filas: list[list]) -> dict:
    """Filas de la hoja de 34010210 a {(provincia, municipio): {trimestre AAAA-Tn: número}} y los trimestres.
    Las cabeceras de comunidad y provincia son filas con nombre y el resto vacío; la última antes de los municipios es la
    provincia (en las uniprovinciales, la comunidad: «MADRID (COMUNIDAD DE)»)."""
    cab = next(i for i, f in enumerate(filas) if any(str(x).startswith("Año ") for x in f))
    años, trim = filas[cab], filas[cab + 2]
    periodos, año = {}, None
    for j, x in enumerate(años):
        if str(x).startswith("Año "):
            año = int(str(x)[4:8])
        if año and str(trim[j]).strip()[:1] in "1234" and str(trim[j]).strip():
            periodos[j] = f"{año}-T{str(trim[j]).strip()[0]}"
    out, provincia = {}, None
    for f in filas[cab + 3:]:
        nombre = str(f[1]).strip() if len(f) > 1 else ""
        if not nombre:
            continue
        if all(str(x).strip() == "" for x in f[2:]):
            provincia = nombre  # cabecera de comunidad o de provincia: la última antes de los municipios es la provincia
            continue
        valores = {p: _ent(f[j]) for j, p in periodos.items() if j < len(f)}
        out[(provincia, nombre)] = valores
    return {"trimestres": list(periodos.values()), "municipios": out}


def parse_valor_tasado(filas: list[list], hoja: str) -> dict:
    """Filas de una hoja de 35103500 (T2A2026) a {(provincia, municipio): {euros_m2, euros_m2_hasta_5_anios,
    euros_m2_mas_5_anios, tasaciones}}. La provincia sale en una sola fila del grupo y no siempre la primera (Almuñécar
    va antes de «Granada»; «Santa Cruz de» y «Tenerife» en dos filas): es solo una pista para indice."""
    out, provincia = {}, None
    for f in filas:
        if len(f) < 10 or not str(f[2]).strip() or _num(f[9]) is None:
            continue
        provincia = str(f[1]).strip() or provincia
        out[(provincia, str(f[2]).strip())] = {"euros_m2": _num(f[5]), "euros_m2_hasta_5_anios": _num(f[3]),
                                               "euros_m2_mas_5_anios": _num(f[4]), "tasaciones": _ent(f[9])}
    m = re.match(r"T(\d)A(\d{4})", hoja.strip())
    return {"trimestre": f"{m.group(2)}-T{m.group(1)}" if m else hoja.strip(), "municipios": out}


def _libro(codigo: str):
    import xlrd
    r = sesion().get(TABLA.format(codigo), timeout=180)
    r.raise_for_status()
    return xlrd.open_workbook(file_contents=r.content)


def compraventas() -> dict:
    s = _libro(COMPRAVENTAS).sheet_by_index(0)
    return parse_compraventas([s.row_values(i) for i in range(s.nrows)])


def valor_tasado() -> dict:
    libro = _libro(VALOR_TASADO)
    s = libro.sheet_by_index(libro.nsheets - 1)  # una hoja por trimestre; la última es la más reciente
    return parse_valor_tasado([s.row_values(i) for i in range(s.nrows)], s.name)


ARTICULO = r"^(el|la|los|las|l'|els|les|o|a|os|as|lo|sa|es) "
# Nombres antiguos o en otra lengua que el ministerio mantiene, con el código INE del municipio renombrado: cada par era
# una fila y un municipio sin casar de la misma provincia, y el código está donde el nombre antiguo caería por orden
# alfabético (Pradales 40161, Villadecanes 24206). Comprobado el 2026-10-05 con las dos tablas.
ALIAS = {"palma de mallorca": "07040", "mahon": "07032", "deya": "07018", "almazora": "12009", "villarreal": "12135",
         "chert": "12052", "adsubia": "03001", "alcocer de planes": "03007", "facheca": "03067", "alfarp": "46026",
         "alfara de algimia": "46024", "villanueva de castellon": "46257", "veracruz": "22246", "candin": "24036",
         "villadecanes": "24206", "pradales": "40161", "puebla de don francisco": "16173", "santa maria de corco": "08254",
         "castell platja d'aro": "17048", "la bisbal de falset": "43027", "sant carles de la rapita": "43136",
         "sant joan de l'enova": "46222", "puig": "46204", "corrales": "49054", "bidegoian": "20024",
         "noain valle de elorz": "31088"}


def _claves(nombre: str | None, partes: bool = False) -> set[str]:
    """Claves de un nombre en cada lengua (tras «/»), con y sin artículo; con partes, también cada trozo separado por «-»
    («Vélez-Málaga» da velez y malaga), que solo se usa si el nombre entero no casa (si no, Rubí caería en Font-rubí)."""
    out = set()
    for lengua in (nombre or "").split("/"):
        for k in {clave(lengua), *([clave(x) for x in lengua.split("-")] if partes else [])}:
            if k:
                out |= {k, re.sub(ARTICULO, "", k)}
    return out


def _cpro(p: str | None, provs: dict) -> str | None:
    """Provincia del ministerio a código: «MADRID (COMUNIDAD DE)», «BALEARS (ILLES)», «Valladodid», «La Coruña» y, en el
    valor tasado, «Santa Cruz de» y «Tenerife» en dos filas."""
    import difflib
    p = clave(p)
    if not p:
        return None
    for k in (p, re.sub(ARTICULO, "", p), " ".join(sorted(p.split()))):
        if k in provs:
            return provs[k]
    for k, c in provs.items():
        if p.startswith(k + " ") or (len(p) >= 8 and (k.startswith(p) or k.endswith(" " + p))):
            return c
    m = difflib.get_close_matches(p, list(provs), 1, 0.8)
    return provs[m[0]] if m else None


def indice(tabla: dict, municipios: list[dict]) -> dict[str, dict]:
    """Código INE de 5 cifras a la fila de la tabla. El ministerio no trae código; cada fila casa, por este orden, con el
    municipio de su provincia de nombre igual (en cualquier lengua), igual sin artículo, igual a un trozo del compuesto
    («Vitoria» con Vitoria-Gasteiz), que empieza o acaba igual («Jarque» con Jarque de Moncayo, «Egüés» con Valle de
    Egüés), el más parecido (erratas: «Santa Coloma Gramanet») o un nombre antiguo de ALIAS. Fuera de su provincia (el
    valor tasado la pone mal a veces) solo si el nombre entero es único en España. Si dos filas caen en un municipio, gana la
    que casa antes; las que no casan se quedan fuera (Sant Joan de l'Ènova no está en el INE)."""
    import difflib
    provs, por_prov, niveles = {}, {}, ({}, {}, {})
    for m in municipios:
        for k in _claves(m["provincia"]):
            provs[k] = provs[" ".join(sorted(k.split()))] = m["cpro"]
        por_prov.setdefault(m["cpro"], []).append(m)
        for k in {clave(x) for x in m["nombre"].split("/")}:
            niveles[0].setdefault(k, []).append(m)
        for i, partes in ((1, False), (2, True)):
            for k in _claves(m["nombre"], partes):
                niveles[i].setdefault(k, []).append(m)
    por_ine = {m["ine"]: m for m in municipios}
    out, nivel = {}, {}
    for (p, nombre), fila in tabla["municipios"].items():
        c, n = _cpro(p, provs), clave(nombre)
        enteros, claves = {clave(x) for x in nombre.split("/")}, _claves(nombre) | {n}
        elegido, paso = None, None
        for i, dic in enumerate(niveles):
            cands = {m["ine"]: m for k in (enteros if i == 0 else claves) for m in dic.get(k, [])}
            en_prov = [m for m in cands.values() if m["cpro"] == c]
            if len(en_prov) == 1:
                elegido, paso = en_prov[0], i
            elif i == 0 and not en_prov and len(cands) == 1:  # fuera de su provincia, solo con el nombre entero
                elegido, paso = next(iter(cands.values())), 0.5
            if elegido:
                break
        if not elegido and c:
            prov = por_prov.get(c, [])
            sin = re.sub(ARTICULO, "", n)
            cont = [m for m in prov if any(k.startswith(sin + " ") or k.endswith(" " + sin) or sin.startswith(k + " ")
                                           for k in _claves(m["nombre"]))]
            if len(cont) == 1:
                elegido, paso = cont[0], 3
            else:
                nombres = {k: m for m in prov for k in _claves(m["nombre"])}
                parecido = difflib.get_close_matches(sin, list(nombres), 1, 0.85)
                if parecido:
                    elegido, paso = nombres[parecido[0]], 4
        if not elegido and n in ALIAS and por_ine[ALIAS[n]]["cpro"] in (c, None):
            elegido, paso = por_ine[ALIAS[n]], 5
        if elegido and nivel.get(elegido["ine"], 9) > paso:
            out[elegido["ine"]], nivel[elegido["ine"]] = fila, paso
    return out


if __name__ == "__main__":
    try:
        from .consulta import buscar_municipio, municipios
    except ImportError:
        from consulta import buscar_municipio, municipios
    m = buscar_municipio(sys.argv[1] if len(sys.argv) > 1 else "Alcalá de Henares", 1)[0]
    c, v = compraventas(), valor_tasado()
    fila = indice(c, municipios()).get(m["ine"])
    print(m["nombre"], "compraventas", {t: fila[t] for t in c["trimestres"][-4:]} if fila else None)
    print(m["nombre"], "valor tasado", v["trimestre"], indice(v, municipios()).get(m["ine"]))
