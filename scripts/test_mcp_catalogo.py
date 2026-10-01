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
TOOLS = {"buscar", "ficha", "codigos", "descargar", "tabla_pcaxis", "boe_sumario", "empresa_nif", "perfil_municipio",
         "coyuntura", "ckan_buscar", "ckan_filas", "socrata_filas", "almacen_sql"}

# Presupuestos en caracteres (unos 3,5 por token): lo que el agente paga en cada turno o en cada llamada típica.
PRESUPUESTO = {"definiciones": 6500, "buscar": 7000, "empresa_nif": 9000, "perfil_municipio": 4000, "tabla_pcaxis": 4000}


def medir(nombre: str, result) -> None:
    texto = "".join(c.text for c in result.content if hasattr(c, "text"))
    assert "\n  " not in texto, f"{nombre} devuelve JSON con sangría"
    if nombre in PRESUPUESTO:
        assert len(texto) < PRESUPUESTO[nombre], f"{nombre} ocupa {len(texto)} caracteres (presupuesto {PRESUPUESTO[nombre]})"


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
            lista = (await session.list_tools()).tools
            names = {t.name for t in lista}
            definiciones = sum(len(t.description or "") + len(json.dumps(t.inputSchema, ensure_ascii=False)) for t in lista)
            assert definiciones < PRESUPUESTO["definiciones"], f"las definiciones ocupan {definiciones} caracteres"
            print(f"definiciones: {definiciones} caracteres (presupuesto {PRESUPUESTO['definiciones']})")
            assert TOOLS <= names, f"faltan herramientas: {TOOLS - names}"
            print(f"herramientas: {', '.join(sorted(names))}")

            assert names == TOOLS, f"herramientas distintas: sobran {names - TOOLS}, faltan {TOOLS - names}"
            res = await session.call_tool("buscar", {"consulta": "paro municipio"})
            medir("buscar", res)
            b = payload(res)
            fuentes = b["fichas"]
            assert fuentes and fuentes[0]["id"] == "sepe-estadisticas", [f["id"] for f in fuentes]
            base = {"id", "name", "sector", "access", "auth", "status", "verified", "summary"}
            assert set(fuentes[0]) == base | {"alerts"} and fuentes[0]["alerts"], fuentes[0]  # sepe-estadisticas tiene alerts
            assert b["recetas"] and b["necesidades"] and b["identificadores"], list(b)
            print("buscar('paro municipio'):", {k: len(v) for k, v in b.items()})
            filtradas = payload(await session.call_tool("buscar", {"consulta": "precios", "sector": "energia", "limite": 3}))["fichas"]
            assert filtradas and all(f["sector"] == "energia" for f in filtradas)
            prod = payload(await session.call_tool("buscar", {"consulta": "licitaciones pymes"}))
            assert any(p["id"] == "radar-licitaciones" for p in prod.get("productos", [])), prod.get("productos")
            needs = payload(await session.call_tool("buscar", {"consulta": "precio gasolina"}))["necesidades"]
            assert needs[0]["source"] == "minetur-precios-carburantes", needs
            print("buscar('licitaciones pymes') productos:", [p["id"] for p in prod["productos"]])

            f = payload(await session.call_tool("ficha", {"id": "ine-api-tempus"}))
            assert f["id"] == "ine-api-tempus" and f["endpoints"] and f["gotchas"]
            assert next(iter(f)) == "alerts" and f["alerts"], list(f)[:3]  # las alertas, lo primero
            print(f"ficha('ine-api-tempus'): {len(f['endpoints'])} endpoints, {len(f['gotchas'])} gotchas, verified {f['verified']}")

            missing = payload(await session.call_tool("ficha", {"id": "ine-tempus"}))
            assert "error" in missing and "ine-api-tempus" in missing["sugerencias"], missing
            print("ficha('ine-tempus'):", missing["sugerencias"])

            recetas = payload(await session.call_tool("buscar", {"consulta": "IPC último dato"}))["recetas"]
            assert recetas and recetas[0]["id"] == "ipc-ultimo-dato", [r["id"] for r in recetas]
            r = payload(await session.call_tool("ficha", {"id": recetas[0]["id"]}))
            assert r["tipo"] == "receta" and r["steps"] and "checks" not in r and {"intent", "inputs", "steps", "output", "verified"} <= set(r)
            print(f"ficha('{r['id']}') de una receta: {len(r['steps'])} pasos, verified {r['verified']}")
            pr = payload(await session.call_tool("ficha", {"id": "radar-licitaciones"}))
            assert pr["tipo"] == "producto" and pr["trampa"] and pr["fuentes"], pr
            idf = payload(await session.call_tool("ficha", {"id": "ine-municipio"}))
            assert idf["tipo"] == "identificador" and idf["regex"] and idf["joins"], idf
            px2 = payload(await session.call_tool("tabla_pcaxis", {"tabla": "24077", "max_filas": 3}))
            assert isinstance(px2["filas"][0], list) and len(px2["filas"][0]) == len(px2["columnas"]), px2  # filas en columnas

            grupos = payload(await session.call_tool("codigos", {}))
            prov = payload(await session.call_tool("codigos", {"grupo": "ine-provincias"}))
            assert any(e["code"] == "28" for e in prov["entries"]), prov
            print(f"codigos(): {len(grupos)} grupos; ine-provincias: {len(prov['entries'])} entradas")
            mun = payload(await session.call_tool("perfil_municipio", {"municipio": "28:900", "solo_codigos": True}))["candidatos"]
            assert mun[0]["ine"] == "28079" and mun[0]["dir3"] == "L01280796", mun
            print(f"perfil_municipio('28:900', solo_codigos): {mun[0]['nombre']} {mun[0]['ine']}")
            rm = payload(await session.call_tool("descargar", {"url": dead["old"], "max_caracteres": 100}))
            assert rm.get("rutas_muertas") and rm["rutas_muertas"][0]["old"] == dead["old"], rm
            print(f"descargar(ruta muerta): sustituta {rm['rutas_muertas'][0]['new']}")
            d = payload(await session.call_tool("descargar", {"url": "https://www.boe.es/datosabiertos/api/boe/sumario/20240102", "max_caracteres": 200}))
            assert d["estado"] == 200 and d["formato"] == "json" and d["fichas"][0]["id"].startswith("boe"), d
            res = await session.call_tool("tabla_pcaxis", {"tabla": "24077", "max_filas": 50})
            medir("tabla_pcaxis", res)
            px = payload(res)
            assert px["columnas"][-1] == "Total" and px["filas"] and px["filas"][0][-1] is None, px  # 2026M09 aún sin dato
            res = await session.call_tool("empresa_nif", {"nif": "Q1132001G", "max_filas": 5})
            medir("empresa_nif", res)
            emp = payload(res)
            assert emp["sector_publico"]["codigoDir3"] == "U00500001" and emp["aei"]["total"] > 0, emp.get("error", emp.keys())
            print(f"empresa_nif('Q1132001G'): {emp['nombre']}, {emp['subvenciones']['concesiones']['total']} concesiones, {emp['aei']['total']} ayudas AEI")
            bloq = payload(await session.call_tool("descargar", {"url": "http://localhost:8080/"}))
            assert "error" in bloq, bloq
            co = payload(await session.call_tool("coyuntura", {}))
            assert co["ipc_variacion_anual"]["tipo"] in ("avance", "definitivo") and co["euribor_12m"]["valor"] > 0, co
            print(f"coyuntura(): IPC {co['ipc_variacion_anual']['periodo']} {co['ipc_variacion_anual']['valor']} ({co['ipc_variacion_anual']['tipo']}), prima {co['prima_riesgo'].get('valor')} pb")
            res = await session.call_tool("perfil_municipio", {"municipio": "02001"})
            medir("perfil_municipio", res)
            pm = payload(res)
            assert pm["municipio"]["nombre"] == "Abengibre" and pm["poblacion"]["habitantes"] > 0 and pm["paro_registrado"]["mes"], pm
            print(f"perfil_municipio('02001'): {pm['poblacion']['habitantes']:.0f} habitantes, paro {pm['paro_registrado']['mes']} {pm['paro_registrado']['total_paro_registrado']}")
            lote = payload(await session.call_tool("perfil_municipio", {"municipio": ["02001", "28005"]}))
            assert [x["municipio"]["ine"] for x in lote["perfiles"]] == ["02001", "28005"], lote
            emps = payload(await session.call_tool("empresa_nif", {"nif": ["B37033297", "A95758389"], "max_filas": 2}))
            assert len(emps["empresas"]) == 2 and emps["empresas"][1]["nif"] == "A95758389", emps
            print(f"lotes: 2 perfiles ({list(lote['perfiles'][0])[:3]}...), 2 empresas")
            alm = payload(await session.call_tool("almacen_sql", {"consulta": "select 1 as uno"}))
            assert alm.get("filas") == [[1]] or "almacén" in alm.get("error", ""), alm  # con o sin almacén local
            print(f"almacen_sql: {alm.get('filas') or alm['error']}")
            print(f"descargar: {d['formato']} con fichas {[f['id'] for f in d['fichas']][:2]}; tabla_pcaxis 24077: {px['filas'][0]}")

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
