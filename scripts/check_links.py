#!/usr/bin/env python3
"""Comprueba que base_url, docs_url y ejemplos absolutos responden. Uso: check_links.py [--fail]

Imprime un informe Markdown. Con --fail devuelve código 1 si alguna URL no responde.
Muchos servidores públicos rechazan HEAD o user-agents genéricos: se usa GET con UA de navegador.
"""
from __future__ import annotations

import concurrent.futures as cf
import re
import sys
import urllib.error
import urllib.request

from common import load_sources

UA = "Mozilla/5.0 (compatible; fuentes-publicas-linkcheck/1.0; +https://github.com/BquantFinance/Administracion-fuentes-publicas)"
TIMEOUT = 25


def urls_of(s: dict) -> list[tuple[str, str]]:
    out = [("base_url", s["base_url"])]
    if s.get("docs_url"):
        out.append(("docs_url", s["docs_url"]))
    for e in s.get("endpoints", []) or []:
        ex = e.get("example", "")
        m = re.search(r"https?://[^\s\"']+", ex)
        if m and "{" not in m.group(0):
            out.append((f"example {e['path']}", m.group(0)))
    return out


def check(url: str) -> tuple[int | None, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, ""
    except urllib.error.HTTPError as e:
        return e.code, e.reason
    except Exception as e:  # noqa: BLE001
        return None, str(e)[:120]


def main() -> int:
    fail = "--fail" in sys.argv
    jobs = [(s["id"], kind, url) for s in load_sources() for kind, url in urls_of(s)]
    results = []
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(check, url): (sid, kind, url) for sid, kind, url in jobs}
        for f in cf.as_completed(futs):
            sid, kind, url = futs[f]
            code, msg = f.result()
            results.append((sid, kind, url, code, msg))
    results.sort()
    bad = [r for r in results if r[3] is None or r[3] >= 400]
    print(f"# Comprobación de enlaces\n\n{len(results)} URLs, {len(bad)} con problemas.\n")
    if bad:
        print("| id | campo | url | código | detalle |\n|---|---|---|---|---|")
        for sid, kind, url, code, msg in bad:
            print(f"| {sid} | {kind} | {url} | {code or 'ERR'} | {msg} |")
    return 1 if (fail and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
