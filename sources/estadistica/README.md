# Estadística oficial

Sector `estadistica` · 7 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Cualquier estadística oficial del INE (IPC, EPA, PIB, padrón, natalidad, empresas) → `ine-api-tempus`
- Códigos INE de municipios, provincias y comunidades → `ine-codigos-territoriales`
- Microdatos de encuestas (EPA, condiciones de vida, presupuestos familiares, censo) → `ine-microdatos`
- Turismo (FRONTUR, EGATUR, ocupación hotelera) → `ine-api-tempus` (las operaciones son del INE; DATAESTUR (mincotur-industria-turismo) las reagrega con una API que no exigió clave y da 504 a menudo)
- Renta por sección censal (Atlas de distribución de renta) → `ine-api-tempus` (operación del INE; localizar la tabla con TABLAS_OPERACION, no verificada en esta sesión)
- Empresas activas por actividad y tamaño (DIRCE) → `ine-api-tempus`
- Tasa de paro, ocupados y activos (EPA) → `ine-api-tempus` (la EPA es del INE, no del SEPE)
- Salarios → `ine-api-tempus` (Encuesta de Estructura Salarial en el INE; salarios en fuentes tributarias por municipio en aeat-estadisticas (modelo190_salarios))
- Defunciones por causa de muerte → `ine-api-tempus` (estadística del INE; Sanidad solo publica PDF)
- Padrón, nacimientos, defunciones y migraciones → `ine-api-tempus`
- Índice de precios de vivienda y de alquiler → `ine-api-tempus`
- Población de una entidad singular, núcleo o diseminado (Nomenclátor) → `ine-codigos-territoriales` (POST a nomen2/DescargaTabla por nombre de población (xls o csv), sin clave; la API Tempus no baja del municipio)
- PIB municipal, contabilidad trimestral y defunciones por barrio de la Comunidad de Madrid → `comunidad-madrid-estadistica-api` (no está en el INE; municipios con código INE de 5 dígitos)
- Estadística oficial de Cataluña por municipio, comarca o sección censal (padrón, renta, PIB, afiliación) → `idescat-api` (municipios con 6 dígitos (INE más dígito de control); el INE de 5 se ignora y devuelve todos sin error)
- Ficha resumen de un municipio catalán (población, renta, paro, vivienda) en una llamada → `idescat-api` (EMEX; la población es la del Censo anual, no la del padrón)
- Población por municipio andaluz desde 1996 y estadística propia del IECA → `ieca-api-badea` (los filtros usan ids internos de miembro, no años ni códigos INE)
- Indicadores coyunturales por provincia andaluza (IPC, EPA, paro, PIB) → `ieca-api-badea` (INDEA; cada código fija tipo de dato y base)
- Estadísticas por comarca valenciana (pobreza, empresas, industria, cultivos) → `ive-pegv-bancos-datos` (el INE no publica comarcas; comarcas solo por nombre y agrupación nueva desde 2023)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [comunidad-madrid-estadistica-api](comunidad-madrid-estadistica-api.yaml) | Instituto de Estadística de la Comunidad de Madrid – API eDatos | api-rest | none | json, xml, csv, zip | monthly | soft-errors-200 | 2026-10-01 |
| [idescat-api](idescat-api.yaml) | Idescat – API de tablas (JSON-stat), El municipio en cifras y búsqueda de población | api-rest | none | json, xml | daily | json-object-or-list, soft-errors-200 | 2026-10-01 |
| [ieca-api-badea](ieca-api-badea.yaml) | IECA – API de BADEA e INDEA (Instituto de Estadística y Cartografía de Andalucía) | api-rest, download | none | json, txt, px, xls, xlsx, pdf, csv, zip, html | irregular | errors-html-or-xml, soft-errors-200 | 2026-10-01 |
| [ine-api-tempus](ine-api-tempus.yaml) | INE – API JSON (Tempus3) | api-rest | none | json, csv | daily | errors-html-or-xml, soft-errors-200 | 2026-10-01 |
| [ine-codigos-territoriales](ine-codigos-territoriales.yaml) | INE – Códigos de municipios, provincias, comunidades e islas | download | none | xlsx, xls, csv, txt, zip, html | annual | static-html, latin1 | 2026-10-01 |
| [ine-microdatos](ine-microdatos.yaml) | INE – Microdatos anonimizados | download | none | csv, txt, parquet, zip, xlsx, json, sav, dta | quarterly | static-html | 2026-10-01 |
| [ive-pegv-bancos-datos](ive-pegv-bancos-datos.yaml) | IVE – Bancos de datos del Portal Estadístico de la GV (BDT y BDO) | download, portal | none | csv, xlsx, xls, px | annual | latin1, errors-html-or-xml, overwritten-in-place, soft-errors-200, connection-reset-intermittent | 2026-10-01 |

- **comunidad-madrid-estadistica-api**: API REST de la plataforma eDatos del Instituto (agencia IECM): 278 operaciones y 858 datasets con datos propios de Madrid (PIB municipal, contabilidad trimestral, nacimientos y defunciones por municipio, barrio o zona de salud, afiliación). JSON o XML, exportación a CSV, sin clave.
- **idescat-api**: APIs REST sin clave del Idescat. Tablas de 33 estadísticas (padrón, censo, PIB trimestral, renta, afiliación, proyecciones) en JSON-stat por Cataluña, provincia, comarca, municipio, distrito y sección censal; ficha municipal EMEX con unos 230 indicadores y población por entidad.
- **ieca-api-badea**: BADEA, banco de datos del IECA, por API REST JSON: cada consulta (padrón municipal desde 1996, Contabilidad Regional Trimestral, condiciones de vida) con metadatos, jerarquías y datos, exportable a txt, px, xls y pdf; e INDEA, indicadores por provincia. Sin autenticación.
- **ine-api-tempus**: Acceso programático a las 112 operaciones estadísticas del INE: metadatos (operaciones, tablas, variables, valores) y datos de tablas y series (IPC, EPA, PIB, padrón, natalidad, empresas). JSON y CSV, sin autenticación.
- **ine-codigos-territoriales**: Relación oficial anual de los 8.132 municipios con código INE (provincia, municipio y dígito de control), comunidades autónomas, provincias e islas, y Nomenclátor de entidades singulares, núcleos y diseminados con su población. Es la clave para cruzar cualquier dataset territorial español.
- **ine-microdatos**: Ficheros de microdatos anonimizados de encuestas (EPA, Condiciones de Vida, Presupuestos Familiares, Estructura Salarial, Censo, Movimiento Natural de la Población). Los ZIP recientes traen ancho fijo, CSV, parquet, RData, SAS, SPSS y Stata con el diseño en JSON; el diseño en xlsx va aparte.
- **ive-pegv-bancos-datos**: Tablas del IVE por municipio, comarca y provincia (pobreza comarcal, renta per cápita, directorio de empresas, superficies de cultivo, indicadores demográficos, industria) con descarga estática por código de consulta en CSV, xlsx y PC-Axis. El INE no da la escala comarcal.
