# Meteorología y clima

Sector `meteorologia-clima` · 2 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Predicción, observación, climatología, avisos y radar → `aemet-opendata` (clave gratuita obligatoria; el cuerpo vacío con 200 es fallo de autenticación)
- Proyecciones de cambio climático y series centenarias → `aemet-otros-servicios` (sin descarga directa verificada)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aemet-opendata](aemet-opendata.yaml) | AEMET OpenData – API meteorológica y climatológica | api-rest | api-key | json, xml, csv, png | hourly | latin1, soft-errors-200 | 2026-09-30 |
| [aemet-otros-servicios](aemet-otros-servicios.yaml) | AEMET – Portal de servicios climáticos y proyecciones de cambio climático | portal | none | html, pdf | irregular | latin1, static-html | 2026-09-30 |

- **aemet-opendata**: API REST con clave gratuita (JWT): predicciones por municipio, provincia y comunidad, observación de estaciones, climatología diaria, mensual, normales y extremos, avisos CAP, radar, rayos, radiación, ozono, satélite y maestro de municipios. 64 rutas en la especificación OpenAPI 3.0.1.
- **aemet-otros-servicios**: Páginas del portal de AEMET fuera de la API: series centenarias, efemérides, proyecciones de cambio climático (AR6 y AR5) y catálogo del plan RISP. Sin descargas directas verificadas y sin FTP; radiación, ozono, normales y extremos están en la API (aemet-opendata).
