#!/usr/bin/env python3
"""Genera los artefactos derivados a partir de sources/**/*.yaml e indices/*.yaml.

Salidas (no editar a mano):
  catalog.json               todas las fichas y los índices, para carga programática
  sources/<sector>/README.md índice compacto por sector, con las necesidades que resuelve
  indices/README.md          recetas, dónde está cada cosa, identificadores y rutas muertas
  llms.txt                   mapa del repo para agentes
  llms-full.txt              todas las fichas en texto compacto
  README.md                  tabla de sectores entre marcadores AUTO
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date

from common import REPO_RAW, ROOT, load_indices, load_sources, load_vocab

REPO_URL = "https://github.com/BquantFinance/Administracion-fuentes-publicas"


def clean(s: dict) -> dict:
    return {k: v for k, v in s.items() if not k.startswith("_")}


def fmt_list(v) -> str:
    return ", ".join(v) if isinstance(v, list) else str(v)


def cell(v) -> str:
    return str(v).replace("|", "\\|") if v is not None else "—"


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
    if s.get("quirks"):
        lines.append(f"quirks: {fmt_list(s['quirks'])}")
    if s.get("ids"):
        lines.append(f"ids: {fmt_list(s['ids'])}")
    for g in s.get("gotchas", []) or []:
        lines.append(f"! {g}")
    for tip in s.get("tips", []) or []:
        lines.append(f"+ {tip}")
    if s.get("related"):
        lines.append(f"related: {fmt_list(s['related'])}")
    return "\n".join(lines)


def render_sector_index(sector: str, title: str, items: list[dict], needs: list[dict]) -> str:
    lines = [
        f"# {title}",
        "",
        f"Sector `{sector}` · {len(items)} fuentes · índice generado por `scripts/build.py`, no editar.",
        "",
    ]
    if needs:
        lines += ["## Dónde está cada cosa", ""]
        for n in needs:
            note = f" ({n['note']})" if n.get("note") else ""
            lines.append(f"- {n['need']} → `{n['source']}`{note}")
        lines.append("")
    lines += [
        "| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for s in items:
        lines.append(
            f"| [{s['id']}]({s['id']}.yaml) | {s['name']} | {fmt_list(s['access'])} | {s['auth']} "
            f"| {fmt_list(s['formats'])} | {s['update']} | {fmt_list(s.get('quirks') or []) or '—'} | {s.get('verified') or '—'} |"
        )
    lines.append("")
    for s in items:
        lines.append(f"- **{s['id']}**: {s['summary'].strip()}")
    lines.append("")
    return "\n".join(lines)


def render_indices_readme(idx: dict, sector_of: dict[str, str], vocab: dict, used_by: dict[str, list[str]]) -> str:
    recetas, dead, idents, needs = idx["recetas"], idx["rutas-muertas"], idx["identificadores"], idx["necesidades"]
    lines = [
        "# Índices para agentes",
        "",
        f"Generado por `scripts/build.py` a partir de `indices/*.yaml`, no editar. {len(recetas)} recetas, "
        f"{len(needs)} necesidades, {len(idents)} identificadores, {len(dead)} rutas muertas.",
        "",
        "## Recetas por intención",
        "",
        "Procedimientos verificados que encadenan fichas. `python scripts/check_recetas.py` ejecuta las comprobaciones "
        "de cada receta contra los servidores reales (batería de regresión).",
        "",
        "| receta | intención | fichas | verificada |",
        "|---|---|---|---|",
    ]
    for r in recetas:
        srcs = []
        for s in r["steps"]:
            if s["source"] not in srcs:
                srcs.append(s["source"])
        lines.append(f"| `{r['id']}` | {cell(r['intent'])} | {', '.join(srcs)} | {r.get('verified') or 'pendiente'} |")
    lines += ["", "### Pasos", ""]
    for r in recetas:
        lines.append(f"**{r['id']}** · {r['intent']}")
        if r.get("inputs"):
            lines.append(f"- entrada: {', '.join(r['inputs'])}")
        for n, s in enumerate(r["steps"], 1):
            lines.append(f"{n}. `{s['source']}`: {s['do']}")
            if s.get("example"):
                lines.append(f"   ```")
                lines.append(f"   {s['example']}")
                lines.append(f"   ```")
        lines.append(f"- salida: {r['output']}")
        if r.get("note"):
            lines.append(f"- nota: {r['note']}")
        lines.append("")
    lines += ["## Dónde está cada cosa", ""]
    by_sector: dict[str, list[dict]] = defaultdict(list)
    for n in needs:
        by_sector[sector_of.get(n["source"], "sin-fuente")].append(n)
    for sector, title in list(vocab["sector"].items()) + [("sin-fuente", "Sin fuente en el catálogo")]:
        items = by_sector.get(sector)
        if not items:
            continue
        lines.append(f"**{title}**")
        for n in items:
            src = f"`{n['source']}`" if n.get("source") else "ninguna"
            note = f" ({n['note']})" if n.get("note") else ""
            lines.append(f"- {n['need']} → {src}{note}")
        lines.append("")
    lines += [
        "## Identificadores para cruzar datos",
        "",
        "| id | formato | regex | ejemplo | emisor | lo usan |",
        "|---|---|---|---|---|---|",
    ]
    for key, info in idents.items():
        rx = f"`{info['regex']}`" if info.get("regex") else "—"
        lines.append(
            f"| {key} | {cell(info['format'])} | {rx} | {cell(info.get('example'))} | {cell(info.get('issuer'))} | {', '.join(used_by.get(key, [])) or '—'} |"
        )
    lines.append("")
    for key, info in idents.items():
        if info.get("gotcha") or info.get("joins"):
            lines.append(f"**{key}**")
            if info.get("gotcha"):
                lines.append(f"- trampa: {info['gotcha']}")
            for j in info.get("joins") or []:
                lines.append(f"- vía `{j['via']}`: {j['how']}")
            lines.append("")
    lines += [
        "## Rutas muertas",
        "",
        "URLs de documentación antigua que ya no sirven y su sustituta verificada.",
        "",
        "| ruta antigua | estado | sustituta | ficha | nota | comprobada |",
        "|---|---|---|---|---|---|",
    ]
    for d in dead:
        lines.append(
            f"| {cell(d['old'])} | {d['status']} | {cell(d.get('new'))} | `{d['source']}` | {cell(d.get('note'))} | {d['checked']} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    vocab = load_vocab()
    sources = load_sources()
    idx = load_indices()
    by_sector: dict[str, list[dict]] = defaultdict(list)
    for s in sources:
        by_sector[s["sector"]].append(s)
    for items in by_sector.values():
        items.sort(key=lambda s: s["id"])
    sector_of = {s["id"]: s["sector"] for s in sources}
    used_by: dict[str, list[str]] = defaultdict(list)
    for s in sources:
        for i in s.get("ids") or []:
            used_by[i].append(s["id"])
    needs_by_sector: dict[str, list[dict]] = defaultdict(list)
    for n in idx["necesidades"]:
        if n.get("source"):
            needs_by_sector[sector_of[n["source"]]].append(n)

    # catalog.json
    identificadores = {k: dict(v, used_by=used_by.get(k, [])) for k, v in idx["identificadores"].items()}
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
        "indices": {
            "recetas": idx["recetas"],
            "necesidades": idx["necesidades"],
            "identificadores": identificadores,
            "rutas_muertas": idx["rutas-muertas"],
        },
    }
    (ROOT / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    # índices por sector
    for sector, items in by_sector.items():
        (ROOT / "sources" / sector / "README.md").write_text(
            render_sector_index(sector, vocab["sector"][sector], items, needs_by_sector.get(sector, [])),
            encoding="utf-8",
        )

    # índices agregados
    (ROOT / "indices" / "README.md").write_text(
        render_indices_readme(idx, sector_of, vocab, used_by), encoding="utf-8"
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
        f"Fuentes: {len(sources)} · Recetas: {len(idx['recetas'])} · Alcance actual: Administración General del Estado · Generado: {date.today().isoformat()}",
        "",
        "## Cómo usar este repo",
        "",
        f"- Todo el catálogo (fichas e índices) en un fichero: {REPO_RAW}/catalog.json",
        f"- Todas las fichas en texto compacto: {REPO_RAW}/llms-full.txt",
        f"- Una ficha: {REPO_RAW}/sources/<sector>/<id>.yaml",
        f"- Índices para agentes (recetas paso a paso, identificadores con regex y cruces, rutas muertas con sustituta): {REPO_RAW}/indices/README.md",
        f"- Esquema de ficha: {REPO_RAW}/schema/source.schema.json",
        f"- Vocabulario (sectores, acceso, auth, formatos, quirks, ids): {REPO_RAW}/schema/vocab.yaml",
        "- `verified: null` significa que la ficha se redactó a partir de documentación oficial pero aún no se ha probado el endpoint.",
        "",
        "## Reglas rápidas antes de programar contra una fuente",
        "",
        "- Lee `quirks`, `ids` y `gotchas` de la ficha: son hechos verificados con llamadas reales, no documentación oficial. `quirks` dice cómo configurar el cliente; `ids` con qué otras fuentes se cruza.",
        "- Muchos servidores .gob.es sirven certificados FNMT sin la cadena intermedia; curl y requests fallan hasta añadirla al bundle. Arreglo copiable en la guía Cliente HTTP (`python scripts/fnmt_bundle.py` genera ca-age.pem).",
        "- Envía siempre User-Agent y Accept de navegador; varios sitios (tesoro.es, seg-social.es) devuelven 403 a los valores por defecto de curl y requests.",
        "- Las APIs del BOE exigen Accept explícito (application/json o application/xml) y devuelven los errores siempre en XML.",
        "- Espera ISO-8859-1 en feeds del BOE y CSV del Banco de España; convierte antes de parsear.",
        "- Ninguna fuente verificada documenta límites ni devolvió 429; para descargas masivas, peticiones secuenciales y reintento con espera ante 5xx. El Catastro bloquea la IP tras ráfagas de unas 15 peticiones.",
        "- Si una URL que recuerdas falla, busca en la tabla de rutas muertas antes de dar la fuente por perdida.",
        "",
        "## Dónde está cada cosa",
        "",
    ]
    for n in idx["necesidades"]:
        src = f"{n['source']}" if n.get("source") else "ninguna"
        note = f" ({n['note']})" if n.get("note") else ""
        llms.append(f"- {n['need']} → {src}{note}")
    llms += ["", "## Recetas por intención", "", f"Pasos, ejemplos y comprobaciones en {REPO_RAW}/indices/recetas.yaml", ""]
    for r in idx["recetas"]:
        srcs = []
        for s in r["steps"]:
            if s["source"] not in srcs:
                srcs.append(s["source"])
        llms.append(f"- {r['id']}: {r['intent']} → {', '.join(srcs)}")
    llms += ["", "## Sectores", ""]
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
    full = [llms[0], "", llms[2], "", f"Fuentes: {len(sources)} · Generado: {date.today().isoformat()} · Formato: un bloque por fuente; '!' marca trampas; '+' marca consejos; 'ej:' es una llamada lista para copiar. Recetas, identificadores y rutas muertas en indices/README.md.", ""]
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

    print(
        f"build OK: {len(sources)} fuentes, {len(by_sector)} sectores, {len(idx['recetas'])} recetas, "
        f"{len(idx['necesidades'])} necesidades, {len(idx['rutas-muertas'])} rutas muertas"
    )


if __name__ == "__main__":
    main()
