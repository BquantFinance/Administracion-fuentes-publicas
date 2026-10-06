# Territorio, catastro y cartografía

Sector `territorio-cartografia` · 6 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Datos de un inmueble o parcela por referencia catastral, dirección o coordenadas → `catastro-ovc` (bloqueo por IP tras ráfagas de unas 15 peticiones)
- Parcelario, edificios y direcciones vectoriales por municipio (INSPIRE) → `catastro-ovc`
- Ortofotos PNOA, modelos del terreno, LiDAR y límites municipales → `cnig-centro-descargas` (descargas con reCAPTCHA; WMS, WMTS y WFS sin restricción)
- Geocodificar una dirección y obtener su código INE, código postal o referencia catastral del portal → `cnig-centro-descargas` (geocoder CartoCiudad, desde la nube (el Catastro no); ignora el municipio escrito en q y devuelve la calle más parecida sin aviso; perfil_municipio con la dirección (consulta.ubicar) pasa municipio_filter y marca exacta)
- Geometría de secciones censales, distritos y municipios por año → `ine-cartografia-censal` (shapefile anual o API OGC del INE con filtro CQL; límites municipales del IGN sin reCAPTCHA en api-features.ign.es (idee-servicios))
- Localizar cualquier servicio WMS, WFS o CSW de una Administración → `idee-servicios`
- Carreteras y ferrocarril oficiales en vectorial → `idee-servicios` (GeoJSON en api-features.idee.es (roadlink, railwaylink); el WFS transportes de servicios.idee.es solo da GML)
- Ríos, embalses y cuencas en vectorial → `idee-servicios` (GeoJSON en api-features.idee.es (watercourse); el WFS hidrografia da GML)
- Ocupación del suelo SIOSE por polígono → `idee-servicios` (110 millones de polígonos en el WFS ocupacion-suelo; sin count no responde)
- Altitud o modelo digital del terreno de una zona → `idee-servicios` (WCS mdt con GetCoverage y SUBSET devuelve GeoTIFF; WMTS mdt para visualizar)
- Buscar un topónimo → `idee-servicios` (api-features.ign.es/collections/namedplace/items?etiqueta={nombre} en GeoJSON; el geocoder de direcciones está en cnig-centro-descargas)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [cartografia-jcyl](cartografia-jcyl.yaml) | Cartografía de Castilla y León – Portal y FTP de descargas (ITACyL) | download, portal | none | laz, shp, pdf, txt | irregular | — | 2026-10-05 |
| [catastro-ovc](catastro-ovc.yaml) | Catastro – Servicios web de la Oficina Virtual (OVC) e INSPIRE | api-rest, ogc, download | none | json, xml, gml, zip, png | daily | latin1, waf-temporary-ban | 2026-10-01 |
| [cnig-centro-descargas](cnig-centro-descargas.yaml) | IGN/CNIG – Centro de Descargas, servicios OGC y geocoder CartoCiudad | ogc, api-rest, download, portal | none | shp, gpkg, geotiff, laz, gml, geojson, json, png | irregular | captcha-required, js-rendered, static-html, errors-html-or-xml, soft-errors-200 | 2026-10-05 |
| [idecyl-servicios](idecyl-servicios.yaml) | IDECyL – Catálogo GeoNetwork y servicios ArcGIS REST de Castilla y León | ogc, api-rest, feed, portal | none | xml, json | irregular | js-rendered | 2026-10-05 |
| [idee-servicios](idee-servicios.yaml) | IDEE – Catálogos CSW y servicios INSPIRE del IGN (WFS, WMS, WMTS, WCS) | ogc, api-rest, portal | none | xml, json, gml, geojson, png, jpg, geotiff | irregular | static-html, errors-html-or-xml | 2026-10-01 |
| [ine-cartografia-censal](ine-cartografia-censal.yaml) | INE – Cartografía de secciones censales y callejero del Censo Electoral | download, ogc, api-rest | none | shp, zip, pdf, txt, geojson, gml | annual | static-html, latin1 | 2026-10-01 |

- **cartografia-jcyl**: Descargas de la cartografía oficial de Castilla y León por FTP anónimo con carpetas por producto: ortofotografía, LiDAR (.laz por campaña: 2009-2014, 2017-2021, 2025), MDE, fotogramas aéreos, SIOSE, SIGPAC y edafología. El portal web es informativo; la descarga va directa al FTP.
- **catastro-ovc**: Datos no protegidos de inmuebles por referencia catastral o dirección (JSON), referencia catastral por coordenadas (XML), equivalencia de códigos de municipio Catastro e INE, parcelario vectorial por WFS INSPIRE, descargas ATOM municipales (parcelas, edificios, direcciones) y WMS. Sin autenticación.
- **cnig-centro-descargas**: Producción del IGN (ortofotos PNOA, modelos del terreno, LiDAR, mapas, límites municipales oficiales, SIOSE) en un Centro de Descargas protegido por reCAPTCHA, más servicios WMS, WMTS y WFS INSPIRE sin restricción y el geocoder CartoCiudad, que devuelve el código INE.
- **idecyl-servicios**: IDE de Castilla y León: catálogo GeoNetwork 3.8.2 con 197 recursos (163 datasets, 31 servicios) consultable por CSW INSPIRE y feed RSS de novedades, más un directorio ArcGIS REST con MapServers de recintos agrícolas anuales (ayg) y visores PGIS (cyt). Sin clave.
- **idee-servicios**: Catálogo CSW INSPIRE y CODSI y servicios del Sistema Cartográfico Nacional: WFS en GML y API Features en GeoJSON de hidrografía, transportes, ocupación del suelo y direcciones, WMS, WMTS y WCS del MDT, y límites, NGBE y núcleos de población del IGN en www.ign.es y api-features.ign.es.
- **ine-cartografia-censal**: Shapefile anual a 1 de enero de las secciones censales (36.669 en 2026, ETRS89 UTM 30) con códigos de sección, distrito, municipio, provincia, comunidad y NUTS desde 2001, las mismas geometrías en GeoJSON por API OGC y el callejero del Censo Electoral con sus variaciones semestrales.
