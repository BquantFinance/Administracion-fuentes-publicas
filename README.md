<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/logo-oscuro.svg">
    <img alt="fuentes públicas: datos públicos de España para agentes y devs" src=".github/assets/logo.svg" width="560">
  </picture>
</p>

# Administración fuentes públicas

[![CI](https://github.com/BquantFinance/Administracion-fuentes-publicas/actions/workflows/ci.yml/badge.svg)](https://github.com/BquantFinance/Administracion-fuentes-publicas/actions/workflows/ci.yml) [![Licencia CC0](https://img.shields.io/badge/licencia-CC0%201.0-blue)](LICENSE)

*Spanish public-sector data sources, catalogued for AI agents and developers: verified endpoints, response shapes, pitfalls, and recipes. Start at `llms.txt`.*

Catálogo de fuentes de datos de la Administración pública española para desarrolladores y agentes de IA: qué hay, dónde está, cómo se llama, qué devuelve y qué falla. Cada endpoint se prueba con una llamada real y cada trampa lleva la fecha en que se comprobó.

## Empieza aquí

- **Agente con MCP** (Claude, Cursor y cualquier cliente MCP): `uvx --from git+https://github.com/BquantFinance/Administracion-fuentes-publicas mcp-catalogo`, o [![Instalar en Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/link/mcp/install?name=catalogo-fuentes-publicas&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXQraHR0cHM6Ly9naXRodWIuY29tL0JxdWFudEZpbmFuY2UvQWRtaW5pc3RyYWNpb24tZnVlbnRlcy1wdWJsaWNhcyIsIm1jcC1jYXRhbG9nbyJdfQ%3D%3D). Carga solo la ficha que hace falta ([guía](guides/servidor-mcp.md)).
- **Agente sin MCP**: [`llms-min.txt`](llms-min.txt) (7 KB) o [`llms.txt`](llms.txt); todo el catálogo en [`catalog.json`](catalog.json) o [`llms-full.txt`](llms-full.txt).
- **Código**: cargadores en Python que ya resuelven las trampas en [`scripts/clientes/`](scripts/clientes/) (BOE y BORME, BDNS, AEMET, INE, PLACSP, DataComex, Saiku), probados contra respuestas reales.

## Lo que no dice la documentación oficial

Algunos ejemplos, verificados con llamadas reales:

- La API del BOE responde 400 si no envías `Accept: application/json`, y la forma del sumario cambia según el día.
- La exportación de la BDNS devuelve 50 filas aunque haya miles si no pasas `pageSize`, y no avisa.
- Para filtrar un municipio, el INE no quiere su código (`02001`) sino un Id interno (`6124`).
- Muchos servidores `.gob.es` envían el certificado FNMT sin la intermedia: el navegador entra, `curl` y `requests` fallan ([arreglo](guides/cliente-http.md)).
- AEMET responde en dos pasos, con el fichero en ISO-8859-15 y los errores dentro de un HTTP 200.

Fuentes catalogadas: <!-- AUTO:count -->85<!-- /AUTO:count -->. Alcance actual: Administración General del Estado. Después: comunidades autónomas, entidades locales, Cortes y Poder Judicial, Unión Europea.

## Principios

- **Una ficha por fuente**, en YAML, con campos fijos validados contra un esquema. Sin prosa de relleno: cada línea ahorra una búsqueda.
- **Fuente única de verdad.** Solo se editan `sources/**/*.yaml`. Índices, `catalog.json` y `llms*.txt` se generan.
- **Lo que no dice la documentación oficial.** El campo `gotchas` recoge los detalles que hacen perder horas: cabeceras obligatorias, codificaciones raras, límites no documentados, URLs que cambian.
- **Verificación explícita.** `verified` lleva la fecha de la última prueba real del endpoint, o `null`. Un job semanal comprueba que las URLs siguen respondiendo.
- **Top-down.** Se cubren primero las fuentes de mayor uso e impacto, sector a sector, hasta cubrirlo todo.

## Sectores

<!-- AUTO:sectors -->
| sector | descripción | fuentes |
|---|---|---|
| [legislacion-boletines](sources/legislacion-boletines/README.md) | Legislación y boletines oficiales | 5 |
| [economia-finanzas](sources/economia-finanzas/README.md) | Economía, finanzas y mercados | 5 |
| [hacienda-presupuestos](sources/hacienda-presupuestos/README.md) | Hacienda, tributos y presupuestos | 6 |
| [estadistica](sources/estadistica/README.md) | Estadística oficial | 3 |
| [contratacion-subvenciones](sources/contratacion-subvenciones/README.md) | Contratación pública y subvenciones | 3 |
| [empleo-seguridad-social](sources/empleo-seguridad-social/README.md) | Empleo y Seguridad Social | 3 |
| [gobierno-abierto-administracion](sources/gobierno-abierto-administracion/README.md) | Gobierno abierto, transparencia y organización administrativa | 5 |
| [territorio-cartografia](sources/territorio-cartografia/README.md) | Territorio, catastro y cartografía | 4 |
| [meteorologia-clima](sources/meteorologia-clima/README.md) | Meteorología y clima | 2 |
| [medio-ambiente-agua-biodiversidad](sources/medio-ambiente-agua-biodiversidad/README.md) | Medio ambiente, agua y biodiversidad | 5 |
| [energia](sources/energia/README.md) | Energía | 5 |
| [sanidad-medicamentos](sources/sanidad-medicamentos/README.md) | Sanidad y medicamentos | 5 |
| [ciencia-investigacion](sources/ciencia-investigacion/README.md) | Ciencia e investigación (biología, química, geología, oceanografía) | 7 |
| [agricultura-pesca-alimentacion](sources/agricultura-pesca-alimentacion/README.md) | Agricultura, pesca y alimentación | 4 |
| [transporte-movilidad](sources/transporte-movilidad/README.md) | Transporte y movilidad | 7 |
| [comercio-industria-propiedad](sources/comercio-industria-propiedad/README.md) | Comercio exterior, industria y propiedad industrial | 4 |
| [educacion-universidades](sources/educacion-universidades/README.md) | Educación y universidades | 2 |
| [justicia-interior-seguridad](sources/justicia-interior-seguridad/README.md) | Justicia, interior y seguridad | 1 |
| [cultura-patrimonio](sources/cultura-patrimonio/README.md) | Cultura y patrimonio | 2 |
| [demografia-migraciones-sociedad](sources/demografia-migraciones-sociedad/README.md) | Demografía, migraciones y sociedad | 4 |
| [vivienda-urbanismo](sources/vivienda-urbanismo/README.md) | Vivienda y urbanismo | 1 |
| [telecomunicaciones-digital](sources/telecomunicaciones-digital/README.md) | Telecomunicaciones y sociedad digital | 1 |
| `exterior-cooperacion` | Acción exterior y cooperación | 0 |
| [consumo-seguridad-alimentaria](sources/consumo-seguridad-alimentaria/README.md) | Consumo y seguridad alimentaria | 1 |
| `defensa` | Defensa | 0 |
<!-- /AUTO:sectors -->

## Estructura

```
sources/<sector>/<id>.yaml   fichas (fuente de verdad)
sources/<sector>/README.md   índice del sector (generado)
schema/source.schema.json    esquema de ficha
schema/vocab.yaml            vocabulario controlado: sectores, acceso, auth, formatos
catalog.json                 todo el catálogo (generado)
llms.txt / llms-full.txt     entrada para agentes (generado)
indices/*.yaml               recetas por intención, necesidades, identificadores, códigos que son parámetros, rutas muertas (fuente de verdad)
indices/README.md            los cinco índices en texto (generado)
scripts/                     validate.py, build.py, check_links.py, check_recetas.py, check_ejemplos.py, fnmt_bundle.py, mcp_catalogo.py (servidor MCP local)
scripts/clientes/            cargadores en Python que resuelven las trampas (BOE y BORME, BDNS, AEMET, INE, PLACSP, DataComex, Saiku)
scripts/clientes/muestras/   respuestas reales recortadas para probar los parsers sin red (python scripts/test_clientes.py)
evals/                       20 tareas con respuesta esperada para medir lo que aporta el repo a un agente
templates/source.yaml        plantilla de ficha
guides/                      guías transversales (identificadores para cruzar datasets, etc.)
```

## Uso rápido

```bash
# Todo el catálogo
curl -s https://raw.githubusercontent.com/BquantFinance/Administracion-fuentes-publicas/main/catalog.json

# Fuentes de un sector con API REST y sin autenticación
curl -s .../catalog.json | jq '.sources[] | select(.sector=="economia-finanzas" and (.access|index("api-rest")) and .auth=="none") | .id'
```

## Índices para agentes

Además de las fichas, `indices/` responde a las preguntas que se hacen antes de elegir una fuente:

- **Recetas por intención**: procedimientos verificados que encadenan fichas (de un NIF a sus subvenciones y contratos, de unas coordenadas a la referencia catastral, del sumario del BOE al texto consolidado). Cada receta lleva comprobaciones que `python scripts/check_recetas.py` ejecuta contra los servidores reales.
- **Dónde está cada cosa**: necesidades habituales con la ficha que las resuelve y la nota que evita el desvío típico.
- **Identificadores**: los códigos que cruzan datasets, con regex, ejemplo, emisor y vías verificadas de conversión.
- **Códigos que son parámetros**: valores que las APIs exigen y no se adivinan (Id del INE para `tv`, países de DataComex, estación de AEMET por capital, productos de carburantes, rangos del BOE), obtenidos con llamadas reales.
- **Rutas muertas**: URLs de documentación antigua que ya no sirven y su sustituta.

**Medido** ([evals/](evals/)): en diez tareas resueltas por el mismo agente con y sin catálogo (dos modelos), el acierto fue el mismo; con catálogo, en las tareas difíciles las llamadas HTTP y los pasos del agente bajan a la mitad y las fallidas casi a cero. El consumo de tokens está pendiente de medir bien: las dos primeras tandas registraron el contexto final de cada agente, no los tokens procesados en todos sus turnos.

Todo en [indices/README.md](indices/README.md) y, para consumo programático, bajo la clave `indices` de `catalog.json`. Cada endpoint principal de una ficha lleva `example` (llamada copiable) y `returns` (forma de la respuesta vista en esa llamada). `python scripts/mcp_catalogo.py` expone el catálogo por MCP en local para cargar solo lo necesario ([guía](guides/servidor-mcp.md)).

## Contribuir

Lee [CONTRIBUTING.md](CONTRIBUTING.md). Resumen: copia `templates/source.yaml`, rellena, ejecuta `python scripts/validate.py && python scripts/build.py`, abre un PR.

## Licencia

Catálogo y documentación: [CC0 1.0](LICENSE). Los datos a los que apuntan las fichas tienen cada uno su propia licencia, indicada en el campo `license`.
