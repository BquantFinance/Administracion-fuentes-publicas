# Estadística oficial

Sector `estadistica` · 3 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [ine-api-tempus](ine-api-tempus.yaml) | INE – API JSON (Tempus3) | api-rest | none | json, csv | daily | latin1 | 2026-09-30 |
| [ine-codigos-territoriales](ine-codigos-territoriales.yaml) | INE – Códigos de municipios, provincias, comunidades e islas | download | none | xlsx, html | annual | — | 2026-09-30 |
| [ine-microdatos](ine-microdatos.yaml) | INE – Microdatos anonimizados | download | none | csv, txt, parquet, zip, xlsx, json | quarterly | — | 2026-09-30 |

- **ine-api-tempus**: Acceso programático a las 112 operaciones estadísticas del INE: metadatos (operaciones, tablas, variables, valores) y datos de tablas y series (IPC, EPA, PIB, padrón, natalidad, empresas). JSON y CSV, sin autenticación.
- **ine-codigos-territoriales**: Relación oficial anual de los 8132 municipios con código INE (provincia, municipio y dígito de control), comunidades autónomas, provincias e islas. Es la clave para cruzar cualquier dataset territorial español.
- **ine-microdatos**: Ficheros de microdatos anonimizados de encuestas (EPA, Condiciones de Vida, Presupuestos Familiares, Estructura Salarial, Censo, Movimiento Natural de la Población). Cada ZIP trae el fichero en ancho fijo, CSV tabulado, parquet, RData, SAS, SPSS y Stata, más el diseño de registro en xlsx y JSON.
