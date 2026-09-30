# Territorio, catastro y cartografía

Sector `territorio-cartografia` · 4 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Datos de un inmueble o parcela por referencia catastral, dirección o coordenadas → `catastro-ovc` (bloqueo por IP tras ráfagas de unas 15 peticiones)
- Parcelario, edificios y direcciones vectoriales por municipio (INSPIRE) → `catastro-ovc`
- Ortofotos PNOA, modelos del terreno, LiDAR y límites municipales → `cnig-centro-descargas` (descargas con reCAPTCHA; WMS, WMTS y WFS sin restricción)
- Geocodificar una dirección y obtener su código INE → `cnig-centro-descargas` (geocoder CartoCiudad)
- Geometría de secciones censales, distritos y municipios por año → `ine-cartografia-censal` (shapefile anual del INE; los límites municipales oficiales del IGN están tras reCAPTCHA (cnig-centro-descargas))
- Localizar cualquier servicio WMS, WFS o CSW de una Administración → `idee-servicios`

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [catastro-ovc](catastro-ovc.yaml) | Catastro – Servicios web de la Oficina Virtual (OVC) e INSPIRE | api-rest, ogc, download | none | json, xml, gml, zip, png | daily | latin1 | 2026-09-30 |
| [cnig-centro-descargas](cnig-centro-descargas.yaml) | IGN/CNIG – Centro de Descargas, servicios OGC y geocoder CartoCiudad | ogc, api-rest, download, portal | none | shp, gpkg, geotiff, laz, gml, geojson, json, png | irregular | captcha-required, js-rendered, static-html | 2026-09-30 |
| [idee-servicios](idee-servicios.yaml) | IDEE – Catálogos CSW y directorio de servicios geográficos | ogc, portal | none | xml, json | daily | static-html | 2026-09-30 |
| [ine-cartografia-censal](ine-cartografia-censal.yaml) | INE – Cartografía de secciones censales y callejero del Censo Electoral | download | none | shp, zip, pdf | annual | static-html | 2026-09-30 |

- **catastro-ovc**: Datos no protegidos de inmuebles por referencia catastral o dirección (JSON), referencia catastral por coordenadas (XML), equivalencia de códigos de municipio Catastro e INE, parcelario vectorial por WFS INSPIRE, descargas ATOM municipales (parcelas, edificios, direcciones) y WMS. Sin autenticación.
- **cnig-centro-descargas**: Producción del IGN (ortofotos PNOA, modelos del terreno, LiDAR, mapas, límites municipales oficiales, SIOSE) en un Centro de Descargas protegido por reCAPTCHA, más servicios WMS, WMTS y WFS INSPIRE sin restricción y el geocoder CartoCiudad, que devuelve el código INE.
- **idee-servicios**: Punto de entrada a los servicios geográficos oficiales de todas las Administraciones: catálogo CSW INSPIRE con más de 13000 registros, catálogo oficial CODSI, directorio de servicios OGC por tipo y organismo y monitorización de disponibilidad. Metadatos ISO 19139 consultables por CQL.
- **ine-cartografia-censal**: Shapefile anual a 1 de enero de las 36.669 secciones censales (ETRS89 UTM 30) con códigos de sección, distrito, municipio, provincia, comunidad y NUTS, desde 2011, más las variaciones semestrales del callejero del Censo Electoral. La geometría para cualquier dato por sección.
