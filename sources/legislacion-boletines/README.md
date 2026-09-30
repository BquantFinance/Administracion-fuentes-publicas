# Legislación y boletines oficiales

Sector `legislacion-boletines` · 5 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | verificada |
|---|---|---|---|---|---|---|
| [boe-api-legislacion-consolidada](boe-api-legislacion-consolidada.yaml) | BOE – API de legislación consolidada | api-rest | none | json, xml | daily | — |
| [boe-api-sumario](boe-api-sumario.yaml) | BOE – API de sumarios | api-rest | none | json, xml | daily | — |
| [boe-eli](boe-eli.yaml) | ELI – Identificador Europeo de Legislación en el BOE | download | none | html, rdf | daily | — |
| [boe-feeds](boe-feeds.yaml) | BOE y BORME – Feeds RSS y alertas | feed | none | rss, xml | daily | — |
| [borme-api-sumario](borme-api-sumario.yaml) | BORME – API de sumarios y actos mercantiles | api-rest, download | none | json, xml, pdf | daily | — |

- **boe-api-legislacion-consolidada**: Textos consolidados de normas estatales y autonómicas con estructura por artículos, versiones históricas, metadatos, análisis jurídico (materias, referencias anteriores y posteriores) y estado de vigencia.
- **boe-api-sumario**: Sumario diario del BOE en JSON/XML: todas las disposiciones publicadas cada día con identificador, título, sección, departamento y enlaces a PDF, HTML y XML del texto completo.
- **boe-eli**: URIs estables tipo ELI para normas estatales, con metadatos RDFa embebidos en las páginas de legislación consolidada, interoperables con EUR-Lex y otros boletines europeos.
- **boe-feeds**: Canales RSS del sumario diario del BOE por secciones y del BORME, útiles para detectar publicaciones nuevas sin consultar la API.
- **borme-api-sumario**: Sumario diario del Boletín Oficial del Registro Mercantil: actos inscritos por provincia (constituciones, nombramientos, ceses, ampliaciones, disoluciones), anuncios y convocatorias, con enlaces a PDF y XML.
