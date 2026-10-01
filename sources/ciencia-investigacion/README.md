# Ciencia e investigación (biología, química, geología, oceanografía)

Sector `ciencia-investigacion` · 7 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Presencia de especies (ocurrencias, datasets de biodiversidad) → `gbif-es`
- Ayudas de investigación concedidas por la AEI → `aei-convocatorias`
- Publicaciones científicas en acceso abierto → `csic-digital` (OAI-PMH; RECOLECTA (fecyt-recolecta) ya no expone OAI)
- Producción científica española por CCAA y país (Scopus, WoS) y percepción social de la ciencia → `fecyt-recolecta` (CSV y xlsx en indicadores.fecyt.es/data/; icono.fecyt.es ya no resuelve)
- Geología, hidrogeología, puntos de agua y minería → `igme-geologia`
- Terremotos recientes y catálogo sísmico → `ign-sismologia` (GeoJSON de 30 días en el JavaScript del visor (todos_visualizadores.js); catálogo por script imitando al navegador)
- Campañas oceanográficas y datasets del IEO (catálogo de metadatos) → `ieo-datos-oceanograficos` (solo catálogo (CSW y Elasticsearch); los datos se piden en SeaDataNet y erddap.ieo.es no resuelve)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aei-convocatorias](aei-convocatorias.yaml) | AEI – Ayudas concedidas (CSV completo) y convocatorias de I+D+i | download, portal | none | csv, html, pdf | irregular | static-html, url-drift | 2026-10-01 |
| [csic-digital](csic-digital.yaml) | Digital.CSIC – Repositorio institucional del CSIC (OAI-PMH) | oai-pmh, portal | none | xml, pdf | daily | waf-blocks-bots, js-rendered | 2026-10-01 |
| [fecyt-recolecta](fecyt-recolecta.yaml) | FECYT – RECOLECTA (agregador de repositorios) e indicadores de ciencia | download, portal | none | csv, xlsx, html | irregular | waf-blocks-bots, js-rendered, url-drift | 2026-10-01 |
| [gbif-es](gbif-es.yaml) | GBIF España – Ocurrencias de biodiversidad (API global filtrada por España) | api-rest, download, feed, portal | none | json, csv, zip, rss | daily | waf-blocks-bots | 2026-10-01 |
| [ieo-datos-oceanograficos](ieo-datos-oceanograficos.yaml) | IEO (CSIC) – Centro Nacional de Datos Oceanográficos (catálogo CSW) | ogc, api-rest, portal | none | xml, json | irregular | errors-html-or-xml, js-rendered | 2026-10-01 |
| [igme-geologia](igme-geologia.yaml) | IGME-CSIC – Cartografía geológica, bases de datos geocientíficas y servicios ArcGIS | api-rest, ogc, download, portal | none | json, geojson, xml, pdf, jpg, zip | irregular | js-rendered, url-drift | 2026-10-01 |
| [ign-sismologia](ign-sismologia.yaml) | IGN – Catálogo sísmico y últimos terremotos | download, portal, scraping | none | geojson, html, csv, txt, kml, zip | realtime | js-rendered, session-required, url-drift | 2026-10-01 |

- **aei-convocatorias**: Todas las ayudas concedidas por la AEI desde 2008 (130.388 filas) en CSV con año de convocatoria, convocatoria, referencia, género del IP, área, título, CIF y entidad, CCAA, provincia e importe, filtrable por URL y con resumen del proyecto, más el buscador de convocatorias y sus resoluciones en PDF.
- **csic-digital**: Publicaciones, datasets y documentos del CSIC (413.998 registros el 01/10/2026), con texto completo abierto cuando lo hay. Cosecha por OAI-PMH con trece formatos de metadatos (oai_dc, dim, datacite, oai_cerif_openaire) y sets por instituto y colección; la web y la API REST tienen filtro antibots.
- **fecyt-recolecta**: Agregador nacional de repositorios de acceso abierto (RECOLECTA) y plataforma de indicadores de FECYT. RECOLECTA ya no expone OAI-PMH y su buscador tiene filtro antibots; los indicadores (producción Scopus y WoS por CCAA y país, percepción social, cultura científica) se descargan en CSV y XLSX.
- **gbif-es**: 95,8 millones de registros de especies en España (country=ES) y 666 datasets publicados desde España, en Darwin Core, por la API global de GBIF (JSON, sin clave), más la API del portal nacional (registros-ws.gbif.es, 59,8 millones) y el IPT del nodo con los DwC-A de 603 recursos.
- **ieo-datos-oceanograficos**: Catálogo GeoNetwork del centro de datos oceanográficos del IEO con 7.582 registros (sobre todo campañas, más corrientes, batimetrías, datasets y series) por CSW 2.0.2 (listado y metadato ISO 19139) y por la API Elasticsearch de GeoNetwork. Los datos se piden en SeaDataNet; erddap.ieo.es no resuelve.
- **igme-geologia**: Mapa geológico continuo GEODE 1:50.000, MAGNA 50 vectorial y decenas de capas más (puntos de agua, minería, movimientos del terreno, fallas activas, geoquímica, catálogo sísmico IGN-UPM) consultables por ArcGIS REST (JSON y GeoJSON) y WMS, más las hojas MAGNA 50 en imagen, PDF y memoria.
- **ign-sismologia**: Terremotos de la Red Sísmica Nacional en el GeoJSON del visor (30 últimos días, todas las magnitudes; Canarias, Antártida y mundiales aparte), tablas HTML de N días (magnitud 1,5 o más o sentidos) y catálogo desde 1370 con búsqueda y descarga en CSV, reproducibles por script imitando el navegador.
