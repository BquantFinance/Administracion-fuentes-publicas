#!/usr/bin/env python3
"""Cliente MCP de línea de órdenes para la condición MCP de la evaluación.

Arranca scripts/mcp_catalogo.py por stdio, llama a una herramienta o lee un recurso y escribe el resultado en JSON,
el mismo que recibe cualquier cliente MCP. Sirve para dar el catálogo a un agente que solo tiene Bash.

Uso:
  python evals/mcp_cli.py                                   instrucciones del servidor, herramientas, parámetros y recursos
  python evals/mcp_cli.py HERRAMIENTA [clave=valor ...]     llama a la herramienta (los enteros se convierten)
  python evals/mcp_cli.py recurso NOMBRE                    lee catalogo://NOMBRE (llms.txt o reglas)
Ejemplo: python evals/mcp_cli.py buscar consulta="paro municipio" limite=5
EVAL_SIN=h1,h2 oculta esas herramientas (condición sin las piezas que se miden; cuarta tanda) y EVAL_SIN=h.bloque quita ese
bloque de la respuesta de h (perfil_municipio.cerca; quinta tanda; sin el código de las fichas, ficha.code,buscar.code).
Las instrucciones salen sin las frases que nombran algo oculto, como haría un cliente MCP con un servidor sin esas piezas.
"""
import asyncio
import json
import os
import re
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent.parent
SERVER = ROOT / "scripts" / "mcp_catalogo.py"
SIN = {h for h in os.environ.get("EVAL_SIN", "").split(",") if h and "." not in h}
BLOQUES: dict[str, set] = {}
for _h in os.environ.get("EVAL_SIN", "").split(","):
    if "." in _h:
        BLOQUES.setdefault(_h.split(".")[0], set()).add(_h.split(".", 1)[1])


def sin_bloques(herramienta: str, texto: str) -> str:
    """Quita de la respuesta JSON los bloques ocultos (también dentro de perfiles, en las llamadas con lista)."""
    quitar = BLOQUES.get(herramienta)
    if not quitar:
        return texto
    try:
        d = json.loads(texto)
    except ValueError:
        return texto

    def limpia(x):
        if isinstance(x, dict):
            return {k: limpia(v) for k, v in x.items() if k not in quitar}
        if isinstance(x, list):
            return [limpia(v) for v in x]
        return x
    return json.dumps(limpia(d), ensure_ascii=False, separators=(",", ":"))


def sin_frases(texto: str) -> str:
    """Instrucciones sin lo oculto: el nombre se quita de las enumeraciones («perfil_municipio, coyuntura» da «coyuntura»)
    y la frase que aún lo nombre se quita entera (con EVAL_SIN=ficha.code no se anuncia code)."""
    ocultos = SIN | {b for bs in BLOQUES.values() for b in bs}
    texto = texto or ""
    for o in ocultos:
        texto = re.sub(rf"\b{re.escape(o)}, |, {re.escape(o)}\b", "", texto)
    frases = re.split(r"(?<=\.) ", texto)
    return " ".join(f for f in frases if not any(re.search(rf"\b{re.escape(o)}\b", f) for o in ocultos))


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
            init = await session.initialize()
            if not argv:
                # lo primero que ve un cliente MCP real: las instrucciones del servidor (antes no salían y la evaluación
                # medía el descubrimiento peor de lo que es)
                print(json.dumps({"instrucciones": sin_frases(init.instructions)}, ensure_ascii=False))
                tools = [t for t in (await session.list_tools()).tools if t.name not in SIN]
                print(json.dumps([{"herramienta": t.name, "descripcion": t.description + (
                                   f" (En esta sesión no devuelve: {', '.join(sorted(BLOQUES[t.name]))}.)" if t.name in BLOQUES else ""),
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
            print(sin_bloques(argv[0], "\n".join(c.text for c in result.content if getattr(c, "text", None))))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
