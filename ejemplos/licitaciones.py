#!/usr/bin/env python3
"""Licitaciones nuevas en la Plataforma de Contratación del Sector Público por CPV o palabra, recordando lo ya visto
para avisar solo de lo nuevo (para un cron o un bot; ficha placsp-datos-abiertos).

Uso: python ejemplos/licitaciones.py [prefijo_cpv] [palabra]       p. ej. 72 software  (72: servicios TI)
     LICITACIONES_ESTADO=~/.cache/licitaciones.json python ejemplos/licitaciones.py 45
     LICITACIONES_ESTADOS=PUB,EV python ejemplos/licitaciones.py 45     (por defecto PUB: en plazo, como el radar)

Trampas que resuelve: el feed trae una entrada por cada cambio de estado (vale la más reciente de cada expediente), las
anulaciones llegan como deleted-entry, y la página vigente solo trae lo último (para más, max_paginas, 14-16 MB cada una).
"""
import importlib
import json
import os
import sys
from pathlib import Path

import _ruta

placsp = importlib.import_module(f"{_ruta.PAQUETE}.placsp")
ESTADO = Path(os.path.expanduser(os.environ.get("LICITACIONES_ESTADO", "~/.cache/fuentes-publicas/licitaciones-vistas.json")))
# Un expediente no visto puede estar ya resuelto (RES) o adjudicado (ADJ): para avisar de lo que se puede licitar, PUB
ESTADOS = [x.strip() for x in os.environ.get("LICITACIONES_ESTADOS", "PUB").split(",") if x.strip()]


def main(cpv: str = "", palabra: str = "", paginas: int = 1) -> None:
    vistas = set(json.loads(ESTADO.read_text())) if ESTADO.is_file() else set()
    ultimas: dict[str, dict] = {}
    for e in placsp.entradas(max_paginas=paginas):
        ultimas.setdefault(e["id"], e)  # de la más reciente a la más antigua: vale la primera
    nuevas = [e for e in ultimas.values() if not e.get("deleted") and e["id"] not in vistas
              and (ESTADOS == ["*"] or e.get("estado") in ESTADOS)
              and (not cpv or any(c.startswith(cpv) for c in e.get("cpv") or []))
              and (not palabra or palabra.lower() in (e.get("objeto") or "").lower())]
    print(f"{len(nuevas)} licitaciones nuevas en {'/'.join(ESTADOS)}" + (f" con CPV {cpv}*" if cpv else "") + (f" y «{palabra}»" if palabra else ""))
    for e in sorted(nuevas, key=lambda e: e.get("importe_sin_iva") and float(e["importe_sin_iva"]) or 0, reverse=True)[:25]:
        importe = f"{float(e['importe_sin_iva']):>14,.2f} €" if e.get("importe_sin_iva") else " " * 16
        print(f"{(e.get('fecha_publicacion') or e.get('updated') or '')[:10]} {e.get('estado', ''):4} {importe}  {e.get('organo', '')[:45]} | {(e.get('objeto') or '')[:90]}")
    ESTADO.parent.mkdir(parents=True, exist_ok=True)
    ESTADO.write_text(json.dumps(sorted(vistas | set(ultimas))))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0] if a else "", a[1] if len(a) > 1 else "")
