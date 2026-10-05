#!/usr/bin/env python3
"""Cliente MCP de línea de órdenes para la condición MCP de la evaluación.

Arranca scripts/mcp_catalogo.py por stdio, llama a una herramienta o lee un recurso y escribe el resultado en JSON,
el mismo que recibe cualquier cliente MCP. Sirve para dar el catálogo a un agente que solo tiene Bash.

Uso:
  python evals/mcp_cli.py                                   lista herramientas, parámetros y recursos
  python evals/mcp_cli.py HERRAMIENTA [clave=valor ...]     llama a la herramienta (los enteros se convierten)
  python evals/mcp_cli.py recurso NOMBRE                    lee catalogo://NOMBRE (llms.txt o reglas)
Ejemplo: python evals/mcp_cli.py buscar consulta="paro municipio" limite=5
EVAL_SIN=h1,h2 oculta esas herramientas (condición sin las piezas que se miden; cuarta tanda).
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
SIN = {h for h in os.environ.get("EVAL_SIN", "").split(",") if h}


def argumentos(pares: list[str]) -> dict:
    args = {}
    for p in pares:
        clave, _, valor = p.partition("=")
        args[clave] = int(valor) if valor.lstrip("-").isdigit() else valor
    return args


async def main(argv: list[str]) -> None:
    if argv and argv[0] in SIN:
        sys.exit(f"herramienta desconocida: {argv[0]}")
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)], cwd=str(ROOT), env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            if not argv:
                tools = [t for t in (await session.list_tools()).tools if t.name not in SIN]
                print(json.dumps([{"herramienta": t.name, "descripcion": t.description,
                                   "parametros": t.inputSchema.get("properties", {})} for t in tools],
                                 ensure_ascii=False, indent=1))
                print(json.dumps({"recursos": [str(r.uri) for r in (await session.list_resources()).resources]},
                                 ensure_ascii=False))
                return
            if argv[0] == "recurso":
                res = await session.read_resource(f"catalogo://{argv[1]}")
                print("\n".join(c.text for c in res.contents))
                return
            result = await session.call_tool(argv[0], argumentos(argv[1:]))
            print("\n".join(c.text for c in result.content if getattr(c, "text", None)))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
