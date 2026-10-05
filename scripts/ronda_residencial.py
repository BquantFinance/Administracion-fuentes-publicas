#!/usr/bin/env python3
"""Ronda de verificación para las fuentes que rechazan o cortan las IP de centros de datos (contenedores, GitHub
Actions): se ejecuta desde una conexión residencial, sin claves, y deja ronda-residencial.md para subirlo a un issue.

Uso: pip install -r scripts/requirements.txt && python scripts/ronda_residencial.py   (unos 5 a 10 minutos)
Corre el example de cada endpoint de esas fichas, las comprobaciones de las recetas que las citan, la portada, la
documentación y los endpoints sin example (las fichas en verified null no tienen) y el cargador de carburantes. No envía nada a ningún sitio ni escribe la IP en el informe. Con el informe, quien mantenga el catálogo
pone fecha en verified o anota en gotchas lo que siga fallando también desde casa.
"""
from __future__ import annotations

import platform
import re
import subprocess
import sys
import time
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
# Fichas cuyos hosts dieron 403, cortes o la página del WAF desde la nube (CLAUDE.md, «Hosts que rechazan IP de
# centros de datos»). datacomex queda fuera: además pide usuario y contraseña.
FICHAS = [
    "catastro-ovc", "ree-redata", "datos-gob-es-api", "bne-datos", "fega-beneficiarios-pac", "oepm-invenes",
    "mitma-opendata-movilidad", "miteco-banco-datos-naturaleza", "isciii-cne", "cis-estudios",
    "inmujeres-mujeres-cifras", "segsocial-estadisticas", "renfe-datos-abiertos", "mincotur-industria-turismo",
    "fecyt-recolecta", "ieca-api-badea", "minetur-precios-carburantes", "placsp-datos-abiertos",
]
CARGADORES = [["ejemplos/carburante_cerca.py", "Alcalá de Henares", "gasoleo", "8"]]


def recetas_que_citan(fichas: list[str]) -> list[str]:
    recetas = yaml.safe_load((RAIZ / "indices" / "recetas.yaml").read_text(encoding="utf-8"))
    return [r["id"] for r in recetas if r.get("checks") and any(p.get("source") in fichas for p in r.get("steps", []))]


def portadas(fichas: list[str], ca: Path) -> str:
    """base_url, docs_url y endpoints con URL completa y sin example: estado, tamaño, tipo y título de cada uno (las
    fichas con verified null no tienen example que probar)."""
    import requests
    ua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
    filas = ["## Portadas y endpoints sin example\n", "| ficha | url | estado | bytes | tipo | título o error |", "|---|---|---|---|---|---|"]
    for f in fichas:
        d = yaml.safe_load(next((RAIZ / "sources").rglob(f"{f}.yaml")).read_text(encoding="utf-8"))
        urls = [d.get("base_url"), d.get("docs_url")] + [e["path"] for e in d.get("endpoints", [])
                                                       if not e.get("example") and e["path"].startswith("http") and "{" not in e["path"]]
        for u in dict.fromkeys(x for x in urls if x):
            try:
                with requests.get(u, headers=ua, timeout=40, stream=True, verify=str(ca) if ca.is_file() else True) as r:
                    cuerpo = r.raw.read(200_000, decode_content=True)
                t = re.search(rb"<title[^>]*>(.*?)</title>", cuerpo, re.S | re.I)
                titulo = t.group(1).decode("utf-8", "replace").strip()[:80] if t else ""
                filas.append(f"| {f} | {u} | {r.status_code} | {len(cuerpo)} | {r.headers.get('content-type', '')[:40]} | {titulo} |")
            except Exception as exc:  # noqa: BLE001
                filas.append(f"| {f} | {u} | error | 0 | | {type(exc).__name__}: {str(exc)[:80]} |")
    return "\n".join(filas) + "\n"


def correr(args: list[str], limite: int = 900) -> tuple[int, str]:
    try:
        p = subprocess.run([sys.executable, *args], cwd=RAIZ, capture_output=True, text=True, timeout=limite,
                           encoding="utf-8", errors="replace")
        return p.returncode, (p.stdout + p.stderr).strip()
    except subprocess.TimeoutExpired:
        return -1, f"sin terminar en {limite} s"


def main() -> int:
    t0 = time.time()
    salida = Path.cwd() / "ronda-residencial.md"
    ca = RAIZ / "ca-age.pem"
    if not ca.is_file():
        print("bundle de CA de FNMT...", flush=True)
        correr(["scripts/fnmt_bundle.py", "--out", str(ca)])
    trozos = [f"# Ronda residencial · {time.strftime('%Y-%m-%d %H:%M')}\n",
              f"Desde una conexión residencial; Python {platform.python_version()} en {platform.system()}.\n"]

    print(f"ejemplos de {len(FICHAS)} fichas...", flush=True)
    informe = RAIZ / "ronda-ejemplos.md"
    rc, log = correr(["scripts/check_ejemplos.py", "--ca", str(ca), "--report", str(informe),
                      *[a for f in FICHAS for a in ("--only", f)]])
    trozos.append(informe.read_text(encoding="utf-8") if informe.is_file() else f"## Ejemplos\n\n```\n{log[-3000:]}\n```\n")
    informe.unlink(missing_ok=True)

    recetas = recetas_que_citan(FICHAS)
    print(f"comprobaciones de {len(recetas)} recetas...", flush=True)
    informe = RAIZ / "ronda-recetas.md"
    rc, log = correr(["scripts/check_recetas.py", "--ca", str(ca), "--report", str(informe),
                      *[a for r in recetas for a in ("--only", r)]])
    trozos.append(informe.read_text(encoding="utf-8") if informe.is_file() else f"## Recetas\n\n```\n{log[-3000:]}\n```\n")
    informe.unlink(missing_ok=True)

    print("portadas y endpoints sin example...", flush=True)
    trozos.append(portadas(FICHAS, ca))

    trozos.append("## Cargadores\n")
    for args in CARGADORES:
        print(" ".join(args) + "...", flush=True)
        rc, log = correr(args, 600)
        trozos.append(f"### {' '.join(args)} · exit {rc}\n\n```\n" + "\n".join(log.splitlines()[-15:]) + "\n```\n")

    salida.write_text("\n".join(trozos), encoding="utf-8")
    print(f"\nlisto en {time.time() - t0:.0f} s: {salida}\nSúbelo a un issue del repositorio (o pásaselo a quien mantenga el catálogo).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
