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


class LimiteAemet(RuntimeError):
    """Límite de peticiones por minuto (estado 429); se libera al minuto siguiente."""


def url_datos(status: int, contenido: bytes) -> str:
    """URL del fichero de datos a partir de la respuesta intermedia, sin fiarse de Content-Type (el 401 llega como text/plain con JSON).

    Sin cabecera api_key: 200 con cuerpo vacío. Clave inválida: 401 con JSON. Errores de datos y límite por minuto:
    estado 404 o 429 dentro del JSON, a veces con HTTP 200.
    """
    if not contenido.strip():
        raise PermissionError("AEMET: cuerpo vacío; falta la cabecera api_key")
    texto = contenido.decode("utf-8", "replace")
    try:
        meta = json.loads(texto)
    except ValueError:
        raise RuntimeError(f"AEMET {status}: {texto[:120]}") from None
    estado = meta.get("estado", status)
    if 429 in (estado, status):
        raise LimiteAemet(f"AEMET 429: {meta.get('descripcion')}")
    if estado != 200 or "datos" not in meta:
        raise RuntimeError(f"AEMET {estado}: {meta.get('descripcion')}")
    return meta["datos"]


def leer_datos(contenido: bytes):
    """Los ficheros de datos son JSON en ISO-8859-15; decodificados como UTF-8 las tildes salen mal o fallan."""
    return json.loads(contenido.decode("iso-8859-15"))


def get(path: str, key: str | None = None, retries: int = 2, verify=None):
    """JSON del fichero de datos de un endpoint (lista o dict): primera petición con api_key, segunda a la URL datos.
    Ante el límite por minuto espera 62 s y reintenta."""
    key = key or os.environ["AEMET_KEY"]
    s = session()
    verify = verify if verify is not None else s.verify
    for intento in range(retries + 1):
        r = s.get(f"{BASE}{path}", headers={"api_key": key}, timeout=60, verify=verify)
        try:
            url = url_datos(r.status_code, r.content)
        except LimiteAemet:
            if intento == retries:
                raise
            time.sleep(62)
            continue
        return leer_datos(s.get(url, timeout=60, verify=verify).content)
    raise RuntimeError("AEMET: sin respuesta")


def dias(prediccion: list) -> list[dict]:
    """Días de la predicción diaria (fecha, temperatura.maxima/minima, probPrecipitacion[])."""
    return prediccion[0]["prediccion"]["dia"]


def prediccion_diaria(municipio_ine: str, key: str | None = None) -> list[dict]:
    """Predicción diaria para un municipio INE de 5 dígitos."""
    return dias(get(f"/prediccion/especifica/municipio/diaria/{municipio_ine}", key))


if __name__ == "__main__":
    for d in prediccion_diaria(sys.argv[1] if len(sys.argv) > 1 else "28079")[:3]:
        print(d["fecha"][:10], d["temperatura"]["maxima"], d["temperatura"]["minima"], d["probPrecipitacion"][0]["value"])
