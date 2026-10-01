#!/usr/bin/env python3
"""Ficha de un municipio con datos oficiales: sus códigos en cada sistema, población del padrón, renta media, paro
registrado y contratos del año y criminalidad (consulta.perfil_municipio; fichas ine-api-tempus, sepe-estadisticas,
interior-criminalidad y datos/municipios.csv). La herramienta MCP perfil_municipio devuelve lo mismo en JSON.

Uso: python ejemplos/mi_municipio.py "Alcalá de Henares"      (nombre, código INE o código SIGPAC como 28:900)

Trampas que resuelve: el INE no filtra por el código de municipio sino por un Id interno (tv=19:Id); con nult=1 el
último periodo puede venir vacío; SIGPAC y Catastro numeran distinto que el INE; el CSV del SEPE llega en windows-1252,
con «<5» por secreto y con Oza-Cesuras y Cerdedo-Cotobade bajo sus códigos de antes de la fusión; la criminalidad solo
existe para municipios de más de 20.000 habitantes y es acumulada desde enero.
"""
import importlib
import sys

import _ruta

consulta = importlib.import_module(f"{_ruta.PAQUETE}.consulta")


def n(v) -> str:
    return "—" if v is None else f"{v:,.0f}".replace(",", ".")


def main(q: str) -> None:
    p = consulta.perfil_municipio(q)
    if "error" in p:
        sys.exit(p["error"])
    m = p["municipio"]
    print(f"{m['nombre']} · {m['provincia']} · INE {m['ine']} (con control {m['ine']}{m['dc']}) · SIGPAC/Catastro {m['sigpac'] or '-'}")
    print(f"  DIR3 {m['dir3']} · NIF del ayuntamiento {m['nif']} · NUTS3 {m['nuts3']} · capital {m['nucleo']} ({m['lat']}, {m['lon']})")
    pob, renta, paro, contr, crim = (p[k] for k in ("poblacion", "renta", "paro_registrado", "contratos", "criminalidad"))
    print(f"  Población (padrón a {pob['padron_a']}): {n(pob['habitantes'])}" if "error" not in pob else f"  Población: {pob['error']}")
    print(f"  Renta neta media por persona ({renta['anio']}): {n(renta['renta_neta_media_por_persona'])} €" if "error" not in renta
          else "  Renta: sin dato del Atlas de renta")
    if "error" not in paro:
        print(f"  Paro registrado ({paro['mes']}): {n(paro['total_paro_registrado'])} · en el año: "
              + ", ".join(f"{k[5:]} {n(v)}" for k, v in paro["serie"].items()))
    if "error" not in contr:
        print(f"  Contratos ({contr['mes']}): {n(contr['total_contratos'])}")
    if "infracciones_penales" in crim:
        print("  Infracciones penales: " + ", ".join(f"{k} {n(v)}" for k, v in crim["infracciones_penales"].items()) + " (acumulado desde enero)")
    else:
        print(f"  Criminalidad: {crim.get('nota') or crim.get('error')}")


if __name__ == "__main__":
    main(" ".join(sys.argv[1:]) or "Alcalá de Henares")
