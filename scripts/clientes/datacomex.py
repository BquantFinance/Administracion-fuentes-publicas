"""DataComex: sesión con token prefijado, códigos numéricos de país y números con coma (ficha datacomex).

Uso: DATACOMEX_USER=... DATACOMEX_PASS=... python scripts/clientes/datacomex.py E LastM 003 1001 28
"""
from __future__ import annotations

import os
import sys

try:
    from ._http import session
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    from _http import session

BASE = "https://comercio.serviciosmin.gob.es/DatacomexAPI"


def token(usuario: str | None = None, password: str | None = None) -> str:
    """POST IniciarSesion con JSON {Usuario, Pass}; la respuesta es la cadena "token:<JWT>" entrecomillada."""
    s = session()
    r = s.post(f"{BASE}/IniciarSesion", json={"Usuario": usuario or os.environ["DATACOMEX_USER"], "Pass": password or os.environ["DATACOMEX_PASS"]}, timeout=60, verify=s.verify)
    if r.status_code != 200:  # credenciales malas: 403 con texto plano
        raise RuntimeError(f"DataComex login {r.status_code}: {r.text[:120]}")
    return limpiar_token(r.text)


def limpiar_token(texto: str) -> str:
    """La respuesta de IniciarSesion es la cadena entrecomillada "token:<JWT>"; el Bearer es solo el JWT."""
    return texto.strip().strip('"').split("token:", 1)[-1]


def numero(texto: str) -> float:
    """euros y kilos llegan como texto con coma decimal."""
    return float(texto.replace(".", "").replace(",", "."))


def obtener_datos(f: str, pe: str, pa: str, ta: str, pr: str, tok: str | None = None) -> list[dict]:
    """f E|I, pe AAAA|AAAAMM|LastM|LastY|ALL (sensible a mayúsculas), pa país de 3 dígitos o ALL, ta TARIC o ALL, pr INE o ALL."""
    s = session()
    r = s.get(f"{BASE}/ObtenerDatos", params={"f": f, "pe": pe, "pa": pa, "ta": ta, "pr": pr}, headers={"Authorization": f"Bearer {tok or token()}"}, timeout=120, verify=s.verify)
    if r.status_code != 200:  # sin token o caducado: 401 con JSON {"Message": ...}
        raise RuntimeError(f"DataComex {r.status_code}: {r.text[:120]}")
    return filas(r.json())


def filas(o: dict) -> list[dict]:
    """Filas de ObtenerDatos con euros_num y kilos_num ya convertidos desde texto con coma decimal."""
    out = o.get("Resultados", [])
    for fila in out:
        fila["euros_num"], fila["kilos_num"] = numero(fila["euros"]), numero(fila["kilos"])
    return out


def catalogo(nombre: str) -> list[dict]:
    """ObtenerPaises, ObtenerPeriodos, ObtenerProvincias, ObtenerFlujos u ObtenerTarics (7,5 MB); sin token."""
    s = session()
    return s.get(f"{BASE}/{nombre}", timeout=300, verify=s.verify).json()


if __name__ == "__main__":
    args = sys.argv[1:] or ["E", "LastM", "003", "1001", "28"]
    for fila in obtener_datos(*args):
        print(fila["periodo"], fila["pais"], fila["prov"], fila["taric"], fila["euros_num"], "EUR", fila["kilos_num"], "kg", fila["mensaje"])
