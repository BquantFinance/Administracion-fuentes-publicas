#!/usr/bin/env python3
"""Resumen del BOE del día (o del último publicado) filtrado por palabras, en Markdown listo para un bot o un correo
(fichas boe-api-sumario y boe-feeds).

Uso: python ejemplos/boe_hoy.py [palabra ...]       p. ej. subvención vivienda
     BOE_FECHA=2026-09-30 python ejemplos/boe_hoy.py

Trampas que resuelve: la API exige Accept application/json (sin él, 400); domingos y festivos no hay BOE (404, se
retrocede al día anterior); un día puede traer número extraordinario y la forma del sumario cambia por sección.
"""
import importlib
import os
import sys
import unicodedata
from datetime import date, datetime, timedelta

import _ruta

boe = importlib.import_module(f"{_ruta.PAQUETE}.boe")


def sin_tildes(s: str) -> str:
    """«subvención» debe casar con «subvenciones»: comparar sin tildes ni mayúsculas."""
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def main(palabras: list[str]) -> None:
    dia = datetime.strptime(os.environ["BOE_FECHA"], "%Y-%m-%d").date() if os.environ.get("BOE_FECHA") else date.today()
    for _ in range(7):
        s = boe.sumario(dia)
        if s:
            break
        dia -= timedelta(days=1)
    items = list(boe.items(s))
    if palabras:
        items = [i for i in items if any(sin_tildes(p) in sin_tildes(i.get("titulo") or "") for p in palabras)]
    print(f"# BOE del {dia:%d/%m/%Y}: {len(items)} disposiciones" + (f" con «{' | '.join(palabras)}»" if palabras else ""))
    seccion = None
    for i in items:
        if i.get("seccion_nombre") != seccion:
            seccion = i.get("seccion_nombre")
            print(f"\n## {seccion}")
        print(f"- [{i['identificador']}]({i.get('url_html') or i.get('url_pdf')}) {i.get('departamento_nombre', '')}: "
              f"{(i.get('titulo') or '')[:220]}")


if __name__ == "__main__":
    main(sys.argv[1:])
