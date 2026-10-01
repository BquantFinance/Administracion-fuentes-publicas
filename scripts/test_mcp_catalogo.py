#!/usr/bin/env python3
"""Prueba real del servidor MCP: lo arranca por stdio, lista las herramientas y llama a varias.

Uso: python scripts/test_mcp_catalogo.py. Necesita catalog.json (python scripts/build.py) y el paquete mcp.
No está en CI: es una comprobación manual tras tocar mcp_catalogo.py o el catálogo.
"""
import asyncio
import json
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent.parent
SERVER = ROOT / "scripts" / "mcp_catalogo.py"
TOOLS = {"buscar_fuentes", "ficha", "buscar_recetas", "receta", "necesidad", "identificador", "ruta_muerta", "sectores", "codigos", "municipio", "descargar", "tabla_pcaxis", "boe_sumario",
         "subvenciones_nif", "empresa_nif", "ckan_buscar", "ckan_filas", "socrata_filas", "almacen_sql"}


def payload(result):
    """Valor devuelto por la herramienta (mcp 1.x y 2.x): structured content si lo hay, si no el texto JSON."""
    if getattr(result, "is_error", None) or getattr(result, "isError", None):
        raise AssertionError(f"herramienta con error: {result.content[0].text}")
    structured = getattr(result, "structured_content", None) or getattr(result, "structuredContent", None)
    if isinstance(structured, dict):
        return structured["result"] if set(structured) == {"result"} else structured
    parts = [json.loads(c.text) for c in result.content]
    return parts[0] if len(parts) == 1 else parts


async def main() -> None:
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    dead = catalog["indices"]["rutas_muertas"][0]
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)], cwd=str(ROOT), env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            names = {t.name for t in (await session.list_tools()).tools}
            assert TOOLS <= names, f"faltan herramientas: {TOOLS - names}"
            print(f"herramientas: {', '.join(sorted(names))}")

            fuentes = payload(await session.call_tool("buscar_fuentes", {"consulta": "paro municipio"}))
            assert fuentes and fuentes[0]["id"] == "sepe-estadisticas", [f["id"] for f in fuentes]
            base = {"id", "name", "sector", "access", "auth", "status", "verified", "summary"}
            assert set(fuentes[0]) == base | {"alerts"} and fuentes[0]["alerts"], fuentes[0]  # sepe-estadisticas tiene alerts
            print("buscar_fuentes('paro municipio'):", [f["id"] for f in fuentes])

            filtradas = payload(await session.call_tool("buscar_fuentes", {"consulta": "precios", "sector": "energia", "limite": 3}))
            assert filtradas and all(f["sector"] == "energia" for f in filtradas)
            print("buscar_fuentes('precios', sector=energia):", [f["id"] for f in filtradas])

            f = payload(await session.call_tool("ficha", {"id": "ine-api-tempus"}))
            assert f["id"] == "ine-api-tempus" and f["endpoints"] and f["gotchas"]
            assert next(iter(f)) == "alerts" and f["alerts"], list(f)[:3]  # las alertas, lo primero
            print(f"ficha('ine-api-tempus'): {len(f['endpoints'])} endpoints, {len(f['gotchas'])} gotchas, verified {f['verified']}")

            missing = payload(await session.call_tool("ficha", {"id": "ine-tempus"}))
            assert "error" in missing and "ine-api-tempus" in missing["sugerencias"], missing
            print("ficha('ine-tempus'):", missing["sugerencias"])

            recetas = payload(await session.call_tool("buscar_recetas", {"consulta": "IPC último dato"}))
            assert recetas and recetas[0]["id"] == "ipc-ultimo-dato", [r["id"] for r in recetas]
            r = payload(await session.call_tool("receta", {"id": recetas[0]["id"]}))
            assert r["steps"] and "checks" not in r and {"intent", "inputs", "steps", "output", "verified"} <= set(r)
            print(f"receta('{r['id']}'): {len(r['steps'])} pasos, verified {r['verified']}")

            needs = payload(await session.call_tool("necesidad", {"consulta": "precio gasolina"}))
            assert needs and needs[0]["source"] == "minetur-precios-carburantes", needs
            print("necesidad('precio gasolina'):", needs[0]["need"], "->", needs[0]["source"])

            ident = payload(await session.call_tool("identificador", {"id": "ine-municipio"}))
            assert ident["regex"] and ident["joins"] and ident["used_by"]
            print(f"identificador('ine-municipio'): regex {ident['regex']}, {len(ident['joins'])} cruces")

            rm = payload(await session.call_tool("ruta_muerta", {"url": dead["old"]}))
            assert rm["rutas"] and rm["rutas"][0]["old"] == dead["old"] and rm["rutas"][0]["status"] == dead["status"]
            print(f"ruta_muerta('{dead['old']}'): {rm['rutas'][0]['status']} -> {rm['rutas'][0]['new']}")
            rm2 = payload(await session.call_tool("ruta_muerta", {"url": dead["old"].rstrip("/") + "/lo-que-sea"}))
            assert rm2["rutas"] and rm2["rutas"][0]["old"] == dead["old"], rm2
            rm3 = payload(await session.call_tool("ruta_muerta", {"url": "https://example.org/nada"}))
            assert rm3["rutas"] == [] and rm3["nota"], rm3
            print("ruta_muerta(desconocida):", rm3["nota"])

            grupos = payload(await session.call_tool("codigos", {}))
            prov = payload(await session.call_tool("codigos", {"grupo": "ine-provincias"}))
            assert any(e["code"] == "28" for e in prov["entries"]), prov
            print(f"codigos(): {len(grupos)} grupos; ine-provincias: {len(prov['entries'])} entradas")
            mun = payload(await session.call_tool("municipio", {"consulta": "28:900"}))
            assert mun[0]["ine"] == "28079" and mun[0]["dir3"] == "L01280796", mun
            alcala = payload(await session.call_tool("municipio", {"consulta": "Alcala de Henares"}))
            assert alcala[0]["ine"] == "28005" and alcala[0]["sigpac"] == "28:5", alcala
            print(f"municipio('28:900'): {mun[0]['nombre']} {mun[0]['ine']}; municipio('Alcala de Henares'): {alcala[0]['ine']}")
            d = payload(await session.call_tool("descargar", {"url": "https://www.boe.es/datosabiertos/api/boe/sumario/20240102", "max_caracteres": 200}))
            assert d["estado"] == 200 and d["formato"] == "json" and d["fichas"][0]["id"].startswith("boe"), d
            px = payload(await session.call_tool("tabla_pcaxis", {"tabla": "24077", "max_filas": 2}))
            assert px["columnas"][-1] == "Total" and px["filas"], px
            emp = payload(await session.call_tool("empresa_nif", {"nif": "Q1132001G", "max_filas": 1}))
            assert emp["sector_publico"]["codigoDir3"] == "U00500001" and emp["aei"]["total"] > 0, emp.get("error", emp.keys())
            print(f"empresa_nif('Q1132001G'): {emp['nombre']}, {emp['subvenciones']['concesiones']['total']} concesiones, {emp['aei']['total']} ayudas AEI")
            bloq = payload(await session.call_tool("descargar", {"url": "http://localhost:8080/"}))
            assert "error" in bloq, bloq
            alm = payload(await session.call_tool("almacen_sql", {"consulta": "select 1 as uno"}))
            assert alm.get("filas") == [[1]] or "almacén" in alm.get("error", ""), alm  # con o sin almacén local
            print(f"almacen_sql: {alm.get('filas') or alm['error']}")
            print(f"descargar: {d['formato']} con fichas {[f['id'] for f in d['fichas']][:2]}; tabla_pcaxis 24077: {px['filas'][0]}")
            secs = payload(await session.call_tool("sectores", {}))
            assert sum(s["sources"] for s in secs) == catalog["count"]
            print(f"sectores(): {len(secs)} sectores, {sum(s['sources'] for s in secs)} fichas")

            uris = {str(r.uri) for r in (await session.list_resources()).resources}
            assert {"catalogo://llms.txt", "catalogo://reglas"} <= uris, uris
            reglas = (await session.read_resource("catalogo://reglas")).contents[0].text
            assert reglas.startswith("## Reglas rápidas") and "## Dónde" not in reglas
            llms = (await session.read_resource("catalogo://llms.txt")).contents[0].text
            assert llms.startswith("# Administración fuentes públicas")
            print(f"recursos: reglas {len(reglas)} caracteres, llms.txt {len(llms)} caracteres")
    print("test_mcp_catalogo OK")


if __name__ == "__main__":
    asyncio.run(main())
