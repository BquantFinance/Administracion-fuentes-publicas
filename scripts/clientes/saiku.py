"""Portal estadístico de violencia de género (Saiku): cookie, consulta MDX y exportación (ficha igualdad-estadisticas-violencia-genero).

Uso: python scripts/clientes/saiku.py
"""
from __future__ import annotations

import os
import sys

try:
    from ._http import session
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    from _http import session

BASE = "https://estadisticasviolenciagenero.igualdad.gob.es/saiku/rest/saiku/anonymous"
CATALOGO = "VDG_CIUDADANO_PRO"


class Saiku:
    def __init__(self):
        self.s = session()
        self.s.get(f"{BASE}/discover", timeout=60, verify=self.s.verify)  # fija la cookie; sin ella la primera consulta se pierde

    def cubos(self) -> list[str]:
        o = self.s.get(f"{BASE}/discover", timeout=60, verify=self.s.verify).json()
        return [c["name"] for con in o for cat in con.get("catalogs", []) for sch in cat.get("schemas", []) for c in sch.get("cubes", [])]

    def metadata(self, cubo: str) -> dict:
        return self.s.get(f"{BASE}/discover/xmla/{CATALOGO}/null/{cubo}/metadata", timeout=60, verify=self.s.verify).json()

    def consulta(self, cubo: str, mdx: str, nombre: str = "q1") -> list[list]:
        """Crea la consulta en la sesión y ejecuta el MDX; devuelve el cellset como filas de valores (cabecera primero)."""
        for intento in range(2):
            self.s.post(f"{BASE}/query/{nombre}", data={"connection": "xmla", "cube": cubo, "catalog": CATALOGO, "schema": "", "type": "MDX"}, timeout=60, verify=self.s.verify)
            o = self.s.post(f"{BASE}/query/{nombre}/result/flattened", data={"mdx": mdx}, timeout=120, verify=self.s.verify).json()
            if o.get("cellset"):
                return [[c.get("value") for c in fila] for fila in o["cellset"]]
        raise RuntimeError(f"Saiku: {o.get('error')}")

    def csv(self, nombre: str = "q1") -> bytes:
        return self.s.get(f"{BASE}/query/{nombre}/export/csv", timeout=120, verify=self.s.verify).content


if __name__ == "__main__":
    sk = Saiku()
    filas = sk.consulta("040 Servicio 016", "SELECT NON EMPTY {[Measures].[Llamadas pertinentes]} ON COLUMNS, NON EMPTY {[02 Estructura temporal - Año].[Año].[Año].Members} ON ROWS FROM [040 Servicio 016]")
    for fila in filas[-4:]:
        print(fila)
