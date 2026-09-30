#!/usr/bin/env python3
"""Ejecuta las comprobaciones de indices/recetas.yaml contra los servidores reales (batería de regresión).

Uso: check_recetas.py [--only ID ...] [--report FICHERO.md] [--fail] [--ca BUNDLE] [--timeout S] [--sleep S]

Cada check hace la petición con User-Agent y Accept de navegador, lee como mucho read_bytes (65536 por defecto)
y comprueba status (200 por defecto), contains y min_bytes (Content-Length si existe, bytes leídos si no).
Resultado: ok | fail (código o contenido distinto del esperado) | blocked (WAF, filtro antibots o bloqueo por
IP reconocido en la respuesta) | error (sin respuesta). Con --fail devuelve 1 si hay fail o error; blocked
se informa pero no rompe, porque depende de la red desde la que se ejecuta.
El bundle de CA sale de --ca, de la variable CA_BUNDLE o de ca-age.pem (scripts/fnmt_bundle.py) si existe.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import date

import requests

from common import ROOT, load_indices

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
BLOCK_MARKERS = (
    "Petición HTTP bloqueada",
    "Petici&#243;n HTTP bloqueada",
    "Request Rejected",
    "The requested URL was rejected",
    "Making sure you're not a bot",
    "Making sure you&#39;re not a bot",
    "Voight-Kampff",
    "Checking you are not a bot",
    "Acceso denegado",
    "Incapsula",
    "_Incapsula_Resource",
)


def ca_bundle(arg: str | None) -> str | bool:
    for cand in (arg, os.environ.get("CA_BUNDLE"), str(ROOT / "ca-age.pem")):
        if cand and os.path.exists(cand):
            return cand
    return True


def run_check(session: requests.Session, c: dict, timeout: float, sleep: float, verify) -> dict:
    method = c.get("method", "GET")
    headers = {"User-Agent": UA, "Accept": ACCEPT, "Accept-Language": "es-ES,es;q=0.9"}
    headers.update(c.get("headers") or {})
    want_status = c.get("status", 200)
    read_bytes = c.get("read_bytes", 65536)
    attempts = c.get("retries", 0) + 1
    last: dict = {}
    for n in range(attempts):
        t0 = time.time()
        try:
            r = session.request(method, c["url"], headers=headers, timeout=timeout, stream=True, verify=verify)
            raw = b""
            if method != "HEAD":
                for chunk in r.iter_content(8192):
                    raw += chunk
                    if len(raw) >= read_bytes:
                        break
            r.close()
            length = r.headers.get("Content-Length")
            size = int(length) if length and length.isdigit() else len(raw)
            text_utf8 = raw.decode("utf-8", "replace")
            text_lat1 = raw.decode("latin-1")
            blocked = any(m in text_utf8 for m in BLOCK_MARKERS)
            reasons = []
            if r.status_code != want_status:
                reasons.append(f"status {r.status_code}, esperado {want_status}")
            if c.get("contains") and c["contains"] not in text_utf8 and c["contains"] not in text_lat1:
                reasons.append(f"no contiene {c['contains']!r}")
            if c.get("min_bytes") and size < c["min_bytes"]:
                reasons.append(f"{size} bytes, esperados >= {c['min_bytes']}")
            result = "ok" if not reasons else ("blocked" if blocked else "fail")
            last = {"result": result, "status": r.status_code, "bytes": size, "ms": int((time.time() - t0) * 1000),
                    "detail": "; ".join(reasons), "attempt": n + 1}
        except requests.RequestException as exc:
            last = {"result": "error", "status": None, "bytes": 0, "ms": int((time.time() - t0) * 1000),
                    "detail": f"{type(exc).__name__}: {str(exc)[:160]}", "attempt": n + 1}
        if last["result"] == "ok":
            break
        if n + 1 < attempts:
            time.sleep(sleep)
    return last


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", action="append", default=[], help="id de receta (repetible)")
    ap.add_argument("--report", default=None, help="fichero Markdown de salida")
    ap.add_argument("--fail", action="store_true", help="código 1 si hay fail o error")
    ap.add_argument("--ca", default=None, help="bundle de CA (por defecto CA_BUNDLE o ca-age.pem)")
    ap.add_argument("--timeout", type=float, default=45.0)
    ap.add_argument("--sleep", type=float, default=4.0, help="espera entre reintentos (s)")
    args = ap.parse_args()

    recetas = load_indices()["recetas"]
    if args.only:
        recetas = [r for r in recetas if r["id"] in set(args.only)]
    verify = ca_bundle(args.ca)
    session = requests.Session()
    rows: list[tuple[str, dict, dict]] = []
    for r in recetas:
        for c in r["checks"]:
            res = run_check(session, c, args.timeout, args.sleep, verify)
            rows.append((r["id"], c, res))
            print(f"{res['result']:7} {r['id']:36} {res['status'] or '-':>4} {res['bytes']:>9}B {res['ms']:>6}ms  {c['url'][:90]}  {res['detail']}")
            time.sleep(0.5)

    counts = {k: sum(1 for _, _, res in rows if res["result"] == k) for k in ("ok", "fail", "blocked", "error")}
    print(f"\n{len(rows)} comprobaciones en {len(recetas)} recetas: {counts}")
    if args.report:
        lines = [
            f"# Comprobación de recetas · {date.today().isoformat()}",
            "",
            f"{len(rows)} comprobaciones en {len(recetas)} recetas: ok {counts['ok']}, fail {counts['fail']}, blocked {counts['blocked']}, error {counts['error']}.",
            "",
            "| receta | resultado | código | bytes | ms | url | detalle |",
            "|---|---|---|---|---|---|---|",
        ]
        for rid, c, res in rows:
            lines.append(f"| {rid} | {res['result']} | {res['status'] or '-'} | {res['bytes']} | {res['ms']} | {c['url']} | {res['detail']} |")
        with open(args.report, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"informe en {args.report}")
    if args.fail and (counts["fail"] or counts["error"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
