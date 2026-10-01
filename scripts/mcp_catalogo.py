#!/usr/bin/env python3
"""Servidor MCP mínimo (stdio) que expone catalog.json por herramientas.

Un agente carga solo lo que necesita (una ficha, una receta, una necesidad) en vez de todo llms.txt.
Arranque: python scripts/mcp_catalogo.py (desde el repo) o mcp-catalogo tras instalarlo con pip o uvx; si no hay catalog.json local lo descarga de GitHub y lo cachea en ~/.cache/fuentes-publicas.
Prueba real: python scripts/test_mcp_catalogo.py.
"""
import csv
import difflib
import json
import re
import sys
import os
import unicodedata
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

try:
    from .common import REPO_RAW, ROOT  # instalado como paquete (pip, uvx)
except ImportError:
    from common import REPO_RAW, ROOT  # ejecutado como script desde el repo

try:
    from mcp.server.mcpserver import MCPServer as FastMCP  # mcp 2.x
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP

CACHE_DIR = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "fuentes-publicas"


def locate(name: str) -> Path:
    """catalog.json, llms.txt o datos/municipios.csv: variable CATALOGO_DIR, directorio actual, raíz del repo o copia descargada de GitHub."""
    candidates = [Path(os.environ["CATALOGO_DIR"]) / name] if os.environ.get("CATALOGO_DIR") else []
    candidates += [Path.cwd() / name, ROOT / name]
    for c in candidates:
        if c.exists():
            return c
    cached = CACHE_DIR / name
    try:
        cached.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(f"{REPO_RAW}/{name}", headers={"User-Agent": "fuentes-publicas-mcp"})
        with urllib.request.urlopen(req, timeout=30) as r, cached.open("wb") as fh:
            fh.write(r.read())
    except Exception as exc:  # noqa: BLE001
        if not cached.exists():
            sys.exit(f"ERROR: no hay {name} local (CATALOGO_DIR, directorio actual o raíz del repo) y no se pudo descargar de {REPO_RAW}: {exc}")
    return cached


CATALOG_PATH = locate("catalog.json")
LLMS_PATH = ROOT / "llms.txt"
STOPWORDS = {
    "a", "al", "con", "de", "del", "el", "en", "es", "la", "las", "lo", "los", "o", "para", "por", "que",
    "se", "sin", "su", "sus", "un", "una", "y",
}
INSTRUCTIONS = (
    "Catálogo de fuentes de datos de la Administración pública española. Flujo: necesidad o buscar_fuentes "
    "para localizar la fuente, ficha para endpoints, quirks y gotchas verificados (alerts primero: trampas silenciosas "
    "que cambian la cifra sin dar error); buscar_recetas y receta para "
    "procedimientos que cruzan fuentes; identificador para cruzar datos; municipio para los códigos INE, SIGPAC o "
    "Catastro, DIR3, NUTS3 y coordenadas de un municipio; descargar, tabla_pcaxis, boe_sumario, subvenciones_nif, "
    "empresa_nif, ckan_buscar, ckan_filas y socrata_filas traen los datos ya resueltos (certificados, codificación, paginación); ruta_muerta antes de dar por perdida "
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

def _hosts(s: dict) -> set[str]:
    urls = [s.get("base_url") or ""] + [e["path"] for e in s.get("endpoints") or [] if e["path"].startswith("http")]
    hosts = set()
    for u in urls:
        try:
            hosts.add(urlparse(u).hostname)
        except ValueError:  # puerto o host con marcador {..}
            pass
    return {h for h in hosts if h and "{" not in h}


FICHAS_POR_HOST: dict[str, list[str]] = {}
for _s in SOURCES:
    for _h in _hosts(_s):
        FICHAS_POR_HOST.setdefault(_h, []).append(_s["id"])

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
    """Busca fichas por palabras (id, nombre, etiquetas, sector, resumen, organismo). Devuelve id, name, sector, access, auth, status, verified, summary y, si las hay, alerts (trampas silenciosas); después pide la ficha completa con ficha(id)."""
    items = SOURCES
    if sector:
        if sector not in SECTORES:
            raise ValueError(f"sector desconocido: {sector}; válidos: {', '.join(SECTORES)}")
        items = [s for s in SOURCES if s["sector"] == sector]
    hits = rank(consulta, items, lambda s: SOURCE_FIELDS[s["id"]], limite)
    return [
        {**{k: s.get(k) for k in ("id", "name", "sector", "access", "auth", "status", "verified", "summary")},
         **({"alerts": s["alerts"]} if s.get("alerts") else {})}
        for s in hits
    ]


@mcp.tool()
def ficha(id: str) -> dict:
    """Ficha completa de una fuente (alerts primero, endpoints con ejemplo, quirks, ids, gotchas, tips, related). Si el id no existe, devuelve hasta 5 ids parecidos."""
    if id in BY_ID:
        s = BY_ID[id]
        return {"alerts": s["alerts"], **s} if s.get("alerts") else s
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


_MUNICIPIOS: list[dict] = []


def municipios() -> list[dict]:
    """datos/municipios.csv, cargado la primera vez que se pide (lo descarga si no hay copia local)."""
    if not _MUNICIPIOS:
        with locate("datos/municipios.csv").open(encoding="utf-8", newline="") as fh:
            _MUNICIPIOS.extend(csv.DictReader(fh))
    return _MUNICIPIOS


@mcp.tool()
def municipio(consulta: str, limite: int = 5) -> list[dict]:
    """Códigos de un municipio en cada sistema: INE (5 dígitos y dígito de control), SIGPAC y Catastro (las capitales
    son 900: Madrid 28:900, no 28079), DIR3 y NIF del ayuntamiento, CCAA, provincia, NUTS3, Id del INE Tempus (el
    que exige tv=19:Id) y coordenadas de su núcleo capital. Acepta código INE (28079 o 280796), SIGPAC (28:900), DIR3 (L01280796), NIF (P2807900B) o nombre."""
    return _consulta().buscar_municipio(consulta, limite, municipios())


def _consulta():
    """Capa de datos (scripts/clientes/consulta.py), importada al primer uso para no frenar el arranque."""
    try:
        from .clientes import consulta  # instalado como paquete
    except ImportError:
        from clientes import consulta  # desde el repo
    return consulta


def _datos(fn, *args, **kwargs) -> dict:
    """Ejecuta una consulta de datos y convierte los fallos en un error legible para el agente."""
    try:
        return fn(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001
        tipo, texto = type(exc).__name__, str(exc)
        if tipo == "Bloqueado":
            pista = "el servidor bloquea esta red (WAF o IP de centro de datos); probar desde otra red"
        elif "CERTIFICATE_VERIFY_FAILED" in texto:
            pista = ("certificado no verificado: tras un proxy que intercepta TLS, pasar al servidor MCP la variable "
                     "EXTRA_CA_BUNDLE o REQUESTS_CA_BUNDLE con la CA del proxy (en env de la configuración del cliente)")
        elif tipo in ("ConnectionError", "ReadTimeout", "ConnectTimeout"):
            pista = "sin respuesta del servidor tras varios reintentos; puede rechazar IP de centros de datos"
        else:
            pista = "revisar parámetros con ficha() de la fuente"
        return {"error": f"{tipo}: {str(exc)[:400]}", "pista": pista}


@mcp.tool()
def descargar(url: str, max_caracteres: int = 20000, desde: int = 0) -> dict:
    """Descarga una URL pública con las reglas del catálogo (CA de FNMT, User-Agent de navegador, reintentos, gzip sin
    anunciar, UTF-8 o Latin-1 reales) y la resume: columnas y primeras filas de un CSV, claves de un JSON, hojas de un
    xlsx, ficheros de un ZIP. Detecta páginas de bloqueo de WAF. Si el host es de una ficha, añade su id y sus alerts.
    Úsala cuando el fetch propio falle con un .gob.es o para ver qué devuelve una URL antes de programar."""
    r = _datos(_consulta().descargar, url, max_caracteres, desde)
    host = urlparse(r.get("url") or url).hostname or ""
    ids = FICHAS_POR_HOST.get(host, [])
    if ids:
        r["fichas"] = [{"id": i, **({"alerts": BY_ID[i]["alerts"]} if BY_ID[i].get("alerts") else {})} for i in ids]
    return r


@mcp.tool()
def tabla_pcaxis(tabla: str, filtro: str | None = None, max_filas: int = 200) -> dict:
    """Tabla PC-Axis en filas con números ya convertidos (None es dato no disponible o secreto, no cero): id de tabla
    del INE (24077), URL Tabla.htm del INE, Interior, Educación o Cultura, o URL del fichero. filtro deja las filas con
    ese texto en algún campo (código INE como 08019, nombre, periodo)."""
    return _datos(_consulta().tabla_pcaxis, tabla, filtro, max_filas)


@mcp.tool()
def boe_sumario(fecha: str, diario: str = "boe", seccion: str | None = None, texto: str | None = None,
                max_items: int = 200) -> dict:
    """Disposiciones de un día del BOE (diario=boe) o del BORME (diario=borme); fecha AAAA-MM-DD. Filtra por código de
    sección (1, 2A, 2B, 3, 4, 5A) y por texto en el título. Domingos y festivos no hay boletín."""
    return _datos(_consulta().boe_sumario, fecha, diario, seccion, texto, max_items)


@mcp.tool()
def subvenciones_nif(nif: str, max_filas: int = 20) -> dict:
    """Subvenciones, ayudas de Estado, minimis y grandes beneficiarios de un NIF en la BDNS, con totales y las más
    recientes."""
    return _datos(_consulta().subvenciones_nif, nif, max_filas)


@mcp.tool()
def empresa_nif(nif: str, max_filas: int = 10) -> dict:
    """Lo público de una empresa o entidad por NIF sin certificado: si es sector público (Invente, con DIR3),
    subvenciones, ayudas de Estado y minimis (BDNS), ayudas de la AEI y prohibiciones de contratar vigentes (por
    denominación). Con almacén local, también contratos adjudicados y actos del BORME (clave almacen); no_cubierto dice
    dónde mirar lo demás."""
    return _datos(_consulta().empresa_nif, nif, max_filas)


@mcp.tool()
def coyuntura() -> dict:
    """Último dato de los indicadores de coyuntura de España en una llamada: IPC (variación anual y mensual, marcando si
    es avance), paro EPA, PIB (variación trimestral y anual corregidas), paro registrado, Euríbor, dólar, deuda PDE,
    bono a 10 años y prima de riesgo. Cada uno con periodo, serie y fuente (INE o Banco de España)."""
    return _datos(_consulta().coyuntura)


@mcp.tool()
def perfil_municipio(municipio: str) -> dict:
    """Un municipio en una llamada (nombre, código INE, SIGPAC, DIR3 o NIF): sus códigos en cada sistema, población del
    padrón, renta neta media, paro registrado y contratos del año por mes (SEPE) y criminalidad acumulada (Interior,
    solo más de 20.000 habitantes). Cada bloque trae su fuente; uno que falle no tumba los demás."""
    return _datos(_consulta().perfil_municipio, municipio)


@mcp.tool()
def almacen_sql(consulta: str, limite: int = 100) -> dict:
    """SQL de solo lectura (DuckDB) sobre el almacén local en Parquet, si existe (FUENTES_ALMACEN o ./almacen): tablas
    boe, borme, bdns, placsp, placsp_adjudicaciones y carburantes, y vistas placsp_ultimo y adjudicaciones_ultimo
    (último estado de cada expediente). Devuelve columnas, filas y cobertura (solo está lo cargado). Sin almacén, dice
    cómo crearlo; empresa_nif lo usa solo para contratos y BORME."""
    def _ejecutar():
        try:
            from .clientes import almacen
        except ImportError:
            from clientes import almacen
        d = almacen.existe()
        if not d:
            return {"error": "no hay almacén local", "pista": "python scripts/clientes/almacen.py sync --fuentes boe,borme,bdns,placsp "
                    "--desde AAAA-MM-DD (guides/almacen.md); FUENTES_ALMACEN apunta a otra carpeta"}
        return dict(almacen.sql(consulta, d, limite), cobertura=almacen.cobertura(d))
    return _datos(_ejecutar)


@mcp.tool()
def ckan_buscar(portal: str, texto: str, limite: int = 10) -> dict:
    """Conjuntos de un portal CKAN con sus recursos (id, formato, si tiene datastore, url de descarga). portal:
    comunidad-madrid, madrid, barcelona, gva, andalucia, cnmc, renfe o la URL de su /api/3/action."""
    return _datos(_consulta().ckan_buscar, portal, texto, limite)


@mcp.tool()
def ckan_filas(portal: str, recurso: str, filtros: dict | None = None, limite: int = 100) -> dict:
    """Filas del datastore de un recurso CKAN con filtros por igualdad ({"Territorio": "Madrid"}), paginando sin el
    tope silencioso del portal. Devuelve total_datastore: compáralo con el fichero antes de dar un total."""
    return _datos(_consulta().ckan_filas, portal, recurso, filtros, limite)


@mcp.tool()
def socrata_filas(conjunto: str, where: str | None = None, select: str | None = None, order: str | None = None,
                  limite: int = 100) -> dict:
    """Filas de un conjunto de la Generalitat de Catalunya (analisi.transparenciacatalunya.cat, id como gn9e-3qhr) con
    SoQL; números ya convertidos. Los nombres de campo van sin caracteres no ASCII (estaci por Estació)."""
    return _datos(_consulta().socrata_filas, conjunto, where, select, order, limite)


@mcp.tool()
def sectores() -> list[dict]:
    """Sectores del catálogo con su título y número de fichas; el id sirve como filtro en buscar_fuentes."""
    counts = {}
    for s in SOURCES:
        counts[s["sector"]] = counts.get(s["sector"], 0) + 1
    return [{"id": k, "name": v, "sources": counts.get(k, 0)} for k, v in SECTORES.items()]


def read_llms() -> str:
    return locate("llms.txt").read_text(encoding="utf-8")


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


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
