# Agricultura, pesca y alimentación

Sector `agricultura-pesca-alimentacion` · 4 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Beneficiarios de la PAC → `fega-beneficiarios-pac` (FEGA cierra la conexión desde IP de centros de datos (30/09 y 01/10/2026); parte de los pagos directos está en bdns-api como convocatorias autonómicas, con cobertura desigual)
- Recintos agrícolas, usos del suelo y referencia catastral rústica → `mapa-sigpac`
- Anuario de estadística agraria, precios percibidos y pagados, consumo alimentario → `mapa-estadisticas-agrarias`
- Flota pesquera, capturas y acuicultura → `mapa-pesca` (el identificador de buque es CODIGOBUQUE, no el CFR)
- Superficie por cultivo y comunidad autónoma (ESYRCE) → `mapa-estadisticas-agrarias` (xlsx anual desde 2022; microdatos solo previa solicitud en sede electrónica)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [fega-beneficiarios-pac](fega-beneficiarios-pac.yaml) | FEGA – Beneficiarios de ayudas de la PAC y datos de pagos | portal, download | none | csv, xlsx, pdf | annual | waf-blocks-bots | — |
| [mapa-estadisticas-agrarias](mapa-estadisticas-agrarias.yaml) | MAPA – Anuario de estadística, precios, avances de cultivos, ESYRCE, ganadería y consumo | download, portal | none | xlsx, xls, pdf, html | monthly | url-drift, static-html | 2026-10-01 |
| [mapa-pesca](mapa-pesca.yaml) | MAPA – Registro de flota pesquera y estadísticas de capturas, desembarcos y acuicultura | download, portal | none | xlsx, pdf, html | annual | url-drift, static-html | 2026-10-01 |
| [mapa-sigpac](mapa-sigpac.yaml) | SIGPAC – Recintos agrícolas por OGC API, consultas REST, WMS, teselas y GeoPackage (FEGA) | api-rest, ogc, download, portal | none | json, geojson, gpkg, zip, xml, protobuf, pdf | annual | url-drift | 2026-10-01 |

- **fega-beneficiarios-pac**: Consulta pública de beneficiarios de la PAC (FEAGA y FEADER) por ejercicio con importe y medida, informes de pagos y datos abiertos del organismo. No verificable desde aquí porque el servidor cierra la conexión; parte de las ayudas está en la BDNS y el SIGPAC del FEGA vive en sigpac-hubcloud.es.
- **mapa-estadisticas-agrarias**: Anuario de Estadística con todas las tablas en xlsx por capítulo (2000-2024), precios percibidos y pagados, precios medios semanales, avances mensuales de superficies y producciones, ESYRCE (xlsx nacional y por comunidad), encuestas ganaderas y panel de consumo alimentario en hogares.
- **mapa-pesca**: Registro General de la Flota Pesquera 2006-2025 en un xlsx por buque y año (197.131 filas con código de buque, puerto base, caladero, modalidad, arqueo, potencia, eslora y edad), capturas por especie FAO y zona (serie 1992-2024), desembarcos por destino, flota por características y acuicultura.
- **mapa-sigpac**: Recintos SIGPAC de toda España (uso, superficie, pendiente, regadío, altitud) con OGC API Features, consultas REST por coordenadas o códigos (referencia catastral, Red Natura, nitratos), WMS, teselas vectoriales, listas de códigos y GeoPackage por provincia y campaña. Sin clave, licencia CC BY 4.0.
