"""Utilidades compartidas: carga de vocabulario y fichas."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
SCHEMA = ROOT / "schema" / "source.schema.json"
VOCAB = ROOT / "schema" / "vocab.yaml"
REPO_RAW = "https://raw.githubusercontent.com/BquantFinance/Administracion-fuentes-publicas/main"


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
INDEX_FILES = ("recetas", "rutas-muertas", "identificadores", "necesidades")


def load_indices() -> dict:
    """Carga los cuatro índices agregados de indices/*.yaml (listas, salvo identificadores que es un dict)."""
    out = {}
    for name in INDEX_FILES:
        path = INDICES / f"{name}.yaml"
        with path.open(encoding="utf-8") as fh:
            out[name] = yaml.safe_load(fh) or ([] if name != "identificadores" else {})
    return out
