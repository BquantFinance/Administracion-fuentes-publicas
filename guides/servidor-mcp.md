# Servidor MCP del catálogo

`scripts/mcp_catalogo.py` expone `catalog.json` por MCP (transporte stdio) para que un agente cargue solo la ficha,
la receta o la necesidad que le hace falta en vez de todo `llms.txt`. Necesita `catalog.json` generado
(`python scripts/build.py`); si falta, el servidor termina con un mensaje que lo indica. Instalación:
`pip install -r scripts/requirements.txt` (paquete `mcp`, funciona con 1.x y 2.x). Arranque manual:
`python scripts/mcp_catalogo.py` (habla JSON-RPC por stdin/stdout; normalmente lo lanza el cliente MCP).

Instalación en una línea, sin clonar el repo (descarga `catalog.json` y `llms.txt` de GitHub la primera vez y los
guarda en `~/.cache/fuentes-publicas`; con `CATALOGO_DIR` se usa una copia local):

```bash
pipx install git+https://github.com/BquantFinance/Administracion-fuentes-publicas   # o: uv tool install git+https://...
mcp-catalogo
```

Con `uvx` sin instalar nada: `uvx --from git+https://github.com/BquantFinance/Administracion-fuentes-publicas mcp-catalogo`.
En la configuración del cliente, `command` es entonces `mcp-catalogo` (o `uvx` con esos `args`) y no hace falta `cwd`.
Trampas verificadas el 2026-10-01: la forma `git+https` necesita `git` en el PATH (si no, uv falla con «Git executable not
found»); pipx 1.17 usa uv como motor si lo encuentra y exige uv 0.9.17 o posterior (con uno anterior,
`pipx install --backend pip git+...`). El paquete instala el mismo servidor con dos nombres, `mcp-catalogo` y
`fuentes-publicas-mcp`; el segundo es el que ejecutan los clientes que instalan desde el registro de MCP con uvx.

Cursor (mismo formato en `~/.cursor/mcp.json`, global, y en `.cursor/mcp.json` en la raíz de un proyecto; si Cursor no
encuentra `uvx`, poner su ruta absoluta en `command`):

```json
{
  "mcpServers": {
    "catalogo-fuentes-publicas": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "git+https://github.com/BquantFinance/Administracion-fuentes-publicas", "mcp-catalogo"]
    }
  }
}
```

[![Instalar en Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/link/mcp/install?name=catalogo-fuentes-publicas&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXQraHR0cHM6Ly9naXRodWIuY29tL0JxdWFudEZpbmFuY2UvQWRtaW5pc3RyYWNpb24tZnVlbnRlcy1wdWJsaWNhcyIsIm1jcC1jYXRhbG9nbyJdfQ%3D%3D)

Configuración para Claude Code (`.mcp.json` en el proyecto o `~/.claude.json`) y Claude Desktop
(`claude_desktop_config.json`), con la ruta absoluta del repo en `args` y `cwd`:

```json
{
  "mcpServers": {
    "catalogo-fuentes-publicas": {
      "command": "python",
      "args": ["/ruta/al/repo/Administracion-fuentes-publicas/scripts/mcp_catalogo.py"],
      "cwd": "/ruta/al/repo/Administracion-fuentes-publicas"
    }
  }
}
```

Herramientas (respuestas JSON compactas; búsqueda por palabras sin acentos ni mayúsculas):

- `buscar_fuentes(consulta, sector=None, limite=8)`: fichas que casan; devuelve id, name, sector, access, auth, status, verified, summary.
- `ficha(id)`: ficha completa (endpoints con ejemplo, quirks, ids, gotchas, tips); si el id no existe, hasta 5 parecidos.
- `buscar_recetas(consulta, limite=5)`: recetas por intención con las fichas que encadenan.
- `receta(id)`: intent, inputs, steps (source, do, example), output, note, verified.
- `necesidad(consulta, limite=5)`: entradas de "dónde está cada cosa" (need, source, note).
- `identificador(id)`: format, regex, example, issuer, gotcha, joins, used_by de un identificador del vocabulario.
- `ruta_muerta(url)`: busca la URL exacta o por prefijo en rutas muertas; devuelve status, sustituta, ficha y fecha.
- `codigos(grupo=None)`: códigos que son parámetros (INE, DataComex, AEMET, carburantes, BOE); sin grupo lista los grupos, con grupo sus entradas.
- `municipio(consulta, limite=5)`: los códigos de un municipio en cada sistema (INE con dígito de control, SIGPAC y
  Catastro, DIR3 y NIF del ayuntamiento, CCAA, provincia, NUTS3 y coordenadas de su capital) desde `datos/municipios.csv`;
  acepta código INE, SIGPAC (28:900), DIR3, NIF o nombre.
- `sectores()`: sectores con título y número de fichas.

Herramientas que traen datos (con red; usan `scripts/clientes/consulta.py`). Detrás de un proxy que intercepta TLS,
añadir a la configuración del cliente `"env": {"EXTRA_CA_BUNDLE": "/ruta/ca-del-proxy.pem"}`; el resto lo resuelve el servidor.


- `descargar(url, max_caracteres=20000, desde=0)`: cualquier URL pública con las CA de FNMT, User-Agent de navegador,
  reintentos, gzip sin anunciar y la codificación real; resume CSV (columnas, filas, primeras), JSON (claves), xlsx
  (hojas y primeras filas) y ZIP (ficheros), detecta páginas de bloqueo y, si el host es de una ficha, añade su id y
  sus alerts. Solo hosts públicos (rechaza localhost, redes privadas y metadatos de nube) y hasta 25 MB.
- `tabla_pcaxis(tabla, filtro=None, max_filas=200)`: tablas del INE (id o Tabla.htm), Interior, Educación y Cultura en
  filas con números convertidos; filtro por texto en cualquier campo (08019, un nombre, un periodo).
- `boe_sumario(fecha, diario="boe", seccion=None, texto=None)`: disposiciones del día del BOE o del BORME.
- `subvenciones_nif(nif)`: concesiones, ayudas de Estado, minimis y grandes beneficiarios de un NIF en la BDNS.
- `ckan_buscar(portal, texto)` y `ckan_filas(portal, recurso, filtros=None, limite=100)`: portales CKAN (comunidad-madrid,
  madrid, barcelona, gva, andalucia, cnmc, renfe o la URL de su API), paginando sin topes y con el total del datastore.
- `socrata_filas(conjunto, where=None, select=None, order=None, limite=100)`: datos de la Generalitat de Catalunya.

Recursos: `catalogo://llms.txt` (el fichero entero) y `catalogo://reglas` (solo las reglas rápidas antes de programar).

Prueba real sin CI: `python scripts/test_mcp_catalogo.py` arranca el servidor por stdio y llama a todas las herramientas.

## Registros

- Registro oficial de MCP: `io.github.BquantFinance/catalogo-fuentes-publicas`, descrito en `server.json`. Al publicar
  una release `vX.Y.Z` en GitHub (con la misma versión en `server.json`), `.github/workflows/publicar-mcp.yml` empaqueta `mcpb/` como
  `.mcpb` fijado a esa etiqueta, lo adjunta a una release de GitHub y publica la entrada en el registro por OIDC de GitHub:
  sin secretos ni cuentas externas. El registro admite paquetes MCPB alojados en releases de GitHub y exige su sha256, que
  el workflow calcula. PyPI es opcional (`uvx fuentes-publicas-mcp`, más corto) y exige al propietario una cuenta con 2FA.
- Glama: indexa el registro oficial; `glama.json` declara al mantenedor y `Dockerfile` construye la imagen que prueba.
- Smithery: el mismo `.mcpb` de la release (`npx -y @anthropic-ai/mcpb pack mcpb` en local); publicar exige cuenta en Smithery.

<!-- mcp-name: io.github.BquantFinance/catalogo-fuentes-publicas -->
