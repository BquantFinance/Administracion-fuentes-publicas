#!/usr/bin/env python3
"""Ficha de un municipio con datos oficiales: sus códigos en cada sistema, población del padrón, renta media y
criminalidad (fichas ine-api-tempus, ine-codigos-territoriales, interior-criminalidad y datos/municipios.csv).

Uso: python ejemplos/mi_municipio.py "Alcalá de Henares"      (nombre, código INE o código SIGPAC como 28:900)

Trampas que resuelve: el INE no filtra por el código de municipio sino por un Id interno (tv=19:Id); con nult=1 el
último periodo puede venir vacío; SIGPAC y Catastro numeran distinto que el INE; la criminalidad solo existe para
municipios de más de 20.000 habitantes y es acumulada desde enero.
"""
import importlib
import sys

import _ruta

consulta = importlib.import_module(f"{_ruta.PAQUETE}.consulta")
ine = importlib.import_module(f"{_ruta.PAQUETE}.ine_tempus")

CRIMINALIDAD = "https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/csv_bdsc/DatosBalanceAct/l0/{}.px?nocab=1"


def main(q: str) -> None:
    m = consulta.buscar_municipio(q, 1)[0]
    print(f"{m['nombre']} · {m['provincia']} · INE {m['ine']} (con control {m['ine']}{m['dc']}) · SIGPAC/Catastro {m['sigpac'] or '-'}")
    print(f"  DIR3 {m['dir3']} · NIF del ayuntamiento {m['nif']} · NUTS3 {m['nuts3']} · capital {m['nucleo']} ({m['lat']}, {m['lon']})")
    mid = ine.id_municipio(m["ine"])
    fecha, pob = ine.ultimo_valor(ine.datos_tabla(29005, tv={19: mid}, nult=2)[0])
    print(f"  Población (padrón a {fecha}): {pob:,.0f}".replace(",", "."))
    try:
        renta = ine.datos_tabla(30824, tv={19: mid, 482: 284048}, nult=1)
        f, v = ine.ultimo_valor(renta[0])
        print(f"  Renta neta media por persona ({f[:4]}): {v:,.0f} €".replace(",", "."))
    except Exception as exc:  # noqa: BLE001  (municipios pequeños sin dato del Atlas de renta)
        print(f"  Renta: sin dato ({type(exc).__name__})")
    for fichero, periodo in (("09006", "enero-junio"), ("09003", "enero-marzo")):
        t = consulta.tabla_pcaxis(CRIMINALIDAD.format(fichero), f"{m['ine']} ", 200)
        tot = [r for r in t["filas"] if "TOTAL INFRACCIONES" in r["Tipología penal"] and r["Periodos:"][:4] != "Vari"]
        if tot:
            print("  Infracciones penales: " + ", ".join(f"{r['Periodos:']} {r['Total']:,}".replace(",", ".") for r in tot)
                  + (" (acumulado desde enero)" if fichero == "09006" else ""))
            break
    else:
        print("  Criminalidad: Interior solo publica municipios de más de 20.000 habitantes")


if __name__ == "__main__":
    main(" ".join(sys.argv[1:]) or "Alcalá de Henares")
