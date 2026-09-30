# Meteorología y clima

Sector `meteorologia-clima` · 2 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aemet-opendata](aemet-opendata.yaml) | AEMET OpenData – API meteorológica y climatológica | api-rest | api-key | json, xml, csv, png | hourly | — | — |
| [aemet-otros-servicios](aemet-otros-servicios.yaml) | AEMET – Datos de radiación, ozono, polen y modelos numéricos | download, portal | none | csv, grib, netcdf, pdf, txt | daily | — | — |

- **aemet-opendata**: Predicciones por municipio, observación horaria de estaciones, valores climatológicos diarios y normales, avisos, radar, satélite, índice UV, predicción marítima y de montaña. API REST con clave gratuita.
- **aemet-otros-servicios**: Complementos fuera de la API principal: descargas de salidas de modelos numéricos, series climáticas homogeneizadas, radiación solar, ozono y datos históricos en ficheros. Acceso vía portal y FTP anónimo.
