#!/usr/bin/env python3
"""Genera los artefactos derivados a partir de sources/**/*.yaml.

Salidas (no editar a mano):
  catalog.json               todas las fichas, para carga programática
  sources/<sector>/README.md índice compacto por sector
  llms.txt                   mapa del repo para agentes
  llms-full.txt              todas las fichas en texto compacto
  README.md                  tabla de sectores entre marcadores AUTO
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date

from common import REPO_RAW, ROOT, load_sources, load_vocab

REPO_URL = "https://github.com/BquantFinance/Administracion-fuentes-publicas"


def clean(s: dict) -> dict:
    return {k: v for k, v in s.items() if not k.startswith("_")}


def fmt_list(v) -> str:
    return ", ".join(v) if isinstance(v, list) else str(v)


def render_source_compact(s: dict) -> str:
    """Bloque de texto compacto por fuente para llms-full.txt."""
    lines = [f"## {s['id']}", f"{s['name']} | {s['org']}"]
    lines.append(f"summary: {s['summary'].strip()}")
    lines.append(
        f"access: {fmt_list(s['access'])} | auth: {s['auth']} | formats: {fmt_list(s['formats'])} "
        f"| update: {s['update']} | status: {s['status']} | verified: {s.get('verified') or 'pending'}"
    )
    if s.get("coverage"):
        lines.append(f"coverage: {s['coverage']}")
    if s.get("license"):
        lines.append(f"license: {s['license']}")
    lines.append(f"base_url: {s['base_url']}")
    if s.get("docs_url"):
        lines.append(f"docs_url: {s['docs_url']}")
    for e in s.get("endpoints", []) or []:
        line = f"- {e['path']} :: {e['desc']}"
        if e.get("params"):
            line += f" [{e['params']}]"
        lines.append(line)
        if e.get("example"):
            lines.append(f"  ej: {e['example']}")
    if s.get("rate_limit"):
        lines.append(f"rate_limit: {s['rate_limit']}")
    for g in s.get("gotchas", []) or []:
        lines.append(f"! {g}")
    for tip in s.get("tips", []) or []:
        lines.append(f"+ {tip}")
    if s.get("related"):
        lines.append(f"related: {fmt_list(s['related'])}")
    return "\n".join(lines)


def render_sector_index(sector: str, title: str, items: list[dict]) -> str:
    lines = [
        f"# {title}",
        "",
        f"Sector `{sector}` · {len(items)} fuentes · índice generado por `scripts/build.py`, no editar.",
        "",
        "| id | fuente | acceso | auth | formatos | actualización | verificada |",
        "|---|---|---|---|---|---|---|",
    ]
    for s in items:
        lines.append(
            f"| [{s['id']}]({s['id']}.yaml) | {s['name']} | {fmt_list(s['access'])} | {s['auth']} "
            f"| {fmt_list(s['formats'])} | {s['update']} | {s.get('verified') or '—'} |"
        )
    lines.append("")
    for s in items:
        lines.append(f"- **{s['id']}**: {s['summary'].strip()}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    vocab = load_vocab()
    sources = load_sources()
    by_sector: dict[str, list[dict]] = defaultdict(list)
    for s in sources:
        by_sector[s["sector"]].append(s)
    for items in by_sector.values():
        items.sort(key=lambda s: s["id"])

    # catalog.json
    catalog = {
        "name": "Administración fuentes públicas",
        "description": "Catálogo de fuentes de datos de la Administración pública española, optimizado para agentes.",
        "generated": date.today().isoformat(),
        "repo": REPO_URL,
        "schema": f"{REPO_RAW}/schema/source.schema.json",
        "vocab": f"{REPO_RAW}/schema/vocab.yaml",
        "count": len(sources),
        "sectors": {k: v for k, v in vocab["sector"].items() if k in by_sector},
        "sources": [clean(s) for s in sources],
    }
    (ROOT / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    # índices por sector
    for sector, items in by_sector.items():
        (ROOT / "sources" / sector / "README.md").write_text(
            render_sector_index(sector, vocab["sector"][sector], items), encoding="utf-8"
        )

    # tabla de sectores (README) siguiendo el orden del vocabulario
    table = ["| sector | descripción | fuentes |", "|---|---|---|"]
    for sector, title in vocab["sector"].items():
        n = len(by_sector.get(sector, []))
        link = f"[{sector}](sources/{sector}/README.md)" if n else f"`{sector}`"
        table.append(f"| {link} | {title} | {n} |")
    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    readme = re.sub(
        r"(<!-- AUTO:sectors -->).*?(<!-- /AUTO:sectors -->)",
        lambda m: f"{m.group(1)}\n{chr(10).join(table)}\n{m.group(2)}",
        readme,
        flags=re.S,
    )
    readme = re.sub(
        r"(<!-- AUTO:count -->).*?(<!-- /AUTO:count -->)",
        lambda m: f"{m.group(1)}{len(sources)}{m.group(2)}",
        readme,
        flags=re.S,
    )
    readme_path.write_text(readme, encoding="utf-8")

    # llms.txt
    llms = [
        "# Administración fuentes públicas (España)",
        "",
        "> Catálogo de fuentes de datos de la Administración pública española para desarrolladores y agentes: "
        "APIs, descargas, feeds, servicios geográficos y registros. Una ficha YAML por fuente con URL base, "
        "endpoints, autenticación, formatos, periodicidad y trampas conocidas. Contenido en castellano, claves en inglés.",
        "",
        f"Fuentes: {len(sources)} · Alcance actual: Administración General del Estado · Generado: {date.today().isoformat()}",
        "",
        "## Cómo usar este repo",
        "",
        f"- Todo el catálogo en un fichero: {REPO_RAW}/catalog.json",
        f"- Todas las fichas en texto compacto: {REPO_RAW}/llms-full.txt",
        f"- Una ficha: {REPO_RAW}/sources/<sector>/<id>.yaml",
        f"- Esquema de ficha: {REPO_RAW}/schema/source.schema.json",
        f"- Vocabulario (sectores, acceso, auth, formatos): {REPO_RAW}/schema/vocab.yaml",
        "- `verified: null` significa que la ficha se redactó a partir de documentación oficial pero aún no se ha probado el endpoint.",
        "",
        "## Sectores",
        "",
    ]
    for sector, title in vocab["sector"].items():
        items = by_sector.get(sector)
        if not items:
            continue
        ids = ", ".join(s["id"] for s in items)
        llms.append(f"- [{title}]({REPO_RAW}/sources/{sector}/README.md): {ids}")
    llms += ["", "## Guías transversales", ""]
    for g in sorted((ROOT / "guides").glob("*.md")):
        title = g.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        llms.append(f"- [{title}]({REPO_RAW}/guides/{g.name})")
    llms += ["", "## Optional", "", f"- [Contribuir]({REPO_RAW}/CONTRIBUTING.md)", f"- [Plantilla de ficha]({REPO_RAW}/templates/source.yaml)", ""]
    (ROOT / "llms.txt").write_text("\n".join(llms), encoding="utf-8")

    # llms-full.txt
    full = [llms[0], "", llms[2], "", f"Fuentes: {len(sources)} · Generado: {date.today().isoformat()} · Formato: un bloque por fuente; '!' marca trampas; '+' marca consejos; 'ej:' es una llamada lista para copiar.", ""]
    for sector, title in vocab["sector"].items():
        items = by_sector.get(sector)
        if not items:
            continue
        full.append(f"# SECTOR {sector}: {title}")
        full.append("")
        for s in items:
            full.append(render_source_compact(s))
            full.append("")
    (ROOT / "llms-full.txt").write_text("\n".join(full), encoding="utf-8")

    print(f"build OK: {len(sources)} fuentes, {len(by_sector)} sectores")


if __name__ == "__main__":
    main()
