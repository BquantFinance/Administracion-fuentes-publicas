#!/usr/bin/env python3
"""Servidor MCP mínimo (stdio) que expone catalog.json por herramientas.

Un agente carga solo lo que necesita (una ficha, una receta, una necesidad) en vez de todo llms.txt.
Arranque: python scripts/mcp_catalogo.py. Requiere catalog.json generado con python scripts/build.py.
Prueba real: python scripts/test_mcp_catalogo.py.
"""
import difflib
import json
import re
import sys
import unicodedata

from common import ROOT

try:
    from mcp.server.mcpserver import MCPServer as FastMCP  # mcp 2.x
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP

CATALOG_PATH = ROOT / "catalog.json"
LLMS_PATH = ROOT / "llms.txt"
STOPWORDS = {
    "a", "al", "con", "de", "del", "el", "en", "es", "la", "las", "lo", "los", "o", "para", "por", "que",
    "se", "sin", "su", "sus", "un", "una", "y",
}
INSTRUCTIONS = (
    "Catálogo de fuentes de datos de la Administración pública española. Flujo: necesidad o buscar_fuentes "
    "para localizar la fuente, ficha para endpoints, quirks y gotchas verificados; buscar_recetas y receta para "
    "procedimientos que cruzan fuentes; identificador para cruzar datos; ruta_muerta antes de dar por perdida "
    "una URL. Lee el recurso catalogo://reglas antes de programar contra una fuente."
)


def load_catalog() -> dict:
    if not CATALOG_PATH.exists():
        sys.exit(f"ERROR: no existe {CATALOG_PATH}; genéralo con: python scripts/build.py")
    with CATALOG_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


CATALOG = load_catalog()
SOURCES = CATALOG["sources"]
BY_ID = {s["id"]: s for s in SOURCES}
IDX = CATALOG["indices"]
RECETAS = IDX["recetas"]
RECETA_BY_ID = {r["id"]: r for r in RECETAS}
NECESIDADES = IDX["necesidades"]
IDENTIFICADORES = IDX["identificadores"]
RUTAS_MUERTAS = IDX["rutas_muertas"]
CODIGOS = IDX.get("codigos") or {}
SECTORES = CATALOG["sectors"]


def norm(value) -> str:
    """Minúsculas sin acentos; listas y dicts se aplanan a texto."""
    if isinstance(value, (list, tuple)):
        return " ".join(norm(v) for v in value)
    if isinstance(value, dict):
        return norm(list(value.values()))
    text = unicodedata.normalize("NFKD", str(value or ""))
    return "".join(c for c in text if not unicodedata.combining(c)).lower()


def tokens(query: str) -> list[str]:
    return [t for t in re.split(r"[^a-z0-9]+", norm(query)) if len(t) > 1 and t not in STOPWORDS]


def variants(token: str) -> list[str]:
    """El token y sus prefijos cortos, para que gasolina case con gasolinera y municipios con municipio."""
    out = [token]
    if len(token) >= 5:
        out.append(token[:-1])
    if len(token) >= 7:
        out.append(token[:-2])
    return out


def score(query: str, strong: str, weak: str) -> tuple[int, int]:
    """(tokens que casan, puntuación); id/name/tags pesan 3, el resto 1."""
    matched = points = 0
    for tok in tokens(query):
        vs = variants(tok)
        if any(v in strong for v in vs):
            matched += 1
            points += 3
        elif any(v in weak for v in vs):
            matched += 1
            points += 1
    return matched, points


def rank(query: str, items: list, fields, limite: int) -> list:
    """Ordena items por (tokens casados, puntuación); fields(item) devuelve (strong, weak) ya normalizados."""
    scored = []
    for item in items:
        matched, points = score(query, *fields(item))
        if matched:
            scored.append((-matched, -points, item))
    scored.sort(key=lambda t: t[:2])
    return [item for _, _, item in scored[: max(1, min(limite, 50))]]


def parecidos(key: str, keys, n: int = 5) -> list[str]:
    """Ids parecidos: primero los que comparten trozos del id (ine, tempus), después por similitud de texto."""
    wanted = norm(key)
    parts = [p for p in re.split(r"[^a-z0-9]+", wanted) if len(p) > 2]
    scored = []
    for k in keys:
        segments = re.split(r"[^a-z0-9]+", norm(k))
        hits = sum(any(seg.startswith(p) for seg in segments) for p in parts)
        ratio = difflib.SequenceMatcher(None, wanted, k).ratio()
        if hits or ratio >= 0.5:
            scored.append((-hits, -ratio, k))
    return [k for _, _, k in sorted(scored)[:n]]


SOURCE_FIELDS = {
    s["id"]: (
        norm([s["id"], s["name"], s.get("tags"), s["sector"], SECTORES.get(s["sector"])]),
        norm([s["summary"], s["org"], s.get("ministry"), s.get("ids")]),
    )
    for s in SOURCES
}
RECETA_FIELDS = {
    r["id"]: (
        norm([r["id"], r["intent"], [st["source"] for st in r["steps"]]]),
        norm([r.get("inputs"), [st["do"] for st in r["steps"]], r["output"], r.get("note")]),
    )
    for r in RECETAS
}

mcp = FastMCP("catalogo-fuentes-publicas", instructions=INSTRUCTIONS)


@mcp.tool()
def buscar_fuentes(consulta: str, sector: str | None = None, limite: int = 8) -> list[dict]:
    """Busca fichas por palabras (id, nombre, etiquetas, sector, resumen, organismo). Devuelve id, name, sector, access, auth, status, verified y summary; después pide la ficha completa con ficha(id)."""
    items = SOURCES
    if sector:
        if sector not in SECTORES:
            raise ValueError(f"sector desconocido: {sector}; válidos: {', '.join(SECTORES)}")
        items = [s for s in SOURCES if s["sector"] == sector]
    hits = rank(consulta, items, lambda s: SOURCE_FIELDS[s["id"]], limite)
    return [
        {k: s.get(k) for k in ("id", "name", "sector", "access", "auth", "status", "verified", "summary")}
        for s in hits
    ]


@mcp.tool()
def ficha(id: str) -> dict:
    """Ficha completa de una fuente (endpoints con ejemplo, quirks, ids, gotchas, tips, related). Si el id no existe, devuelve hasta 5 ids parecidos."""
    if id in BY_ID:
        return BY_ID[id]
    return {"error": f"no existe la ficha {id}", "sugerencias": parecidos(id, BY_ID)}


@mcp.tool()
def buscar_recetas(consulta: str, limite: int = 5) -> list[dict]:
    """Busca recetas por intención (procedimientos verificados que encadenan fichas). Devuelve id, intent, sources y verified; los pasos se piden con receta(id)."""
    hits = rank(consulta, RECETAS, lambda r: RECETA_FIELDS[r["id"]], limite)
    return [
        {
            "id": r["id"],
            "intent": r["intent"],
            "sources": list(dict.fromkeys(st["source"] for st in r["steps"])),
            "verified": r.get("verified"),
        }
        for r in hits
    ]


@mcp.tool()
def receta(id: str) -> dict:
    """Receta completa: intent, inputs, steps (source, do, example), output, note y verified. Si el id no existe, devuelve ids parecidos."""
    if id in RECETA_BY_ID:
        return {k: v for k, v in RECETA_BY_ID[id].items() if k != "checks"}
    return {"error": f"no existe la receta {id}", "sugerencias": parecidos(id, RECETA_BY_ID)}


@mcp.tool()
def necesidad(consulta: str, limite: int = 5) -> list[dict]:
    """Dónde está cada cosa: necesidades habituales con la ficha que las resuelve y la nota que evita el desvío típico. source null significa que no hay fuente en el catálogo."""
    hits = rank(consulta, NECESIDADES, lambda n: (norm(n["need"]), norm([n.get("source"), n.get("note")])), limite)
    return [{"need": n["need"], "source": n.get("source"), "note": n.get("note")} for n in hits]


@mcp.tool()
def identificador(id: str) -> dict:
    """Entrada del índice de identificadores (ine-municipio, nif, dir3, cpv, boe-id...): format, regex, example, issuer, gotcha, joins y used_by. Si no existe, devuelve claves parecidas."""
    if id in IDENTIFICADORES:
        return {"id": id, **IDENTIFICADORES[id]}
    return {"error": f"no existe el identificador {id}", "sugerencias": parecidos(id, IDENTIFICADORES)}


@mcp.tool()
def ruta_muerta(url: str) -> dict:
    """Comprueba si una URL figura en rutas muertas, exacta o por prefijo en ambos sentidos. Devuelve old, status, new (sustituta o null), source, note y checked."""
    wanted = url.strip().rstrip("/")
    exact = [d for d in RUTAS_MUERTAS if d["old"].rstrip("/") == wanted]
    prefix = [
        d for d in RUTAS_MUERTAS
        if d not in exact and (d["old"].rstrip("/").startswith(wanted) or wanted.startswith(d["old"].rstrip("/")))
    ]
    rutas = [
        {k: d.get(k) for k in ("old", "status", "new", "source", "note", "checked")}
        for d in exact + prefix
    ]
    if not rutas:
        return {"url": url, "rutas": [], "nota": f"no figura en rutas-muertas ({len(RUTAS_MUERTAS)} entradas); no implica que funcione"}
    return {"url": url, "rutas": rutas}


@mcp.tool()
def codigos(grupo: str | None = None) -> dict | list[dict]:
    """Códigos que una API exige como parámetro y no se adivinan (Id de municipio y provincia del INE para tv, países de DataComex, estación de AEMET por capital, productos de carburantes, rangos del BOE). Sin grupo, lista los grupos con fuente y uso; con grupo, sus entradas {code, name, note}."""
    if grupo is None:
        return [
            {"grupo": k, "source": g["source"], "use": g["use"], "entries": len(g["entries"]), "verified": g["verified"]}
            for k, g in CODIGOS.items()
        ]
    if grupo in CODIGOS:
        return CODIGOS[grupo]
    return {"error": f"no existe el grupo {grupo}", "sugerencias": parecidos(grupo, CODIGOS)}


@mcp.tool()
def sectores() -> list[dict]:
    """Sectores del catálogo con su título y número de fichas; el id sirve como filtro en buscar_fuentes."""
    counts = {}
    for s in SOURCES:
        counts[s["sector"]] = counts.get(s["sector"], 0) + 1
    return [{"id": k, "name": v, "sources": counts.get(k, 0)} for k, v in SECTORES.items()]


def read_llms() -> str:
    if not LLMS_PATH.exists():
        return f"no existe {LLMS_PATH}; genéralo con: python scripts/build.py"
    return LLMS_PATH.read_text(encoding="utf-8")


@mcp.resource("catalogo://llms.txt", mime_type="text/plain")
def llms_txt() -> str:
    """llms.txt completo: reglas, dónde está cada cosa, recetas y sectores."""
    return read_llms()


@mcp.resource("catalogo://reglas", mime_type="text/plain")
def reglas() -> str:
    """Reglas rápidas antes de programar contra una fuente (sección de llms.txt)."""
    text = read_llms()
    m = re.search(r"^## Reglas rápidas.*?(?=^## )", text, flags=re.S | re.M)
    return m.group(0).strip() if m else "sección de reglas no encontrada en llms.txt"


if __name__ == "__main__":
    mcp.run(transport="stdio")
