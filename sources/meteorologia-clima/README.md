# Meteorología y clima

Sector `meteorologia-clima` · 2 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Predicción, observación, climatología, avisos y radar → `aemet-opendata` (clave gratuita obligatoria; el cuerpo vacío con 200 es fallo de autenticación)
- Proyecciones de cambio climático y series centenarias → `aemet-otros-servicios` (proyecciones AR5 y rejilla diaria de 5 km en tar.gz; desde IP de centro de datos llegaron vacíos)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aemet-opendata](aemet-opendata.yaml) | AEMET OpenData – API meteorológica y climatológica | api-rest | api-key | json, xml, csv, png | hourly | latin1, soft-errors-200 | 2026-10-01 |
| [aemet-otros-servicios](aemet-otros-servicios.yaml) | AEMET – Portal de servicios climáticos y proyecciones de cambio climático | portal, download | none | html, pdf, netcdf, txt | irregular | latin1, static-html | 2026-10-01 |

- **aemet-opendata**: API REST con clave gratuita (JWT): predicciones por municipio, provincia y comunidad, observación de estaciones, climatología diaria, mensual, normales y extremos, avisos CAP, radar, rayos, radiación, ozono, satélite y maestro de municipios. 64 rutas en la especificación OpenAPI 3.0.1.
- **aemet-otros-servicios**: Portal de AEMET fuera de la API: series centenarias, efemérides, proyecciones de cambio climático (AR6 y AR5) y catálogo RISP, con tar.gz de proyecciones AR5 diarias y de la rejilla observacional diaria de 5 km (NetCDF y txt). Sin FTP; radiación, ozono, normales y extremos están en aemet-opendata.
