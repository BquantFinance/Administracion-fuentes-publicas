"""Tablas PC-Axis (JAXI) en CSV: INE (jaxiT3 y jaxi), Educabase, CulturaBase y Criminalidad de Interior (fichas
ine-api-tempus, educacion-estadisticas-ruct, cultura-culturabase, interior-criminalidad).

Trampas que resuelve:
- El CSV llega en UTF-8 con BOM aunque Content-Type diga ISO-8859-15 (leído como Latin-1 sale «autÃ³noma»).
- Números con punto de miles y coma decimal (197.079, 926,6) y el periodo aún sin dato como "" (INE): numero().
- De la URL que se ve en el navegador (Tabla.htm?t=... o Tabla.htm?path=...&file=...) a la del fichero
  (files/.../csv_bdsc/...): url_csv(). csv_bdsc es el formato de una fila por combinación; csv_bd usa tabulador y
  csv_sc añade título.
- Los índices DynPx enlazan las tablas con &amp; escapado: tablas_de_indice() devuelve las URL ya limpias.
Ojo, sin arreglo posible aquí: el balance de criminalidad de Interior es acumulado desde enero (enero-junio), no
trimestral, y los nombres de columna cambian entre tablas (periodo, Periodo, Periodos:).

Uso: python scripts/clientes/pcaxis.py                    IPC del INE (tabla 24077), últimos periodos
     python scripts/clientes/pcaxis.py URL_O_ID [N]        primeras N filas de cualquier tabla (id del INE o URL)
     python scripts/clientes/pcaxis.py --indice URL        tablas enlazadas en un índice DynPx (Educabase, CulturaBase)
"""
from __future__ import annotations

import csv
import html
import io
import os
import re
import sys
from urllib.parse import parse_qs, urljoin, urlparse

try:
    from .sesion import Bloqueado, sesion, texto
except ImportError:
    sys.path.insert(0, os.path.dirname(__file__))
    from sesion import Bloqueado, sesion, texto

VACIOS = {"", "..", ".", "-", ":", "...", '""'}
_S = None


def _sesion():
    global _S
    if _S is None:
        _S = sesion(accept="text/csv, text/plain, */*;q=0.8")
    return _S


def url_csv(tabla: str | int, formato: str = "csv_bdsc") -> str:
    """URL del fichero a partir del id de tabla del INE (24077), de un Tabla.htm o de otra URL files/ de la tabla."""
    t = str(tabla).strip()
    if t.isdigit():
        return f"https://www.ine.es/jaxiT3/files/t/es/{formato}/{t}.csv?nocab=1"
    u = urlparse(html.unescape(t))
    q = {k: v[0] for k, v in parse_qs(u.query).items()}
    raiz = f"{u.scheme}://{u.netloc}"
    if "/files/" in u.path:  # ya es un fichero: cambiar el formato
        ruta = re.sub(r"/(csv_bdsc|csv_bd|csv_sc|csv_c|px|xlsx|xls|json)/", f"/{formato}/", u.path, count=1)
        if "/jaxiT3/" in ruta:
            ruta = re.sub(r"\.\w+$", ".px" if formato == "px" else ".xlsx" if formato == "xlsx" else ".csv", ruta)
        return f"{raiz}{ruta}?nocab=1"
    if "t" in q and "/jaxiT3/" in u.path:
        return f"https://{u.netloc}/jaxiT3/files/t/es/{formato}/{q['t']}.csv?nocab=1"
    if "path" in q and "file" in q:  # Tabla.htm o dlgExport.htm de jaxi, EducaJaxiPx, CulturaJaxiPx, sec/jaxiPx
        base = u.path.rsplit("/", 1)[0]
        return f"{raiz}{base}/files/_px/es/{formato}/{q['path'].strip('/')}/{q['file']}?nocab=1"
    raise ValueError(f"no reconozco la tabla PC-Axis en {tabla!r}")


def numero(v: str | None) -> float | int | None:
    """'197.079' -> 197079, '926,6' -> 926.6, '' o '..' -> None (sin dato o secreto estadístico, no cero)."""
    if v is None or v.strip() in VACIOS:
        return None
    s = v.strip().replace(".", "").replace(",", ".")
    n = float(s)
    return int(n) if "." not in s and n.is_integer() else n


def leer(datos: bytes | str, numeros: bool = True) -> list[dict]:
    """Filas del CSV csv_bdsc (; y una columna de valor al final, Total o el nombre de la medida)."""
    t = datos if isinstance(datos, str) else texto(datos)
    filas = list(csv.DictReader(io.StringIO(t), delimiter=";"))
    if numeros and filas:
        valor = list(filas[0])[-1]
        for f in filas:
            f[valor] = numero(f[valor])
    return filas


def tabla(tabla_o_url: str | int, numeros: bool = True) -> list[dict]:
    """Descarga y lee una tabla en csv_bdsc."""
    return leer(texto(_sesion().get(url_csv(tabla_o_url))), numeros)


def periodo_iso(p: str) -> str:
    """Periodo del INE a ISO: 2026M09 -> 2026-09, 2025T3 -> 2025-Q3, 2025S1 -> 2025-H1; el resto sin cambios."""
    m = re.fullmatch(r"(\d{4})([MTSQ])(\d{1,2})", p.strip())
    if not m:
        return p
    a, tipo, n = m.groups()
    return f"{a}-{int(n):02d}" if tipo == "M" else f"{a}-{'H' if tipo == 'S' else 'Q'}{int(n)}"


def tablas_de_indice(url: str) -> list[str]:
    """URL csv_bdsc de las tablas enlazadas en un índice DynPx (EducaDynPx, CulturaDynPx) o una página de tema."""
    r = _sesion().get(url)
    enlaces = re.findall(r'href="([^"]*Tabla\.htm\?[^"]*)"', texto(r))
    return list(dict.fromkeys(url_csv(urljoin(r.url, html.unescape(e))) for e in enlaces))


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        if args[:1] == ["--indice"]:
            for u in tablas_de_indice(args[1]):
                print(u)
        elif args:
            for f in tabla(args[0])[: int(args[1]) if len(args) > 1 else 5]:
                print(f)
        else:
            for f in tabla(24077)[:3]:  # IPC, índice general (base 2021), del periodo más reciente al más antiguo
                print(periodo_iso(f["Periodo"]), f["Total"], "(None = periodo aún sin publicar, no cero)" if f["Total"] is None else "")
    except Bloqueado as e:
        sys.exit(f"bloqueado: {e}")
