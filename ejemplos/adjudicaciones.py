#!/usr/bin/env python3
"""Quién gana contratos públicos: las mayores adjudicaciones de los últimos días y los adjudicatarios que más suman,
cargadas en el almacén local en Parquet (scripts/clientes/almacen.py; fichas placsp-datos-abiertos y guides/almacen.md).

Uso: python ejemplos/adjudicaciones.py [dias] [prefijo_cpv]          p. ej. 3 72  (72: servicios TI); 0 es solo hoy
     FUENTES_ALMACEN=~/datos/almacen python ejemplos/adjudicaciones.py

Necesita duckdb (pip install duckdb). La primera vez sigue la cadena de los tres feeds hasta el primer día pedido (unos
dos minutos por día desde una red doméstica, más desde algunas nubes); después solo baja lo nuevo. Con 0 basta la
página vigente de cada feed. Trampas que resuelve: una entrada por cambio de estado (vale la última,
vista adjudicaciones_ultimo), una fila por lote y adjudicatario, NIF con guiones o en minúscula normalizado, y los
adjudicatarios personas físicas sin NIF ni nombre (persona_fisica).
"""
import importlib
import sys
from datetime import date, timedelta

import _ruta

almacen = importlib.import_module(f"{_ruta.PAQUETE}.almacen")


def main(dias: int = 1, cpv: str = "") -> None:
    desde = date.today() - timedelta(days=dias)
    alm = almacen.Almacen()
    alm.sync_placsp(desde, float("inf"), log=lambda m: print(m, file=sys.stderr))
    # el 1044 no trae AwardDate (0 de 17.222 en agosto de 2026): se usa la del contrato o la de la entrada
    fecha = "coalesce(a.fecha_adjudicacion, a.fecha_contrato, CAST(a.updated AS DATE))"
    filtro = f"{fecha} >= ? AND a.importe_sin_iva IS NOT NULL"
    params = [desde]
    if cpv:
        filtro += " AND list_any_value(list_filter(p.cpv, c -> starts_with(c, ?))) IS NOT NULL"
        params.append(cpv)
    con = almacen.conectar(alm.dir)
    if not con.execute("SELECT count(*) FROM duckdb_views() WHERE view_name = 'adjudicaciones_ultimo'").fetchone()[0]:
        print(f"Sin adjudicaciones cargadas en {alm.dir}")
        return
    base = f"FROM adjudicaciones_ultimo a JOIN placsp_ultimo p USING (id, updated) WHERE {filtro}"
    # en acuerdos marco el importe del lote se repite en cada adjudicatario: el total cuenta cada lote una vez
    n, total = con.execute(f"SELECT count(*), sum(CASE WHEN a.importe_compartido THEN a.importe_sin_iva / a.adjudicatarios "
                           f"ELSE a.importe_sin_iva END) {base}", params).fetchone()
    print(f"{n} adjudicaciones desde {desde}" + (f" con CPV {cpv}*" if cpv else "") + f", {total or 0:,.0f} € sin IVA")
    print("\nLas diez mayores (sin acuerdos marco con el importe repetido en cada adjudicatario):")
    for f, imp, nif, nombre, organo, objeto, _ in con.execute(
            f"SELECT {fecha}, a.importe_sin_iva, a.nif, a.nombre, p.organo, p.objeto, a.adjudicatarios {base} "
            "AND NOT a.importe_compartido ORDER BY a.importe_sin_iva DESC LIMIT 10", params).fetchall():
        quien = f"{nif} {nombre}" if nif else "(persona física)"
        print(f"{f} {imp:>16,.2f} €  {quien[:45]:45} | {organo[:35]:35} | {(objeto or '')[:60]}")
    print("\nAdjudicatarios que más suman:")
    for nif, nombre, k, imp in con.execute(
            f"SELECT a.nif, any_value(a.nombre), count(*), sum(a.importe_sin_iva) {base} AND a.nif IS NOT NULL "
            "AND NOT a.importe_compartido "
            "GROUP BY a.nif ORDER BY 4 DESC LIMIT 5", params).fetchall():
        print(f"{nif:12} {(nombre or '')[:50]:50} {k:4} contratos {imp:>16,.2f} €")


if __name__ == "__main__":
    a = sys.argv[1:]
    main(int(a[0]) if a else 1, a[1] if len(a) > 1 else "")
