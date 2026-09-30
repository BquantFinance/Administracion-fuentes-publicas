# Estadística oficial

Sector `estadistica` · 3 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Cualquier estadística oficial del INE (IPC, EPA, PIB, padrón, natalidad, empresas) → `ine-api-tempus`
- Códigos INE de municipios, provincias y comunidades → `ine-codigos-territoriales`
- Microdatos de encuestas (EPA, condiciones de vida, presupuestos familiares, censo) → `ine-microdatos`
- Turismo (FRONTUR, EGATUR, ocupación hotelera) → `ine-api-tempus` (las operaciones son del INE; DATAESTUR (mincotur-industria-turismo) las reagrega con API de clave)
- Renta por sección censal (Atlas de distribución de renta) → `ine-api-tempus` (operación del INE; localizar la tabla con TABLAS_OPERACION, no verificada en esta sesión)
- Empresas activas por actividad y tamaño (DIRCE) → `ine-api-tempus`
- Tasa de paro, ocupados y activos (EPA) → `ine-api-tempus` (la EPA es del INE, no del SEPE)
- Salarios → `ine-api-tempus` (Encuesta de Estructura Salarial en el INE; salarios en fuentes tributarias por municipio en aeat-estadisticas (modelo190_salarios))
- Defunciones por causa de muerte → `ine-api-tempus` (estadística del INE; Sanidad solo publica PDF)
- Padrón, nacimientos, defunciones y migraciones → `ine-api-tempus`
- Índice de precios de vivienda y de alquiler → `ine-api-tempus`
- Población de una entidad singular, núcleo o diseminado (Nomenclátor) → `ine-codigos-territoriales` (POST a nomen2/DescargaTabla por nombre de población (xls o csv), sin clave; la API Tempus no baja del municipio)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [ine-api-tempus](ine-api-tempus.yaml) | INE – API JSON (Tempus3) | api-rest | none | json, csv | daily | errors-html-or-xml | 2026-09-30 |
| [ine-codigos-territoriales](ine-codigos-territoriales.yaml) | INE – Códigos de municipios, provincias, comunidades e islas | download | none | xlsx, html | annual | static-html | 2026-09-30 |
| [ine-microdatos](ine-microdatos.yaml) | INE – Microdatos anonimizados | download | none | csv, txt, parquet, zip, xlsx, json | quarterly | static-html | 2026-09-30 |

- **ine-api-tempus**: Acceso programático a las 112 operaciones estadísticas del INE: metadatos (operaciones, tablas, variables, valores) y datos de tablas y series (IPC, EPA, PIB, padrón, natalidad, empresas). JSON y CSV, sin autenticación.
- **ine-codigos-territoriales**: Relación oficial anual de los 8132 municipios con código INE (provincia, municipio y dígito de control), comunidades autónomas, provincias e islas. Es la clave para cruzar cualquier dataset territorial español.
- **ine-microdatos**: Ficheros de microdatos anonimizados de encuestas (EPA, Condiciones de Vida, Presupuestos Familiares, Estructura Salarial, Censo, Movimiento Natural de la Población). Cada ZIP trae el fichero en ancho fijo, CSV tabulado, parquet, RData, SAS, SPSS y Stata, más el diseño de registro en xlsx y JSON.
