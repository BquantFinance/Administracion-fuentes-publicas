"""Sesión HTTP con las reglas de guides/cliente-http.md: User-Agent de navegador y bundle FNMT si existe."""
from __future__ import annotations

import os
from pathlib import Path

import requests

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def bundle() -> str | bool:
    """CA_BUNDLE, ca-age.pem en el directorio actual o en la raíz del repo; si no, el de certifi."""
    for cand in (os.environ.get("CA_BUNDLE"), "ca-age.pem", Path(__file__).resolve().parents[2] / "ca-age.pem"):
        if cand and Path(cand).exists():
            return str(cand)
    return True


def session(accept: str = "application/json, */*;q=0.8") -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": accept, "Accept-Language": "es-ES,es;q=0.9"})
    s.verify = bundle()  # REQUESTS_CA_BUNDLE en el entorno tiene prioridad sobre esto: pasar verify= por petición si hace falta
    return s
