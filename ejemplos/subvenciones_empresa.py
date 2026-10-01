#!/usr/bin/env python3
"""Ayudas públicas de una empresa o entidad por su NIF: subvenciones, ayudas de Estado y minimis de la BDNS, con
totales por año y por convocante (ficha bdns-api).

Uso: python ejemplos/subvenciones_empresa.py Q1132001G

Trampas que resuelve: el NIF se filtra con nifCif (beneficiario es otra cosa, el idPersona interno); beneficiario trae
NIF y nombre en un solo campo; pageSize se recorta a 10.000 sin aviso; las fechas de filtro van en dd/mm/aaaa.
"""
import collections
import importlib
import sys

import _ruta

bdns = importlib.import_module(f"{_ruta.PAQUETE}.bdns")


def eur(v: float, decimales: int = 0) -> str:
    """Importe con formato español (punto de miles, coma decimal)."""
    return f"{v:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"


def main(nif: str) -> None:
    filas = list(bdns.buscar("concesiones", nifCif=nif))
    if not filas:
        print(f"{nif}: sin concesiones en la BDNS")
        return
    nombre = bdns.separar_beneficiario(filas[0]["beneficiario"])[1]
    total = sum(f.get("importe") or 0 for f in filas)
    print(f"{nif} {nombre}: {len(filas)} concesiones, {eur(total, 2)}")
    por_anio = collections.Counter()
    por_organo = collections.Counter()
    for f in filas:
        por_anio[f["fechaConcesion"][:4]] += f.get("importe") or 0
        por_organo[f.get("nivel3") or f.get("nivel2") or f.get("nivel1")] += f.get("importe") or 0
    print("  Por año:", ", ".join(f"{a} {eur(v)}" for a, v in sorted(por_anio.items(), reverse=True)[:6]))
    print("  Principales concedentes:")
    for org, v in por_organo.most_common(5):
        print(f"    {eur(v):>16}  {org}")
    for col in ("ayudasestado", "minimis"):
        o = bdns.pagina(col, 0, 1, nifCif=nif)
        print(f"  {col}: {o.get('totalElements', 0)} registros")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Q1132001G")
