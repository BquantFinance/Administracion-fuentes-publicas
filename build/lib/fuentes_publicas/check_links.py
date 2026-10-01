#!/usr/bin/env python3
"""Comprueba que base_url, docs_url y ejemplos absolutos responden. Uso: check_links.py [--fail] [--ca BUNDLE]

Imprime un informe Markdown. Con --fail devuelve código 1 si alguna URL no responde.
Peticiones GET con User-Agent y Accept de navegador; los ejemplos con POST (curl -X POST, -d, --data) no se
comprueban y se listan aparte. El bundle de CA sale de --ca, de CA_BUNDLE o de ca-age.pem (scripts/fnmt_bundle.py)
si existe, porque muchos servidores públicos no envían la cadena intermedia de FNMT.
Una raíz de API (base_url de una ficha con acceso api-rest o api-soap) que responde 400, 404 o 405 cuenta como
respuesta esperada, no como problema.
"""
from __future__ import annotations

import concurrent.futures as cf
import os
import re
import sys

import requests

from common import ROOT, load_sources

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
HEADERS = {"User-Agent": UA, "Accept": "application/json, text/html;q=0.9, */*;q=0.8", "Accept-Language": "es-ES,es;q=0.9"}
TIMEOUT = 25
POST_RE = re.compile(r"-X\s*POST|(?:^|\s)(?:-d|--data|--data-urlencode)\s")
API_ROOT_OK = {400, 404, 405}


def ca_bundle(argv: list[str]):
    if "--ca" in argv:
        return argv[argv.index("--ca") + 1]
    env = os.environ.get("CA_BUNDLE")
    if env:
        return env
    default = ROOT / "ca-age.pem"
    return str(default) if default.exists() else True


def urls_of(s: dict) -> list[tuple[str, str, bool]]:
    api = bool({"api-rest", "api-soap"} & set(s.get("access") or []))
    out = [("base_url", s["base_url"], api)]
    if s.get("docs_url"):
        out.append(("docs_url", s["docs_url"], False))
    for e in s.get("endpoints", []) or []:
        ex = e.get("example", "")
        m = re.search(r"https?://[^\s\"']+", ex)
        if m and "{" not in m.group(0):
            kind = "post" if POST_RE.search(ex) else "example"
            out.append((f"{kind} {e['path']}", m.group(0), False))
    return out


def check(url: str, verify) -> tuple[int | None, str]:
    try:
        with requests.get(url, headers=HEADERS, timeout=TIMEOUT, verify=verify, stream=True) as r:
            return r.status_code, "" if r.ok else (r.reason or "")
    except requests.RequestException as e:  # noqa: BLE001
        return None, str(e)[:120]


def main() -> int:
    fail = "--fail" in sys.argv
    verify = ca_bundle(sys.argv)
    jobs = [(s["id"], kind, url, api) for s in load_sources() for kind, url, api in urls_of(s)]
    skipped = [(sid, kind, url) for sid, kind, url, _ in jobs if kind.startswith("post ")]
    jobs = [j for j in jobs if not j[1].startswith("post ")]
    results = []
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(check, url, verify): (sid, kind, url, api) for sid, kind, url, api in jobs}
        for f in cf.as_completed(futs):
            sid, kind, url, api = futs[f]
            code, msg = f.result()
            results.append((sid, kind, url, code, msg, api))
    results.sort()
    bad = [r for r in results if r[3] is None or (r[3] >= 400 and not (r[5] and r[1] == "base_url" and r[3] in API_ROOT_OK))]
    print(f"# Comprobación de enlaces\n\n{len(results)} URLs, {len(bad)} con problemas; {len(skipped)} ejemplos POST sin comprobar.\n")
    if bad:
        print("| id | campo | url | código | detalle |\n|---|---|---|---|---|")
        for sid, kind, url, code, msg, _ in bad:
            print(f"| {sid} | {kind} | {url} | {code or 'ERR'} | {msg} |")
    if skipped:
        print("\nEjemplos POST (no comprobados): " + ", ".join(f"{sid} ({url})" for sid, _, url in skipped))
    return 1 if (fail and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
