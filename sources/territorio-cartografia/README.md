# Territorio, catastro y cartografía

Sector `territorio-cartografia` · 4 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Datos de un inmueble o parcela por referencia catastral, dirección o coordenadas → `catastro-ovc` (bloqueo por IP tras ráfagas de unas 15 peticiones)
- Parcelario, edificios y direcciones vectoriales por municipio (INSPIRE) → `catastro-ovc`
- Ortofotos PNOA, modelos del terreno, LiDAR y límites municipales → `cnig-centro-descargas` (descargas con reCAPTCHA; WMS, WMTS y WFS sin restricción)
- Geocodificar una dirección y obtener su código INE → `cnig-centro-descargas` (geocoder CartoCiudad)
- Geometría de secciones censales, distritos y municipios por año → `ine-cartografia-censal` (shapefile anual del INE; los límites municipales oficiales del IGN están tras reCAPTCHA (cnig-centro-descargas))
- Localizar cualquier servicio WMS, WFS o CSW de una Administración → `idee-servicios`
- Carreteras y ferrocarril oficiales en vectorial → `idee-servicios` (WFS transportes de servicios.idee.es solo en GML; filtrar por bbox y paginar con count)
- Ríos, embalses y cuencas en vectorial → `idee-servicios` (WFS hidrografia; GetCapabilities falla con 500 la mitad de las veces, repetir; GetFeature no falla)
- Ocupación del suelo SIOSE por polígono → `idee-servicios` (110 millones de polígonos en el WFS ocupacion-suelo; sin count no responde)
- Altitud o modelo digital del terreno de una zona → `idee-servicios` (WCS mdt con GetCoverage y SUBSET devuelve GeoTIFF; WMTS mdt para visualizar)
- Buscar un topónimo → `idee-servicios` (WFS NGBE de www.ign.es con FILTER por nombre y GeoJSON; el geocoder de direcciones está en cnig-centro-descargas)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [catastro-ovc](catastro-ovc.yaml) | Catastro – Servicios web de la Oficina Virtual (OVC) e INSPIRE | api-rest, ogc, download | none | json, xml, gml, zip, png | daily | latin1 | 2026-09-30 |
| [cnig-centro-descargas](cnig-centro-descargas.yaml) | IGN/CNIG – Centro de Descargas, servicios OGC y geocoder CartoCiudad | ogc, api-rest, download, portal | none | shp, gpkg, geotiff, laz, gml, geojson, json, png | irregular | captcha-required, js-rendered, static-html | 2026-09-30 |
| [idee-servicios](idee-servicios.yaml) | IDEE – Catálogos CSW y servicios INSPIRE del IGN (WFS, WMS, WMTS, WCS) | ogc, portal | none | xml, json, gml, geojson, png, jpg, geotiff | irregular | static-html, errors-html-or-xml | 2026-09-30 |
| [ine-cartografia-censal](ine-cartografia-censal.yaml) | INE – Cartografía de secciones censales y callejero del Censo Electoral | download | none | shp, zip, pdf | annual | static-html | 2026-09-30 |

- **catastro-ovc**: Datos no protegidos de inmuebles por referencia catastral o dirección (JSON), referencia catastral por coordenadas (XML), equivalencia de códigos de municipio Catastro e INE, parcelario vectorial por WFS INSPIRE, descargas ATOM municipales (parcelas, edificios, direcciones) y WMS. Sin autenticación.
- **cnig-centro-descargas**: Producción del IGN (ortofotos PNOA, modelos del terreno, LiDAR, mapas, límites municipales oficiales, SIOSE) en un Centro de Descargas protegido por reCAPTCHA, más servicios WMS, WMTS y WFS INSPIRE sin restricción y el geocoder CartoCiudad, que devuelve el código INE.
- **idee-servicios**: Catálogo CSW INSPIRE y CODSI, directorio de servicios OGC y los servicios INSPIRE del Sistema Cartográfico Nacional en servicios.idee.es (WFS de hidrografía, transportes y ocupación del suelo en GML, WMS temáticos, WMTS y WCS del MDT), más el WFS del Nomenclátor NGBE en www.ign.es con GeoJSON.
- **ine-cartografia-censal**: Shapefile anual a 1 de enero de las 36.669 secciones censales (ETRS89 UTM 30) con códigos de sección, distrito, municipio, provincia, comunidad y NUTS, desde 2011, más las variaciones semestrales del callejero del Censo Electoral. La geometría para cualquier dato por sección.
