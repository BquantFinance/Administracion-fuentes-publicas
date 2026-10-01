# Legislación y boletines oficiales

Sector `legislacion-boletines` · 5 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Sumario diario del BOE con identificador y URLs de cada disposición → `boe-api-sumario`
- Texto consolidado, vigencia y versiones de una norma → `boe-api-legislacion-consolidada` (incluye normas autonómicas; los boletines autonómicos no están en el catálogo)
- URI estable de una norma para citar o enlazar → `boe-eli`
- Vigilar novedades del BOE, BORME, ayudas o licitaciones sin programar contra la API → `boe-feeds` (RSS en ISO-8859-1)
- Actos societarios inscritos en el Registro Mercantil → `borme-api-sumario` (sin búsqueda por empresa; recorrer días y provincias)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [boe-api-legislacion-consolidada](boe-api-legislacion-consolidada.yaml) | BOE – API de legislación consolidada | api-rest | none | json, xml | daily | accept-header-required, errors-html-or-xml | 2026-10-01 |
| [boe-api-sumario](boe-api-sumario.yaml) | BOE – API de sumarios | api-rest | none | json, xml, pdf, html | daily | accept-header-required, json-object-or-list, errors-html-or-xml, no-weekend-data | 2026-10-01 |
| [boe-eli](boe-eli.yaml) | ELI – Identificador Europeo de Legislación en el BOE | download | none | html, rdf | daily | — | 2026-10-01 |
| [boe-feeds](boe-feeds.yaml) | BOE y BORME – Feeds RSS | feed | none | rss, xml | daily | latin1 | 2026-10-01 |
| [borme-api-sumario](borme-api-sumario.yaml) | BORME – API de sumarios y actos mercantiles | api-rest, download | none | json, xml, pdf, html | daily | accept-header-required, json-object-or-list, errors-html-or-xml, no-weekend-data | 2026-10-01 |

- **boe-api-legislacion-consolidada**: Textos consolidados de normas estatales y autonómicas por bloques (artículos, disposiciones) con todas las versiones de cada bloque, metadatos, análisis (materias, referencias) y vigencia. Listado filtrable por fecha de actualización, búsqueda por título y tablas auxiliares de códigos.
- **boe-api-sumario**: Sumario diario del BOE en JSON o XML: todas las disposiciones y anuncios publicados cada día con identificador, título, sección, departamento, epígrafe y URLs de PDF, HTML y XML del texto completo de cada uno.
- **boe-eli**: URIs estables ELI para normas publicadas en el BOE, que resuelven a la página HTML de la norma con metadatos RDFa de la ontología eli embebidos, interoperables con EUR-Lex y otros boletines europeos.
- **boe-feeds**: Canales RSS 2.0 del sumario diario del BOE (completo o por sección), del BORME, de canales temáticos (ayudas, becas, convenios colectivos, sentencias del TC) y de anuncios de licitación por división CPV.
- **borme-api-sumario**: Sumario diario del Boletín Oficial del Registro Mercantil con los actos inscritos por provincia (constituciones, nombramientos, ceses, ampliaciones, disoluciones), otros actos y anuncios, con XML y PDF de cada documento.
