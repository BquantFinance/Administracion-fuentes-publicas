#!/usr/bin/env python3
"""Ejecuta el `example` de cada endpoint de las fichas contra los servidores reales y comprueba que responde.

Uso: check_ejemplos.py [--only ID ...] [--report FICHERO.md] [--fail] [--ca BUNDLE] [--muestra N] [--timeout S]

Solo ejecuta ejemplos que son una URL o un curl, sin shell: se descarta lo que va tras una tubería (iconv, sed...) y
las opciones de curl que escriben o leen ficheros. Las variables se expanden como en bash ($VAR y ${VAR} fuera de
comillas simples) con el entorno; si falta una en mayúsculas el ejemplo queda skipped (así se pasan claves como
AEMET_KEY en GitHub Actions sin escribirlas) y si es una en minúsculas, como $limit de Socrata entre comillas dobles,
es fail: al pegarlo en una shell se expandiría a vacío. Resultado: ok (2xx), redirect (3xx sin -L), fail (4xx, 5xx o
variable mal escapada), blocked (WAF o bloqueo de red reconocido), error (sin respuesta) o skipped (también si
lee con -b la cookie que deja otro ejemplo).
--muestra N imprime los primeros N bytes de cada respuesta. Espera entre peticiones al mismo host (3 s al Catastro).
"""
from __future__ import annotations

import argparse
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from common import load_sources

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
BLOQUEO = (b"Petici\xc3\xb3n HTTP bloqueada", b"Petici&#243;n HTTP bloqueada", b"Request Rejected", b"The requested URL was rejected", b"Incapsula",
           b"Making sure you", b"Voight-Kampff", b"Checking you are not a bot", b"Acceso denegado")
LARGAS_CON_VALOR = {"--header", "--user-agent", "--data", "--data-urlencode", "--data-raw", "--data-binary", "--request",
                    "--referer", "--cookie", "--user", "--connect-timeout", "--max-time", "--range", "--form", "--retry",
                    "--retry-delay", "--limit-rate", "--max-filesize", "--resolve", "--connect-to", "--continue-at",
                    "--time-cond", "--url"}
CORTAS_CON_VALOR = set("HAdXebuFrmxEToKwcDCz")
# opciones que tocan ficheros, el proxy o la verificación TLS: se quitan con su valor (el bundle va con --ca)
PROHIBIDAS = {"-o", "--output", "-K", "--config", "-T", "--upload-file", "-w", "--write-out", "-c", "--cookie-jar",
              "-D", "--dump-header", "--output-dir", "--cacert", "--capath", "-x", "--proxy", "-E", "--cert", "--key"}
CORTAS_PROHIBIDAS = set("oKTwcDxE")
CORTAS_FUERA = set("sSOvikJ")  # silencio, nombre remoto, verbosidad, inseguro: las fija el comprobador
LARGAS_FUERA = {"--silent", "--show-error", "--remote-name", "--insecure", "--verbose", "--include", "--remote-header-name"}
VAR = re.compile(r"\$(\{([A-Za-z_][A-Za-z0-9_]*)\}|([A-Za-z_][A-Za-z0-9_]*))")


def expandir(texto: str) -> tuple[str, list[str], list[str]]:
    """Expande $VAR fuera de comillas simples, como bash. Devuelve texto, variables que faltan y variables en minúsculas."""
    out, faltan, minusculas, i, simple = [], [], [], 0, False
    while i < len(texto):
        c = texto[i]
        if c == "'" and not simple and (i == 0 or texto[i - 1] != "\\"):
            simple = True
        elif c == "'" and simple:
            simple = False
        elif c == "$" and not simple and (i == 0 or texto[i - 1] != "\\"):
            m = VAR.match(texto, i)
            if m:
                nombre = m.group(2) or m.group(3)
                if nombre.islower():
                    minusculas.append(nombre)
                elif nombre not in os.environ:
                    faltan.append(nombre)
                out.append(os.environ.get(nombre, ""))
                i = m.end()
                continue
        out.append(c)
        i += 1
    return "".join(out), faltan, minusculas


def argumentos(ejemplo: str) -> list[str] | None:
    """Argumentos de curl sin las opciones que tocan ficheros; None si el ejemplo no es una URL ni un curl."""
    ejemplo = ejemplo.strip()
    if ejemplo.startswith("http"):
        return [ejemplo.split()[0]]
    lex = shlex.shlex(ejemplo, posix=True, punctuation_chars="|;&")
    lex.whitespace_split = True
    try:
        tokens = list(lex)
    except ValueError:
        return None
    for corte in ("|", "||", "&&", ";", "&"):
        if corte in tokens:
            tokens = tokens[: tokens.index(corte)]
    if not tokens or tokens[0] != "curl":
        return None
    args, i = [], 1
    while i < len(tokens):
        t = tokens[i]
        siguiente = tokens[i + 1] if i + 1 < len(tokens) else None
        if t in PROHIBIDAS:
            i += 2
        elif t.startswith("--"):
            if t in LARGAS_FUERA or t.split("=", 1)[0] in PROHIBIDAS:
                i += 1
            elif "=" not in t and t in LARGAS_CON_VALOR and siguiente is not None:
                args += [t, siguiente]
                i += 2
            else:
                args.append(t)
                i += 1
        elif t.startswith("-") and len(t) > 1:
            letras = t[1:]
            ultima = letras[-1]
            toma_valor = ultima in CORTAS_CON_VALOR and siguiente is not None
            quedan = "".join(c for c in letras[:-1] if c not in CORTAS_FUERA)
            if toma_valor:
                if ultima not in CORTAS_PROHIBIDAS:
                    args += (["-" + quedan] if quedan else []) + ["-" + ultima, siguiente]
                elif quedan:
                    args.append("-" + quedan)
                i += 2
            else:
                quedan = "".join(c for c in letras if c not in CORTAS_FUERA)
                if quedan:
                    args.append("-" + quedan)
                i += 1
        else:
            if t.startswith("http"):
                args.append(t)
            i += 1
    return args if any(a.startswith("http") for a in args) else None


def ejecutar(args: list[str], timeout: float, ca: str | None) -> dict:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        ruta = tmp.name
    cmd = ["curl", "-sS", "-A", UA, "-H", "Accept-Language: es-ES,es;q=0.9", "--max-time", str(int(timeout)),
           "--max-filesize", "40000000", "-o", ruta, "-w", "%{http_code} %{size_download} %{content_type}", "--proto", "=https,http"]
    if ca:
        cmd += ["--cacert", ca]
    t0 = time.time()
    p = subprocess.run(cmd + args, capture_output=True, text=True)
    ms = int((time.time() - t0) * 1000)
    cuerpo = Path(ruta).read_bytes()[:400000]
    os.unlink(ruta)
    partes = (p.stdout or "0 0 -").split(" ", 2)
    codigo = int(partes[0]) if partes[0].isdigit() else 0
    tipo = partes[2] if len(partes) > 2 else ""
    if codigo == 0:
        return {"result": "error", "status": None, "bytes": 0, "ms": ms, "type": "", "detail": p.stderr.strip()[:160], "body": b""}
    bloqueado = any(m in cuerpo for m in BLOQUEO)
    if 200 <= codigo < 300:
        res = "blocked" if bloqueado else "ok"
    elif 300 <= codigo < 400:
        res = "redirect"
    else:
        res = "blocked" if bloqueado else "fail"
    detalle = "más de 40 MB, cortado" if p.returncode == 63 else (p.stderr.strip()[:160] if p.returncode else "")
    return {"result": res, "status": codigo, "bytes": int(float(partes[1])) if len(partes) > 1 else 0, "ms": ms, "type": tipo, "detail": detalle, "body": cuerpo}


def necesita_cookie(ejemplo: str) -> bool:
    """True si el curl lee un cookie jar (-b fichero, no -b "a=b") que no escribe él mismo con -c: depende de otro paso."""
    lee = re.search(r"(?:^|\s)(?:-b|--cookie)\s+(\S+)", ejemplo)
    return bool(lee and "=" not in lee.group(1) and not re.search(r"(?:^|\s)(?:-c|--cookie-jar)\s", ejemplo))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", action="append", default=[], help="id de ficha (repetible)")
    ap.add_argument("--report", default=None)
    ap.add_argument("--fail", action="store_true", help="código 1 si hay fail o error")
    ap.add_argument("--ca", default=os.environ.get("CA_BUNDLE"))
    ap.add_argument("--muestra", type=int, default=0, help="imprime los primeros N bytes de cada respuesta")
    ap.add_argument("--timeout", type=float, default=60)
    a = ap.parse_args()

    fuentes = [s for s in load_sources() if not a.only or s["id"] in set(a.only)]
    filas, ultimo = [], {}
    for s in fuentes:
        for e in s.get("endpoints") or []:
            if not e.get("example"):
                continue
            texto, faltan, minusculas = expandir(e["example"])
            args = argumentos(texto)
            if minusculas:
                r = {"result": "fail", "status": None, "bytes": 0, "ms": 0, "type": "", "detail": f"${minusculas[0]} sin escapar: la shell lo expandiría a vacío", "body": b""}
            elif faltan:
                r = {"result": "skipped", "status": None, "bytes": 0, "ms": 0, "type": "", "detail": f"falta la variable {', '.join(faltan)}", "body": b""}
            elif args is None:
                r = {"result": "skipped", "status": None, "bytes": 0, "ms": 0, "type": "", "detail": "no es una URL ni un curl", "body": b""}
            elif necesita_cookie(texto):
                r = {"result": "skipped", "status": None, "bytes": 0, "ms": 0, "type": "", "detail": "lee la cookie de un paso anterior (-b fichero)", "body": b""}
            else:
                host = urlparse(next(x for x in args if x.startswith("http"))).hostname or ""
                espera = 3.0 if "catastro" in host else 1.0
                if host in ultimo and time.time() - ultimo[host] < espera:
                    time.sleep(espera - (time.time() - ultimo[host]))
                r = ejecutar(args, a.timeout, a.ca)
                ultimo[host] = time.time()
            filas.append((s["id"], e["path"], r))
            print(f"{r['result']:8} {s['id']:38} {r['status'] or '-':>4} {r['bytes']:>10}B {r['ms']:>6}ms  {e['path'][:70]}  {r['detail']}")
            if a.muestra and r["body"]:
                print("    " + r["body"][: a.muestra].decode("utf-8", "replace").replace("\n", " ")[: a.muestra])
    cuentas = {k: sum(1 for *_, r in filas if r["result"] == k) for k in ("ok", "redirect", "fail", "blocked", "error", "skipped")}
    print(f"\n{len(filas)} ejemplos en {len(fuentes)} fichas: {cuentas}")
    if a.report:
        lineas = [f"# Ejemplos de las fichas · {date.today().isoformat()}", "",
                  f"{len(filas)} ejemplos en {len(fuentes)} fichas: " + ", ".join(f"{k} {v}" for k, v in cuentas.items()) + ".", "",
                  "| resultado | ficha | endpoint | código | bytes | tipo | detalle |", "|---|---|---|---|---|---|---|"]
        for sid, path, r in sorted(filas, key=lambda f: (f[2]["result"] == "ok", f[0])):
            lineas.append(f"| {r['result']} | {sid} | {path.replace('|', '/')[:80]} | {r['status'] or '—'} | {r['bytes']} | {r['type'][:40]} | {r['detail'].replace('|', '/')} |")
        Path(a.report).write_text("\n".join(lineas) + "\n", encoding="utf-8")
        print(f"informe en {a.report}")
    return 1 if a.fail and (cuentas["fail"] or cuentas["error"]) else 0


if __name__ == "__main__":
    sys.exit(main())
