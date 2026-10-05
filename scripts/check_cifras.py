#!/usr/bin/env python3
"""Cifras de control: datos pasados que no cambian (un BORME ya publicado, una página archivada de PLACSP, un año
cerrado) leídos con los clientes de scripts/clientes y comparados con el valor que scripts/cifras.yaml confirmó por otra
vía. check_formas.py avisa si falta un campo; esto, si el número que sale ya no es el correcto: fecha_publicacion de
PLACSP tomaba el primer anuncio y no el de licitación y dio 274 obras publicadas el 01/10/2026 en vez de 126 durante
dos versiones sin que fallara nada.

Uso: python scripts/check_cifras.py [--only id1,id2] [--report]
  --report  informe en markdown (para el issue de la verificación semanal)
Cada fragmento corre en un proceso aparte con su tiempo máximo (timeout de la entrada, si no 180 s). Una excepción o un
tiempo agotado es error: se informa y no cuenta. Sale con 1 solo si alguna cifra no cuadra (cambio).
"""
from __future__ import annotations

import argparse
import ast
import json
import math
import subprocess
import sys
import time
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent
CIFRAS = RAIZ / "cifras.yaml"
TIMEOUT = 180


class ErrorFragmento(RuntimeError):
    """El fragmento lanzó una excepción en su proceso (red, bloqueo, respuesta inesperada)."""


def evaluar(codigo: str):
    """Ejecuta el fragmento y devuelve el valor de su última línea, que tiene que ser una expresión."""
    arbol = ast.parse(codigo)
    if not arbol.body or not isinstance(arbol.body[-1], ast.Expr):
        raise ValueError("la última línea del fragmento tiene que ser una expresión (el valor)")
    ultima = arbol.body.pop()
    ns = {"__name__": "__cifra__"}  # un solo dict: los generadores ven las variables de las líneas de arriba
    exec(compile(arbol, "<cifra>", "exec"), ns)  # noqa: S102  (fragmentos de scripts/cifras.yaml, del propio repo)
    return eval(compile(ast.Expression(ultima.value), "<cifra>", "eval"), ns)  # noqa: S307


def _hijo() -> int:
    """Proceso aparte: fragmento por stdin, {"valor": ...} o {"error": ...} por stdout, en bytes y JSON ASCII para no
    depender de la codificación del sistema. Lo que impriman los clientes va a stderr y no se mezcla con el resultado."""
    sys.path.insert(0, str(RAIZ / "clientes"))
    salida, sys.stdout = sys.stdout, sys.stderr
    try:
        r = {"valor": evaluar(sys.stdin.buffer.read().decode("utf-8"))}
    except BaseException as exc:  # noqa: BLE001  (también el SystemExit de un cliente)
        r = {"error": f"{type(exc).__name__}: {str(exc)[:150]}"}
    salida.write(json.dumps(r, default=repr))
    salida.flush()
    return 0


def ejecutar(codigo: str, timeout: float):
    """Valor del fragmento, calculado en un proceso aparte: un cliente colgado se mata al agotar el tiempo y ninguno
    deja estado (sesiones, cachés en memoria) a los siguientes."""
    try:
        p = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--hijo"], input=codigo, text=True,
                           encoding="utf-8", capture_output=True, timeout=timeout, cwd=RAIZ.parent)
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"más de {timeout:.0f} s") from None
    try:
        r = json.loads(p.stdout)
    except ValueError:
        raise ErrorFragmento(f"sin resultado (código {p.returncode}): {p.stderr.strip()[-150:]}") from None
    if "error" in r:
        raise ErrorFragmento(r["error"])
    return r["valor"]


def _numero(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def cuadra(valor, esperado, tipo: str = "exacto") -> bool:
    """exacto: números como números (753 y 753.0 cuadran; el texto «753» no, porque el parser dejó de convertir), y
    textos y None tal cual (None es secreto o sin dato: 0 no cuadra con él). minimo: un número igual o mayor."""
    if tipo == "minimo":
        return _numero(valor) and _numero(esperado) and valor >= esperado
    if tipo != "exacto":
        raise ValueError(f"tipo {tipo!r}: exacto o minimo")
    if _numero(esperado):
        return _numero(valor) and math.isclose(valor, esperado, rel_tol=1e-9, abs_tol=1e-9)
    return type(valor) is type(esperado) and valor == esperado


def comprobar(c: dict) -> dict:
    """estado ok, cambio o error, con el valor (o el detalle del error) y los segundos."""
    t0 = time.time()
    try:
        valor = ejecutar(c["python"], float(c.get("timeout") or TIMEOUT))
        bien = cuadra(valor, c["esperado"], c.get("tipo", "exacto"))
    except Exception as exc:  # noqa: BLE001
        detalle = str(exc) if isinstance(exc, ErrorFragmento) else f"{type(exc).__name__}: {str(exc)[:150]}"
        return {"estado": "error", "detalle": detalle, "segundos": time.time() - t0}
    return {"estado": "ok" if bien else "cambio", "valor": valor, "segundos": time.time() - t0}


def _txt(v) -> str:
    t = json.dumps(v, ensure_ascii=False, default=repr)
    return t if len(t) <= 60 else t[:57] + "..."


def _esperado(c: dict) -> str:
    return ("≥ " if c.get("tipo") == "minimo" else "") + _txt(c["esperado"])


def _md(s: str) -> str:
    return s.replace("|", "\\|")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--only", help="ids separados por comas")
    p.add_argument("--report", action="store_true")
    p.add_argument("--hijo", action="store_true", help=argparse.SUPPRESS)
    a = p.parse_args(argv)
    if a.hijo:
        return _hijo()
    cifras = yaml.safe_load(CIFRAS.read_text(encoding="utf-8"))
    if a.only:
        ids = set(a.only.split(","))
        erratas = ids - {c["id"] for c in cifras}
        if erratas:
            print("sin cifra: " + ", ".join(sorted(erratas)), file=sys.stderr)
        cifras = [c for c in cifras if c["id"] in ids]
    filas = []
    for c in cifras:
        r = comprobar(c)
        filas.append((c, r))
        if not a.report:
            d = (r["detalle"] if r["estado"] == "error" else
                 _txt(r["valor"]) + ("" if r["estado"] == "ok" else f", esperado {_esperado(c)}"))
            print(f"{r['estado']:6} {c['id']:32} {r['segundos']:5.1f}s  {d}", flush=True)
    cuenta = {e: sum(1 for _, r in filas if r["estado"] == e) for e in ("ok", "cambio", "error")}
    resumen = f"{len(filas)} cifras: " + ", ".join(f"{k} {v}" for k, v in cuenta.items() if v)
    if a.report:
        print(f"# Cifras de control · {time.strftime('%Y-%m-%d')}\n\n{resumen}.\n")
        print("| cifra | ficha | lo usa | resultado | valor | esperado |\n|---|---|---|---|---|---|")
        for c, r in filas:
            valor = r["detalle"] if r["estado"] == "error" else _txt(r["valor"])
            print(f"| {c['id']} | {c['ficha']} | {c.get('usa', '')} | {r['estado']} | {_md(valor)} | {_md(_esperado(c))} |")
        cambios = [c for c, r in filas if r["estado"] == "cambio"]
        if cambios:  # cómo se confirmó la cifra, para repetirlo antes de tocar esperado
            print("\nCambios: confirmar por la segunda vía antes de tocar esperado.\n")
            print("\n".join(f"- {c['id']}: {c.get('segunda_via', '')}" for c in cambios))
    else:
        print(f"\n{resumen}")
    return 1 if cuenta["cambio"] else 0


if __name__ == "__main__":
    sys.exit(main())
