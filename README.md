<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/assets/logo-oscuro.svg">
    <img alt="fuentes públicas: datos públicos de España para agentes y devs" src=".github/assets/logo.svg" width="560">
  </picture>
</p>

# Administración fuentes públicas

[![CI](https://github.com/BquantFinance/Administracion-fuentes-publicas/actions/workflows/ci.yml/badge.svg)](https://github.com/BquantFinance/Administracion-fuentes-publicas/actions/workflows/ci.yml) [![Licencia CC0](https://img.shields.io/badge/licencia-CC0%201.0-blue)](LICENSE) [![Apoya en Ko-fi](https://img.shields.io/badge/Ko--fi-apoya%20el%20proyecto-FF5E5B?logo=ko-fi&logoColor=white)](https://ko-fi.com/gsnchez)

*Spanish public data, ready to build products on: where each dataset lives, how to call it, what it returns and the traps that change the numbers, verified with real calls; plus code that fetches it already solved. Start at `llms-min.txt` or the MCP server.*

Datos públicos de España listos para construir productos. Para cada fuente: dónde está, cómo pedirla, qué devuelve y qué falla, comprobado con llamadas reales, y código que ya trae el dato resuelto. Pensado para startups, desarrolladores y agentes de IA.

## Empieza aquí

- **Con un agente (MCP)**: `uvx --from git+https://github.com/BquantFinance/Administracion-fuentes-publicas mcp-catalogo`, [![Instalar en Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/link/mcp/install?name=catalogo-fuentes-publicas&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXQraHR0cHM6Ly9naXRodWIuY29tL0JxdWFudEZpbmFuY2UvQWRtaW5pc3RyYWNpb24tZnVlbnRlcy1wdWJsaWNhcyIsIm1jcC1jYXRhbG9nbyJdfQ%3D%3D), o en Claude Code `/plugin marketplace add BquantFinance/Administracion-fuentes-publicas` y `/plugin install fuentes-publicas@fuentes-publicas`. `buscar` encuentra la fuente, `ficha` da endpoints y trampas, y `perfil_municipio`, `coyuntura`, `empresa_nif` y el resto traen el dato ([herramientas](guides/servidor-mcp.md)).
- **Con código**: `pip install "fuentes-publicas-mcp @ git+https://github.com/BquantFinance/Administracion-fuentes-publicas"`. Clientes que ya resuelven certificados, codificaciones y paginación ([scripts/clientes](scripts/clientes/)), un almacén local en Parquet para lo que las APIs no dejan consultar ([guía](guides/almacen.md)) y [ejemplos](ejemplos/) que funcionan.
- **Leyendo**: [`llms-min.txt`](llms-min.txt) para orientarse y la ficha de cada fuente en [`sources/`](sources/).

## Qué puedes construir hoy

Cada producto con piezas que ya funcionan; frescura, volumen medido, licencia y la trampa que más cuesta en [indices/productos.yaml](indices/productos.yaml). Antes de vender: [licencias, cita y datos personales](guides/reutilizacion.md).

<!-- AUTO:productos -->
| producto | para quién | fichas | piezas |
|---|---|---|---|
| **radar-licitaciones** · Avisos de licitaciones nuevas por CPV, provincia u órgano de contratación | pymes y consultoras que licitan con la Administración | placsp-datos-abiertos, dir3-directorio | fuentes-radar con ejemplos/radar/ (aviso diario en GitHub Actions: issue, RSS y JSON; CPV, NUTS, importe y palabras); almacen.py sync --fuentes placsp para histórico y búsquedas |
| **inteligencia-competidores** · Quién gana los contratos de un sector u órgano, a qué importe y contra cuántas ofertas | empresas que licitan, analistas de contratación pública, periodistas | placsp-datos-abiertos | almacen.py (tabla placsp_adjudicaciones y vista adjudicaciones_ultimo); ejemplos/adjudicaciones.py; herramienta almacen_sql |
| **radar-ayudas** · Convocatorias de subvenciones nuevas que encajan con el perfil de una empresa (sector, región, tipo de beneficiario) | pymes, gestorías y consultoras de financiación pública | bdns-api, boe-api-sumario | fuentes-radar con ejemplos/radar/ (convocatorias nuevas por palabras y nivel, aviso diario); scripts/clientes/bdns.py (convocatorias y concesiones paginadas, altas por fecha de alta) |
| **kyb-proveedores** · Ficha de riesgo de un proveedor o cliente por NIF (ayudas, contratos, actos mercantiles, prohibiciones de contratar) | departamentos de compras, fintech de crédito, compliance | bdns-api, placsp-datos-abiertos, borme-api-sumario, hacienda-registro-licitadores | herramienta empresa_nif (por NIF o por nombre, que resuelve el NIF con el directorio de la BDNS) y ejemplos/empresa_nif.py; con almacén local añade contratos adjudicados y actos del BORME |
| **leads-sociedades-nuevas** · Sociedades recién constituidas por provincia y objeto social, con capital y domicilio | proveedores B2B (asesorías, bancos, software de gestión, seguros) | borme-api-sumario | fuentes-radar con ejemplos/radar/ (constituciones por provincia, objeto social y capital, aviso diario); almacen.py sync --fuentes borme para el histórico; empresa_nif con la denominación para el NIF |
| **informe-ubicacion** · Informe de una localización (población, renta, paro, alquiler, criminalidad) para inmobiliarias, retail y franquicias | inmobiliarias, cadenas de retail y franquicias, proptech | ine-api-tempus, sepe-estadisticas, interior-criminalidad, mivau-precios-vivienda-alquiler, catastro-ovc | herramienta perfil_municipio con el municipio, una dirección o «lat,lon» (CP, referencia catastral del portal) y ejemplos/mi_municipio.py; datos/municipios.csv para pasar entre códigos |
| **comparador-carburantes** · Gasolineras más baratas cerca y evolución de precios por estación para conductores y flotas | apps de movilidad, gestores de flotas, comparadores | minetur-precios-carburantes | ejemplos/carburante_cerca.py; almacen.py sync --fuentes carburantes para la serie diaria por estación |
| **monitor-regulatorio** · Avisos de normas nuevas o modificadas por materia y del texto vigente de un artículo | despachos, compliance, legaltech | boe-api-sumario, boe-api-legislacion-consolidada, boe-eli | fuentes-radar con ejemplos/radar/ (BOE por sección, departamento y palabras, aviso diario); scripts/clientes/boe.py (normas actualizadas ayer y versión vigente de un bloque) |
| **panel-macro** · Panel de coyuntura (IPC, paro, PIB, Euríbor, prima de riesgo) para fintech, medios y asesores | fintech, medios, asesores financieros | ine-api-tempus, bde-estadisticas | herramienta coyuntura (consulta.coyuntura); los 90 ZIP del Banco de España con descarga condicional para series completas |
| **precio-electricidad** · Precio de la electricidad por cuarto de hora para apps de ahorro, domótica y recarga de vehículos | apps de consumo, domótica, puntos de recarga | omie-mercado | ficha omie-mercado (ficheros marginalpdbc por día y ZIP anual) |
| **buscador-medicamentos** · Buscador de medicamentos con presentaciones, prospecto y problemas de suministro | farmacias, healthtech, apps de pacientes | aemps-cima-api | ficha aemps-cima-api (API REST JSON sin clave) |
| **agritech-parcelas** · Información de una parcela agrícola por coordenadas (uso, superficie, Red Natura, zonas vulnerables a nitratos) | agritech, cooperativas, aseguradoras agrarias | mapa-sigpac, catastro-ovc | perfil_municipio con «lat,lon» (recinto, uso, superficie y referencia catastral de la parcela, municipio INE); scripts/clientes/ogc.py (recintos por bbox siguiendo next) |
<!-- /AUTO:productos -->

## Lo que no dice la documentación oficial

Algunos ejemplos, comprobados con llamadas reales:

- La exportación de la BDNS devuelve 50 filas aunque haya miles si no pasas `pageSize`, y no avisa. Y para sincronizarla no sirve la fecha de concesión: las del 15/01/2025 se siguieron dando de alta hasta agosto de 2026 (el filtro bueno, `fechaRegInicio`, no está documentado).
- Para filtrar un municipio, el INE no quiere su código (`02001`) sino un Id interno (`6124`). En SIGPAC y Catastro, Madrid es `28:900`, no `28079`, y otros 4.448 municipios cambian de número ([tabla de equivalencias](datos/municipios.csv)).
- El IPC del último mes es un avance que se revisa, y el PIB que se publica es el corregido: 0,68 % trimestral en 2026T2 frente al 4,79 % de la serie sin corregir.
- En el CSV del paro registrado del SEPE, Oza-Cesuras sale con 0 parados y Cerdedo-Cotobade no aparece: sus datos van con los códigos de antes de la fusión.
- Muchos servidores `.gob.es` envían el certificado FNMT sin la intermedia: el navegador entra, `curl` y `requests` fallan ([arreglo](guides/cliente-http.md)).
- Los CSV de los portales PC-Axis llegan en UTF-8 aunque la cabecera diga ISO-8859-15, y el del SEPE en Windows-1252 aunque diga UTF-8.
- En GBIF la encina ibérica es sobre todo *Quercus rotundifolia* (1,3 millones de registros en España); preguntar por *Quercus ilex*, que es lo que devuelve el buscador de nombres, da 21.322 sin ningún aviso. Y 41,6 de sus 95,8 millones de registros en España son CC BY-NC.

Fuentes catalogadas: <!-- AUTO:count -->95<!-- /AUTO:count -->. Alcance actual: Administración General del Estado y, desde octubre de 2026, las cuatro comunidades más pobladas (Madrid, Cataluña, Andalucía y Comunitat Valenciana) y los ayuntamientos de Madrid y Barcelona. Después: resto de comunidades y entidades locales, Cortes y Poder Judicial, Unión Europea.

## Principios

- **Una ficha por fuente**, en YAML, con campos fijos validados contra un esquema. Sin prosa de relleno: cada línea ahorra una búsqueda.
- **Fuente única de verdad.** Solo se editan `sources/**/*.yaml`. Índices, `catalog.json` y `llms*.txt` se generan.
- **Lo que no dice la documentación oficial.** El campo `gotchas` recoge los detalles que hacen perder horas: cabeceras obligatorias, codificaciones raras, límites no documentados, URLs que cambian. Las trampas silenciosas, las que dan una cifra incompleta o distinta sin ningún error, van aparte en `alerts`, y el servidor MCP las devuelve lo primero.
- **Verificación explícita.** `verified` lleva la fecha de la última prueba real del endpoint, o `null`. Un job semanal comprueba que las URLs siguen respondiendo.
- **Top-down.** Se cubren primero las fuentes de mayor uso e impacto, sector a sector, hasta cubrirlo todo.

## Sectores

<!-- AUTO:sectors -->
| sector | descripción | fuentes |
|---|---|---|
| [legislacion-boletines](sources/legislacion-boletines/README.md) | Legislación y boletines oficiales | 5 |
| [economia-finanzas](sources/economia-finanzas/README.md) | Economía, finanzas y mercados | 5 |
| [hacienda-presupuestos](sources/hacienda-presupuestos/README.md) | Hacienda, tributos y presupuestos | 6 |
| [estadistica](sources/estadistica/README.md) | Estadística oficial | 7 |
| [contratacion-subvenciones](sources/contratacion-subvenciones/README.md) | Contratación pública y subvenciones | 3 |
| [empleo-seguridad-social](sources/empleo-seguridad-social/README.md) | Empleo y Seguridad Social | 3 |
| [gobierno-abierto-administracion](sources/gobierno-abierto-administracion/README.md) | Gobierno abierto, transparencia y organización administrativa | 11 |
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
llms-min.txt, llms.txt, llms-full.txt   entrada para agentes, de menos a más (generado)
indices/*.yaml               productos, recetas por intención, necesidades, identificadores, códigos que son parámetros, rutas muertas (fuente de verdad)
indices/README.md            los seis índices en texto (generado)
ejemplos/                    proyectos pequeños que funcionan (carburante, BOE, licitaciones, municipio, subvenciones)
plugins/, .claude-plugin/    plugin de Claude Code con la skill y el servidor MCP
datos/municipios.csv         los 8.132 municipios con su código INE, Id del INE Tempus, SIGPAC y Catastro, DIR3, NIF, NUTS3 y coordenadas (scripts/municipios.py)
scripts/                     validate.py, build.py, check_links.py, check_recetas.py, check_ejemplos.py, fnmt_bundle.py, mcp_catalogo.py (servidor MCP local)
scripts/clientes/            sesión HTTP, clientes CKAN, Socrata, PC-Axis, ArcGIS y OGC, cargadores (BOE y BORME, BDNS, AEMET, INE, PLACSP, DataComex, Saiku) y almacén local en Parquet
scripts/clientes/muestras/   respuestas reales recortadas para probar los parsers sin red (python scripts/test_clientes.py)
evals/                       24 tareas con respuesta esperada para medir lo que aporta el repo a un agente
templates/source.yaml        plantilla de ficha
guides/                      guías transversales (cliente HTTP, identificadores, servidor MCP, reutilización y datos personales, almacén)
```

## Uso rápido

```bash
# Todo el catálogo
curl -s https://raw.githubusercontent.com/BquantFinance/Administracion-fuentes-publicas/main/catalog.json

# Fuentes de un sector con API REST y sin autenticación
curl -s .../catalog.json | jq '.sources[] | select(.sector=="economia-finanzas" and (.access|index("api-rest")) and .auth=="none") | .id'
```

```python
# pip install "fuentes-publicas-mcp @ git+https://github.com/BquantFinance/Administracion-fuentes-publicas"
from fuentes_publicas.clientes import ckan, socrata, pcaxis, arcgis, ogc
from fuentes_publicas.clientes.sesion import sesion  # requests.Session con FNMT, User-Agent, reintentos y bloqueos

pcaxis.tabla(24077)[:3]                 # IPC del INE en CSV: UTF-8 real, coma decimal y periodo sin dato como None
list(socrata.filas("gn9e-3qhr"))        # 87.930 filas de la Generalitat, no las 1.000 que da Socrata sin $limit
list(ckan.filas("cnmc", rid))           # todas las filas del datastore aunque el portal recorte limit a 32.000
ckan.comparar("comunidad-madrid", rec)  # el datastore del padrón tiene 5.000 filas; el CSV, 18.718
```

## Índices para agentes

Además de las fichas, `indices/` responde a las preguntas que se hacen antes de elegir una fuente:

- **Productos**: qué se puede construir hoy, para quién y con qué piezas.
- **Recetas por intención**: procedimientos verificados que encadenan fichas (de un NIF a sus subvenciones y contratos, de unas coordenadas a la referencia catastral, del sumario del BOE al texto consolidado). Cada receta lleva comprobaciones que `python scripts/check_recetas.py` ejecuta contra los servidores reales.
- **Dónde está cada cosa**: necesidades habituales con la ficha que las resuelve y la nota que evita el desvío típico.
- **Identificadores**: los códigos que cruzan datasets, con regex, ejemplo, emisor y vías verificadas de conversión.
- **Códigos que son parámetros**: valores que las APIs exigen y no se adivinan (Id del INE para `tv`, países de DataComex, estación de AEMET por capital, productos de carburantes, rangos del BOE), obtenidos con llamadas reales.
- **Rutas muertas**: URLs de documentación antigua que ya no sirven y su sustituta.

**Medido** ([evals/](evals/)): en diez tareas resueltas por el mismo agente con y sin catálogo (dos modelos), el acierto fue el mismo; con catálogo, en las tareas difíciles las llamadas HTTP y los pasos del agente bajan a la mitad y las fallidas casi a cero. En tareas con trampas silenciosas y un modelo pequeño (Haiku, tres repeticiones, tokens medidos turno a turno), el acierto pasa de 3 de 21 sin catálogo a 13 de 21 con el servidor MCP, con un 43 % menos de tokens; con las alertas, las trampas que aún fallaban pasan de 5 a 18 de 18.

Todo en [indices/README.md](indices/README.md) y, para consumo programático, bajo la clave `indices` de `catalog.json`. Cada endpoint principal de una ficha lleva `example` (llamada copiable) y `returns` (forma de la respuesta vista en esa llamada). `python scripts/mcp_catalogo.py` expone el catálogo por MCP en local para cargar solo lo necesario ([guía](guides/servidor-mcp.md)).

## Contribuir

Lee [CONTRIBUTING.md](CONTRIBUTING.md). Resumen: copia `templates/source.yaml`, rellena, ejecuta `python scripts/validate.py && python scripts/build.py`, abre un PR.

## Licencia

Catálogo y documentación: [CC0 1.0](LICENSE). Los datos a los que apuntan las fichas tienen cada uno su propia licencia, indicada en el campo `license`.
