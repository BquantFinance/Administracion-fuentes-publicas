# Territorio, catastro y cartografía

Sector `territorio-cartografia` · 3 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | verificada |
|---|---|---|---|---|---|---|
| [catastro-ovc](catastro-ovc.yaml) | Catastro – Servicios web de la Oficina Virtual (OVC) e INSPIRE | api-rest, api-soap, ogc, download | none | json, xml, gml, shp, dxf, png | daily | — |
| [cnig-centro-descargas](cnig-centro-descargas.yaml) | IGN/CNIG – Centro de Descargas de cartografía y geodatos | download, ogc, api-rest | none | shp, gpkg, geotiff, laz, ecw, pdf, jpg, kml | irregular | — |
| [idee-servicios](idee-servicios.yaml) | IDEE – Infraestructura de Datos Espaciales de España | ogc, api-rest, portal | none | xml, gml, geojson, json | daily | — |

- **catastro-ovc**: Consulta de referencias catastrales por dirección, coordenadas o RC; datos no protegidos de inmuebles (superficie, uso, año); cartografía parcelaria vectorial vía INSPIRE (WFS/ATOM) y WMS. Sin autenticación para datos no protegidos; titularidad y valor requieren certificado.
- **cnig-centro-descargas**: Descarga gratuita de toda la producción del IGN: ortofotos PNOA, modelos digitales del terreno, LiDAR, mapas topográficos, límites municipales oficiales, redes de transporte, SIOSE, nomenclátor geográfico. Servicios WMS/WMTS.
- **idee-servicios**: Catálogo de servicios geográficos interoperables de todas las Administraciones (más de 3.000 WMS, WFS, WMTS, CSW) y directorio de nodos IDE. Punto de partida para localizar cualquier capa geográfica oficial.
