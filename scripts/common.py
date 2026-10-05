"""Utilidades compartidas: carga de vocabulario y fichas, herramientas del servidor MCP y puntero al código de una ficha."""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
SCHEMA = ROOT / "schema" / "source.schema.json"
VOCAB = ROOT / "schema" / "vocab.yaml"
REPO_RAW = "https://raw.githubusercontent.com/BquantFinance/Administracion-fuentes-publicas/main"
SCRIPTS = Path(__file__).resolve().parent  # scripts/ en el repo, fuentes_publicas/ instalado


def herramientas_mcp() -> list[dict]:
    """Nombre, firma y descripción de cada herramienta de mcp_catalogo.py, leídos sin importar el servidor: la lista
    única que usan build.py (guía y manifiesto) y validate.py (code.mcp de las fichas)."""
    tree = ast.parse((SCRIPTS / "mcp_catalogo.py").read_text(encoding="utf-8"))
    out = []
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and any(ast.unparse(d) in ("herramienta", "mcp.tool()") for d in n.decorator_list):
            args = n.args.args
            defaults = [None] * (len(args) - len(n.args.defaults)) + list(n.args.defaults)
            firma = ", ".join(a.arg + (f"={ast.unparse(d)}" if d is not None else "") for a, d in zip(args, defaults))
            doc = " ".join((ast.get_docstring(n) or "").split())
            primera = doc.split(". ")[0].rstrip(".") + "."
            out.append({"name": n.name, "firma": f"{n.name}({firma})", "doc": doc, "resumen": primera})
    return out


def comandos_paquete() -> set[str]:
    """Órdenes de consola que instala el paquete ([project.scripts] de pyproject.toml): fuentes-almacen, fuentes-radar..."""
    texto = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    seccion = re.search(r"^\[project\.scripts\]\n(.*?)(?=^\[|\Z)", texto, flags=re.M | re.S)
    return set(re.findall(r"^([\w-]+)\s*=", seccion.group(1), flags=re.M)) if seccion else set()


def puntero_code(code: dict | None) -> str | None:
    """Lo que buscar y llms.txt dicen del código de una ficha: su módulo (clientes.placsp) o, si la trae resuelta la capa
    de consulta, la herramienta MCP que la envuelve (perfil_municipio)."""
    if not code:
        return None
    corto = code["module"].rsplit(".", 1)[-1]
    return code["mcp"][0] if corto == "consulta" and code.get("mcp") else f"clientes.{corto}"


def load_vocab() -> dict:
    with VOCAB.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def iter_source_files():
    return sorted(SOURCES.glob("*/*.yaml"))


def load_sources() -> list[dict]:
    out = []
    for path in iter_source_files():
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        data["_path"] = path.relative_to(ROOT).as_posix()
        data["_dir_sector"] = path.parent.name
        out.append(data)
    return out


def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)

INDICES = ROOT / "indices"
INDEX_FILES = ("productos", "recetas", "rutas-muertas", "identificadores", "necesidades", "codigos")


def load_indices() -> dict:
    """Carga los índices agregados de indices/*.yaml (listas, salvo identificadores y codigos, que son dicts)."""
    out = {}
    for name in INDEX_FILES:
        path = INDICES / f"{name}.yaml"
        with path.open(encoding="utf-8") as fh:
            out[name] = yaml.safe_load(fh) or ([] if name not in ("identificadores", "codigos") else {})
    return out
