# Ciencia e investigación (biología, química, geología, oceanografía)

Sector `ciencia-investigacion` · 6 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aei-convocatorias](aei-convocatorias.yaml) | AEI – Ayudas concedidas (CSV completo) y convocatorias de I+D+i | download, portal | none | csv, html, pdf | irregular | — | 2026-09-30 |
| [csic-digital](csic-digital.yaml) | Digital.CSIC – Repositorio institucional del CSIC (OAI-PMH) | oai-pmh, portal | none | xml, pdf | daily | waf-blocks-bots, js-rendered | 2026-09-30 |
| [fecyt-recolecta](fecyt-recolecta.yaml) | FECYT – RECOLECTA (agregador de repositorios) e ICONO | portal | none | html | irregular | waf-blocks-bots, url-drift | 2026-09-30 |
| [gbif-es](gbif-es.yaml) | GBIF España – Ocurrencias de biodiversidad (API global filtrada por España) | api-rest, download, portal | none | json, csv, zip | daily | waf-blocks-bots | 2026-09-30 |
| [igme-geologia](igme-geologia.yaml) | IGME-CSIC – Cartografía geológica, bases de datos geocientíficas y servicios ArcGIS | api-rest, ogc, download, portal | none | json, xml, shp, pdf, jpg, zip | irregular | js-rendered, url-drift | 2026-09-30 |
| [ign-sismologia](ign-sismologia.yaml) | IGN – Catálogo sísmico y últimos terremotos | portal, scraping | none | html, csv, txt, kml, geojson | realtime | js-rendered, session-required, url-drift | 2026-09-30 |

- **aei-convocatorias**: Todas las ayudas concedidas por la AEI desde 2008 (130.000 filas) en un CSV descargable con año, convocatoria, referencia, género del IP, área, título, CIF y entidad beneficiaria, CCAA, provincia e importe, más el buscador de convocatorias con sus páginas de detalle y estadísticas en PDF.
- **csic-digital**: Publicaciones, datasets y documentos científicos del CSIC en acceso abierto. Cosecha por OAI-PMH con trece formatos de metadatos (oai_dc, datacite, oai_cerif_openaire, mods, marc) y sets por instituto. La web y la API REST están tras un filtro antibots; OAI-PMH es la única vía automatizable.
- **fecyt-recolecta**: Agregador nacional de repositorios científicos de acceso abierto y observatorio de indicadores ICONO. En la verificación el endpoint OAI-PMH ya no existe, el buscador está tras un filtro antibots e ICONO no respondió; solo quedan las páginas informativas. Cosechar cada repositorio por separado.
- **gbif-es**: 95,8 millones de registros de presencia de especies en España (country=ES) y 666 datasets publicados por instituciones españolas, en Darwin Core, a través de la API global de GBIF (JSON, sin clave para consultar). El portal nacional y su API propia no son utilizables desde scripts.
- **igme-geologia**: Mapa geológico continuo GEODE 1:50.000 y decenas de capas más (hidrogeología, puntos de agua, minería, movimientos del terreno, fallas activas, geoquímica) consultables por ArcGIS REST (JSON, consultas espaciales y por atributos) y WMS, más las hojas MAGNA 50 descargables (vector, PDF, memoria).
- **ign-sismologia**: Terremotos localizados por la Red Sísmica Nacional: tablas HTML de los últimos 5, 10 y 30 días y del año (magnitud 1,5 o superior o sentidos) y catálogo histórico con formulario por fechas, zona, magnitud e intensidad, descargable en csv, kmz o geojson desde la web (no reproducido por script).
