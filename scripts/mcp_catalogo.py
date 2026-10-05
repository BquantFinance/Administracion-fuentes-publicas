#!/usr/bin/env python3
"""Servidor MCP mínimo (stdio) que expone catalog.json por herramientas.

Un agente carga solo lo que necesita (una ficha, una receta, una necesidad) en vez de todo llms.txt.
Arranque: python scripts/mcp_catalogo.py (desde el repo) o mcp-catalogo tras instalarlo con pip o uvx; si no hay catalog.json local lo descarga de GitHub y lo cachea en ~/.cache/fuentes-publicas.
Prueba real: python scripts/test_mcp_catalogo.py.
"""
import difflib
import functools
import inspect
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
        with urllib.request.urlopen(req, timeout=30) as r:
            datos = r.read()
        if name.endswith(".json"):
            json.loads(datos)  # una descarga cortada o una página de error no sustituye a la copia buena
        # se escribe aparte y se reemplaza: abrir la caché en "wb" antes de leer la dejaba a 0 bytes si la descarga
        # fallaba, y el servidor no volvía a arrancar sin red justo cuando la copia hacía falta
        tmp = cached.with_name(f"{cached.name}.{os.getpid()}.tmp")
        tmp.write_bytes(datos)
        os.replace(tmp, cached)
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
    "Datos públicos de España para construir productos. buscar(texto) mira a la vez fichas, recetas, necesidades, "
    "productos e identificadores y devuelve un índice ligero; ficha(id) da el detalle de cualquiera de ellos (de una "
    "fuente: endpoints, ejemplos y trampas verificadas, alerts primero porque cambian la cifra sin dar error). Datos ya resueltos: perfil_municipio, coyuntura, empresa_nif, "
    "boe_sumario, tabla_pcaxis, ckan_buscar, ckan_filas, socrata_filas, almacen_sql y descargar(url) para cualquier "
    "otra URL pública. Lee catalogo://reglas antes de programar contra una fuente."
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
PRODUCTOS = IDX.get("productos") or []
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


def _columnas(r):
    """Filas como listas bajo columnas, en vez de un dict por fila que repite los nombres (la mitad de tokens), a
    cualquier nivel: también las tablas anidadas de empresa_nif o perfil_municipio."""
    if isinstance(r, list):
        return [_columnas(x) for x in r]
    if not isinstance(r, dict):
        return r
    r = {k: _columnas(v) for k, v in r.items()}
    filas = r.get("filas")
    if isinstance(filas, list) and filas and all(isinstance(f, dict) for f in filas):
        cols = list(r.get("columnas") or dict.fromkeys(k for f in filas for k in f))
        r["columnas"], r["filas"] = cols, [[f.get(c) for c in cols] for f in filas]
    return r


def herramienta(fn):
    """Registra la herramienta y devuelve JSON compacto (sin sangría ni espacios) con las filas en columnas: la
    librería serializa con sangría y eso solo eran tokens."""
    @functools.wraps(fn)
    def envoltura(*args, **kwargs):
        return json.dumps(_columnas(fn(*args, **kwargs)), ensure_ascii=False, separators=(",", ":"), default=str)
    envoltura.__signature__ = inspect.signature(fn).replace(return_annotation=str)
    envoltura.__annotations__ = {**fn.__annotations__, "return": str}
    descripcion = " ".join((fn.__doc__ or "").split())  # sin la sangría de la docstring
    try:
        registrar = mcp.tool(description=descripcion, structured_output=False)  # sin copia estructurada duplicada
    except TypeError:  # versiones sin el parámetro
        registrar = mcp.tool(description=descripcion)
    registrar(envoltura)
    try:  # esquema sin title por parámetro ni anyOf para los opcionales: lo mismo en la mitad de tokens
        tool = mcp._tool_manager._tools[fn.__name__]
        tool.parameters = _esquema_compacto(tool.parameters)
    except (AttributeError, KeyError):
        pass
    return envoltura


def _esquema_compacto(s):
    if isinstance(s, list):
        return [_esquema_compacto(x) for x in s]
    if not isinstance(s, dict):
        return s
    s = {k: _esquema_compacto(v) for k, v in s.items() if k != "title"}
    tipos = s.get("anyOf")
    if isinstance(tipos, list) and len(tipos) == 2 and {"type": "null"} in tipos:
        otro = next(x for x in tipos if x != {"type": "null"})
        if set(otro) == {"type"}:
            del s["anyOf"]
            s["type"] = [otro["type"], "null"]
    return s


def _fichas(consulta: str, sector: str | None, limite: int) -> list[dict]:
    items = SOURCES
    if sector:
        if sector not in SECTORES:
            raise ValueError(f"sector desconocido: {sector}; válidos: {', '.join(SECTORES)}")
        items = [s for s in SOURCES if s["sector"] == sector]
    return [
        {**{k: s.get(k) for k in ("id", "name", "sector", "access", "auth", "status", "verified", "summary")},
         **({"alerts": s["alerts"]} if s.get("alerts") else {})}
        for s in rank(consulta, items, lambda s: SOURCE_FIELDS[s["id"]], limite)
    ]


@herramienta
def buscar(consulta: str, sector: str | None = None, limite: int = 5) -> dict:
    """Busca a la vez fichas (resumen y alerts), recetas que cruzan fuentes, necesidades con la ficha que las resuelve,
    productos que se pueden construir e identificadores. Devuelve un índice ligero; el detalle, con ficha(id)."""
    out = {
        "fichas": _fichas(consulta, sector, limite),
        "recetas": [{"id": r["id"], "intent": r["intent"], "sources": list(dict.fromkeys(st["source"] for st in r["steps"])),
                     "verified": r.get("verified")} for r in rank(consulta, RECETAS, lambda r: RECETA_FIELDS[r["id"]], 3)],
        "necesidades": [{"need": n["need"], "source": n.get("source"), "note": n.get("note")}
                        for n in rank(consulta, NECESIDADES, lambda n: (norm(n["need"]), norm([n.get("source"), n.get("note")])), 3)],
        "productos": [{"id": p["id"], "producto": p["producto"], "fuentes": p["fuentes"]} for p in
                      rank(consulta, PRODUCTOS, lambda p: (norm([p["id"], p["producto"]]), norm([p.get("cliente"), p["fuentes"], p.get("piezas")])), 3)],
        "identificadores": [{"id": k, "format": v.get("format"), "example": v.get("example")} for k, v in
                            rank(consulta, list(IDENTIFICADORES.items()), lambda kv: (norm(kv[0]), norm([kv[1].get("format"), kv[1].get("issuer")])), 2)],
    }
    return {k: v for k, v in out.items() if v} or {"nota": "nada casa; probar con otras palabras o leer catalogo://llms.txt"}


PRODUCTO_BY_ID = {p["id"]: p for p in PRODUCTOS}


@herramienta
def ficha(id: str) -> dict:
    """Detalle de cualquier id de buscar: fuente (alerts primero, endpoints con ejemplo y respuesta, sync, gotchas),
    receta (pasos), producto (piezas, frescura, licencia, trampa) o identificador (regex, cruces). Si no existe, ids
    parecidos."""
    if id in BY_ID:
        s = BY_ID[id]
        return {"alerts": s["alerts"], **s} if s.get("alerts") else s
    if id in RECETA_BY_ID:
        return {"tipo": "receta", **{k: v for k, v in RECETA_BY_ID[id].items() if k != "checks"}}
    if id in PRODUCTO_BY_ID:
        return {"tipo": "producto", **PRODUCTO_BY_ID[id]}
    if id in IDENTIFICADORES:
        return {"tipo": "identificador", "id": id, **IDENTIFICADORES[id]}
    return {"error": f"no existe {id}", "sugerencias": parecidos(id, [*BY_ID, *RECETA_BY_ID, *PRODUCTO_BY_ID, *IDENTIFICADORES])}


def rutas_muertas(url: str) -> list[dict]:
    """Rutas muertas que casan con la URL, exacta o por prefijo en ambos sentidos."""
    wanted = url.strip().rstrip("/")
    exact = [d for d in RUTAS_MUERTAS if d["old"].rstrip("/") == wanted]
    prefix = [d for d in RUTAS_MUERTAS if d not in exact
              and (d["old"].rstrip("/").startswith(wanted) or wanted.startswith(d["old"].rstrip("/")))]
    return [{k: d.get(k) for k in ("old", "status", "new", "source", "note", "checked")} for d in exact + prefix]


@herramienta
def codigos(grupo: str | None = None) -> dict | list[dict]:
    """Códigos que una API exige y no se adivinan (Id del INE para tv, países de DataComex, estaciones de AEMET,
    productos de carburantes, rangos del BOE). Sin grupo, la lista de grupos; con grupo, sus entradas."""
    if grupo is None:
        return [
            {"grupo": k, "source": g["source"], "use": g["use"], "entries": len(g["entries"]), "verified": g["verified"]}
            for k, g in CODIGOS.items()
        ]
    if grupo in CODIGOS:
        return CODIGOS[grupo]
    return {"error": f"no existe el grupo {grupo}", "sugerencias": parecidos(grupo, CODIGOS)}


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


@herramienta
def descargar(url: str, max_caracteres: int = 20000, desde: int = 0) -> dict:
    """Descarga una URL pública resolviendo certificados FNMT, User-Agent, reintentos, gzip y codificación, y la resume
    (CSV, JSON, xlsx o ZIP). Avisa de bloqueos de WAF, añade las alerts de la ficha del host y la sustituta si la URL
    está muerta. Hasta 25 MB. Para cuando tu fetch falle con un .gob.es o para ver qué devuelve una URL."""
    r = _datos(_consulta().descargar, url, max_caracteres, desde)
    host = urlparse(r.get("url") or url).hostname or ""
    ids = FICHAS_POR_HOST.get(host, [])
    if ids:
        r["fichas"] = [{"id": i, **({"alerts": BY_ID[i]["alerts"]} if BY_ID[i].get("alerts") else {})} for i in ids]
    muertas = rutas_muertas(url)
    if muertas:
        r["rutas_muertas"] = muertas  # URL que un agente recuerda y ya no vale: sustituta en new
    return r


@herramienta
def tabla_pcaxis(tabla: str, filtro: str | None = None, max_filas: int = 200) -> dict:
    """Tabla PC-Axis en filas con números ya convertidos (None es dato no disponible o secreto, no cero): id de tabla
    del INE (24077), URL Tabla.htm del INE, Interior, Educación o Cultura, o URL del fichero. filtro deja las filas con
    ese texto en algún campo (código INE como 08019, nombre, periodo)."""
    return _datos(_consulta().tabla_pcaxis, tabla, filtro, max_filas)


@herramienta
def boe_sumario(fecha: str, diario: str = "boe", seccion: str | None = None, texto: str | None = None,
                max_items: int = 200) -> dict:
    """Disposiciones de un día del BOE (diario=boe) o del BORME (diario=borme); fecha AAAA-MM-DD. Filtra por código de
    sección (1, 2A, 2B, 3, 4, 5A) y por texto en el título. Domingos y festivos no hay boletín."""
    return _datos(_consulta().boe_sumario, fecha, diario, seccion, texto, max_items)


CAMPOS_BDNS = ("fechaConcesion", "importe", "ayudaEquivalente", "instrumento", "numeroConvocatoria", "convocatoria",
               "convocante", "nivel2", "nivel3", "reglamento", "objetivo", "ejercicio", "ayudaETotal")


CAMPOS_AEI = ("Año", "Convocatoria", "Referencia", "Título", "€ Conced.")
CORTE = {"convocante": 80, "reglamento": 60, "objetivo": 80}  # instrumento solo si no es la subvención de siempre


def _corto(v, n: int = 120):
    return v[: n - 1].rstrip() + "…" if isinstance(v, str) and len(v) > n and not v.startswith("http") else v


def _empresa_compacta(r: dict) -> dict:
    """Las filas de la BDNS y de la AEI repiten el NIF y el nombre ya conocidos y traen ids internos y URL: se quedan
    los campos que sirven para decidir, con los textos cortados a 120 caracteres (numeroConvocatoria o Referencia
    llevan al resto) y la AEI de lo más reciente a lo más antiguo. Del almacén, solo la cobertura de sus tablas."""
    for col in (r.get("subvenciones") or {}).values():
        if isinstance(col, dict) and isinstance(col.get("filas"), list):
            col["filas"] = [{k: _corto(v.strip() if isinstance(v, str) else v, CORTE.get(k, 120)) for k, v in f.items()
                             if k in CAMPOS_BDNS and not (k == "instrumento" and str(v).startswith("SUBVENCIÓN y ENTREGA"))}
                            for f in col["filas"]]
    aei = r.get("aei")
    if isinstance(aei, dict) and isinstance(aei.get("filas"), list):
        filas = sorted(aei["filas"], key=lambda f: str(f.get("Año", "")), reverse=True)
        aei["filas"] = [{k: _corto(f.get(k), 100) for k in CAMPOS_AEI} for f in filas]
    alm = r.get("almacen")
    if isinstance(alm, dict):
        if isinstance(alm.get("cobertura"), dict):
            alm["cobertura"] = {k: v for k, v in alm["cobertura"].items() if k in ("placsp", "placsp_adjudicaciones", "borme", "bdns")}
        for f in ((alm.get("contratos") or {}).get("recientes") or []):
            f["objeto"] = _corto(f.get("objeto"), 100)
    return r


@herramienta
def empresa_nif(nif: str | list[str], max_filas: int = 5) -> dict:
    """Lo público de una empresa o entidad por NIF: si es sector público (con DIR3), subvenciones, ayudas de Estado y
    minimis con totales (BDNS), ayudas de la AEI y prohibiciones de contratar; con almacén local, contratos adjudicados
    y actos del BORME. Con un nombre en vez de NIF, candidatos con su NIF (directorio de la BDNS y del almacén, sin
    personas físicas), o el perfil si uno coincide exacto. Con una lista de hasta 10, todos en una llamada."""
    if isinstance(nif, list):
        c = _consulta()
        return {"empresas": [_empresa_compacta(r) for r in c.en_lote(lambda n: c.empresa_nif(n, max_filas), nif[:10], 3)]}
    return _empresa_compacta(_datos(_consulta().empresa_nif, nif, max_filas))


@herramienta
def coyuntura() -> dict:
    """Último dato de coyuntura de España con periodo, serie y fuente: IPC (marcando si es avance), paro EPA, PIB
    corregido, paro registrado, Euríbor, dólar, deuda PDE, bono a 10 años y prima de riesgo."""
    return _datos(_consulta().coyuntura)


@herramienta
def perfil_municipio(municipio: str | list[str], solo_codigos: bool = False) -> dict:
    """Un municipio (nombre, código INE, SIGPAC, DIR3 o NIF) o el de una dirección («calle Alcalá 50, Madrid») o
    «lat,lon» en una llamada: sus códigos en cada sistema (SIGPAC y Catastro numeran distinto que el INE), padrón, renta
    media, paro y contratos del año por mes, criminalidad, viviendas turísticas (INE y registro autonómico) y compraventas
    y valor tasado de vivienda; con dirección
    o coordenadas, además ubicacion (CP, coordenadas y
    referencia catastral del portal; exacta=false si la calle hallada no es la pedida; en el campo, recinto SIGPAC, uso y
    referencia de la parcela), certificados energéticos del edificio (Cataluña y C. Valenciana) y, a menos de 1 km,
    puntos de recarga, colegios y centros de salud y hospitales con los tres más cercanos. solo_codigos=True da solo los códigos y la ubicación. Con una lista de hasta 20, en una llamada."""
    c = _consulta()
    if solo_codigos and isinstance(municipio, str) and c.es_ubicacion(municipio):
        u = c.ubicar(municipio)
        return u if u.get("error") else {"ubicacion": u, "candidatos": c.buscar_municipio(u["ine"], 1)}
    if isinstance(municipio, list):
        if solo_codigos:
            return {"candidatos": {q: c.buscar_municipio(q, 5) for q in municipio[:20]}}
        return {"perfiles": c.en_lote(c.perfil_municipio, municipio[:20], 4)}
    if solo_codigos:
        return {"candidatos": c.buscar_municipio(municipio, 5)}
    return _datos(c.perfil_municipio, municipio)


@herramienta
def almacen_sql(consulta: str, limite: int = 100) -> dict:
    """SQL de solo lectura (DuckDB) sobre el almacén local en Parquet si existe: tablas boe, borme, bdns, placsp,
    placsp_adjudicaciones y carburantes, y vistas placsp_ultimo y adjudicaciones_ultimo (último estado). Devuelve
    columnas, filas y cobertura; sin almacén, cómo crearlo."""
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


@herramienta
def ckan_buscar(portal: str, texto: str, limite: int = 10) -> dict:
    """Conjuntos de un portal CKAN con sus recursos (id, formato, si tiene datastore, url de descarga). portal:
    comunidad-madrid, madrid, barcelona, gva, andalucia, cnmc, renfe o la URL de su /api/3/action."""
    return _datos(_consulta().ckan_buscar, portal, texto, limite)


@herramienta
def ckan_filas(portal: str, recurso: str, filtros: dict | None = None, limite: int = 100) -> dict:
    """Filas del datastore de un recurso CKAN con filtros por igualdad ({"Territorio": "Madrid"}), paginando sin el
    tope silencioso del portal. Devuelve total_datastore: compáralo con el fichero antes de dar un total."""
    return _datos(_consulta().ckan_filas, portal, recurso, filtros, limite)


@herramienta
def socrata_filas(conjunto: str, where: str | None = None, select: str | None = None, order: str | None = None,
                  limite: int = 100) -> dict:
    """Filas de un conjunto de la Generalitat de Catalunya (analisi.transparenciacatalunya.cat, id como gn9e-3qhr) con
    SoQL; números ya convertidos. Los nombres de campo van sin caracteres no ASCII (estaci por Estació)."""
    return _datos(_consulta().socrata_filas, conjunto, where, select, order, limite)


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
