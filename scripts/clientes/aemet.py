"""AEMET OpenData: dos pasos, ficheros en ISO-8859-15, errores con HTTP 200 y 429 por minuto (ficha aemet-opendata).

Uso: AEMET_KEY=... python scripts/clientes/aemet.py 16078
"""
from __future__ import annotations

import json
import os
import sys
import time

try:
    from ._http import session
except ImportError:  # ejecutado por ruta
    sys.path.insert(0, os.path.dirname(__file__))
    from _http import session

BASE = "https://opendata.aemet.es/opendata/api"


def get(path: str, key: str | None = None, retries: int = 2, verify=None):
    """Devuelve el JSON del fichero de datos de un endpoint de AEMET (lista o dict).

    Trampas que resuelve: la clave va en la cabecera api_key; la primera respuesta es un JSON con estado y la URL
    datos; los errores llegan con HTTP 200 y estado 404 o 429 en el cuerpo; el fichero va en ISO-8859-15.
    """
    key = key or os.environ["AEMET_KEY"]
    s = session()
    verify = verify if verify is not None else s.verify
    for intento in range(retries + 1):
        r = s.get(f"{BASE}{path}", headers={"api_key": key}, timeout=60, verify=verify)
        meta = r.json() if r.headers.get("Content-Type", "").startswith("application/json") else {"estado": r.status_code}
        if meta.get("estado") == 429 or r.status_code == 429:
            if intento == retries:
                raise RuntimeError("AEMET: límite de peticiones por minuto; esperar un minuto")
            time.sleep(62)
            continue
        if meta.get("estado") != 200:
            raise RuntimeError(f"AEMET {meta.get('estado')}: {meta.get('descripcion')} ({path})")
        datos = s.get(meta["datos"], timeout=60, verify=verify)
        return json.loads(datos.content.decode("iso-8859-15"))
    raise RuntimeError("AEMET: sin respuesta")


def prediccion_diaria(municipio_ine: str, key: str | None = None) -> list[dict]:
    """Lista de días (fecha, temperatura.maxima/minima, probPrecipitacion[]) para un municipio INE de 5 dígitos."""
    return get(f"/prediccion/especifica/municipio/diaria/{municipio_ine}", key)[0]["prediccion"]["dia"]


if __name__ == "__main__":
    dias = prediccion_diaria(sys.argv[1] if len(sys.argv) > 1 else "28079")
    for d in dias[:3]:
        print(d["fecha"][:10], d["temperatura"]["maxima"], d["temperatura"]["minima"], d["probPrecipitacion"][0]["value"])
