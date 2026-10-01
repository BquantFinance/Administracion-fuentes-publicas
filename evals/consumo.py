#!/usr/bin/env python3
"""Tokens procesados por cada subagente, sumando el usage de cada turno de su transcripción.

El total que devuelve el arnés al terminar un agente es el tamaño de su contexto final; lo que se procesa (y se paga)
es la entrada de cada turno, que reenvía el contexto entero. Este script lee las transcripciones JSONL de Claude Code
(~/.claude/projects/<proyecto>/<sesión>/subagents/agent-*.jsonl) y da por agente: turnos, entrada sin caché, escrita en
caché, leída de caché, entrada total, contexto final y salida estimada.

La salida que registra la transcripción es la del inicio del streaming (1 a 4 tokens), no la final, así que se estima
como caracteres de texto y argumentos de herramienta entre 3,5.

Uso: python evals/consumo.py DIRECTORIO_O_FICHEROS... [--json]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def consumo(path: Path) -> dict:
    turnos: dict[str, dict] = {}
    texto_salida = 0
    for linea in path.open(encoding="utf-8"):
        o = json.loads(linea)
        m = o.get("message") or {}
        if o.get("type") != "assistant" or not m.get("usage"):
            continue
        u = m["usage"]
        t = turnos.setdefault(m.get("id") or str(len(turnos)), {"in": 0, "cw": 0, "cr": 0})
        t["in"] = max(t["in"], u.get("input_tokens", 0))
        t["cw"] = max(t["cw"], u.get("cache_creation_input_tokens", 0))
        t["cr"] = max(t["cr"], u.get("cache_read_input_tokens", 0))
        for bloque in m.get("content") or []:
            if bloque.get("type") == "text":
                texto_salida += len(bloque.get("text", ""))
            elif bloque.get("type") == "tool_use":
                texto_salida += len(json.dumps(bloque.get("input", {}), ensure_ascii=False))
    ts = list(turnos.values())
    entrada = [t["in"] + t["cw"] + t["cr"] for t in ts]
    meta = path.with_suffix(".meta.json")
    desc = json.loads(meta.read_text(encoding="utf-8")).get("description") if meta.exists() else None
    return {
        "agente": path.stem, "descripcion": desc, "turnos": len(ts),
        "entrada_sin_cache": sum(t["in"] for t in ts), "escrita_en_cache": sum(t["cw"] for t in ts),
        "leida_de_cache": sum(t["cr"] for t in ts), "entrada_total": sum(entrada),
        "contexto_final": entrada[-1] if entrada else 0, "salida_estimada": round(texto_salida / 3.5),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("rutas", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    ficheros: list[Path] = []
    for r in map(Path, args.rutas):
        ficheros += sorted(r.glob("agent-*.jsonl")) if r.is_dir() else [r]
    filas = [consumo(f) for f in ficheros]
    if args.json:
        print(json.dumps(filas, ensure_ascii=False, indent=1))
        return 0
    cols = ("turnos", "entrada_sin_cache", "escrita_en_cache", "leida_de_cache", "entrada_total", "contexto_final", "salida_estimada")
    print("| agente | " + " | ".join(cols) + " |")
    print("|---" * (len(cols) + 1) + "|")
    for f in filas:
        print(f"| {f['descripcion'] or f['agente']} | " + " | ".join(f"{f[c]:,}".replace(",", ".") for c in cols) + " |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
