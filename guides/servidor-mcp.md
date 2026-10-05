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

Herramientas (lista generada por `scripts/build.py` desde `scripts/mcp_catalogo.py`; respuestas JSON compactas y
búsqueda sin acentos ni mayúsculas). Las que traen datos usan la red; detrás de un proxy que intercepta TLS, añadir a
la configuración del cliente `"env": {"EXTRA_CA_BUNDLE": "/ruta/ca-del-proxy.pem"}`.

<!-- AUTO:herramientas -->
- `buscar(consulta, sector=None, limite=5)`: Busca a la vez fichas (resumen y alerts), recetas que cruzan fuentes, necesidades con la ficha que las resuelve, productos que se pueden construir e identificadores. Devuelve un índice ligero; el detalle, con ficha(id).
- `ficha(id)`: Detalle de cualquier id de buscar: fuente (alerts primero, endpoints con ejemplo y respuesta, sync, gotchas), receta (pasos), producto (piezas, frescura, licencia, trampa) o identificador (regex, cruces). Si no existe, ids parecidos.
- `codigos(grupo=None)`: Códigos que una API exige y no se adivinan (Id del INE para tv, países de DataComex, estaciones de AEMET, productos de carburantes, rangos del BOE). Sin grupo, la lista de grupos; con grupo, sus entradas.
- `descargar(url, max_caracteres=20000, desde=0)`: Descarga una URL pública resolviendo certificados FNMT, User-Agent, reintentos, gzip y codificación, y la resume (CSV, JSON, xlsx o ZIP). Avisa de bloqueos de WAF, añade las alerts de la ficha del host y la sustituta si la URL está muerta. Hasta 25 MB. Para cuando tu fetch falle con un .gob.es o para ver qué devuelve una URL.
- `tabla_pcaxis(tabla, filtro=None, max_filas=200)`: Tabla PC-Axis en filas con números ya convertidos (None es dato no disponible o secreto, no cero): id de tabla del INE (24077), URL Tabla.htm del INE, Interior, Educación o Cultura, o URL del fichero. filtro deja las filas con ese texto en algún campo (código INE como 08019, nombre, periodo).
- `boe_sumario(fecha, diario='boe', seccion=None, texto=None, max_items=200)`: Disposiciones de un día del BOE (diario=boe) o del BORME (diario=borme); fecha AAAA-MM-DD. Filtra por código de sección (1, 2A, 2B, 3, 4, 5A) y por texto en el título. Domingos y festivos no hay boletín.
- `empresa_nif(nif, max_filas=5)`: Lo público de una empresa o entidad por NIF: si es sector público (con DIR3), subvenciones, ayudas de Estado y minimis con totales (BDNS), ayudas de la AEI y prohibiciones de contratar; con almacén local, contratos adjudicados y actos del BORME. Con un nombre en vez de NIF, candidatos con su NIF (directorio de la BDNS y del almacén, sin personas físicas), o el perfil si uno coincide exacto. Con una lista de hasta 10, todos en una llamada.
- `coyuntura()`: Último dato de coyuntura de España con periodo, serie y fuente: IPC (marcando si es avance), paro EPA, PIB corregido, paro registrado, Euríbor, dólar, deuda PDE, bono a 10 años y prima de riesgo.
- `perfil_municipio(municipio, solo_codigos=False)`: Un municipio (nombre, código INE, SIGPAC, DIR3 o NIF) o el de una dirección («calle Alcalá 50, Madrid») o «lat,lon» en una llamada: sus códigos en cada sistema (SIGPAC y Catastro numeran distinto que el INE), padrón, renta media, paro y contratos del año por mes, criminalidad, viviendas turísticas (INE y registro autonómico) y compraventas y valor tasado de vivienda; con dirección o coordenadas, además ubicacion (CP, coordenadas y referencia catastral del portal; exacta=false si la calle hallada no es la pedida; en el campo, recinto SIGPAC, uso y referencia de la parcela). solo_codigos=True da solo los códigos y la ubicación. Con una lista de hasta 20, en una llamada.
- `almacen_sql(consulta, limite=100)`: SQL de solo lectura (DuckDB) sobre el almacén local en Parquet si existe: tablas boe, borme, bdns, placsp, placsp_adjudicaciones y carburantes, y vistas placsp_ultimo y adjudicaciones_ultimo (último estado). Devuelve columnas, filas y cobertura; sin almacén, cómo crearlo.
- `ckan_buscar(portal, texto, limite=10)`: Conjuntos de un portal CKAN con sus recursos (id, formato, si tiene datastore, url de descarga). portal: comunidad-madrid, madrid, barcelona, gva, andalucia, cnmc, renfe o la URL de su /api/3/action.
- `ckan_filas(portal, recurso, filtros=None, limite=100)`: Filas del datastore de un recurso CKAN con filtros por igualdad ({"Territorio": "Madrid"}), paginando sin el tope silencioso del portal. Devuelve total_datastore: compáralo con el fichero antes de dar un total.
- `socrata_filas(conjunto, where=None, select=None, order=None, limite=100)`: Filas de un conjunto de la Generalitat de Catalunya (analisi.transparenciacatalunya.cat, id como gn9e-3qhr) con SoQL; números ya convertidos. Los nombres de campo van sin caracteres no ASCII (estaci por Estació).
<!-- /AUTO:herramientas -->

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
