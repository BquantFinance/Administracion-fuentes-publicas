# Estadística oficial

Sector `estadistica` · 3 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [ine-api-tempus](ine-api-tempus.yaml) | INE – API JSON (Tempus3) | api-rest | none | json, csv, px | daily | — | — |
| [ine-codigos-territoriales](ine-codigos-territoriales.yaml) | INE – Códigos de municipios, provincias y unidades territoriales | download | none | xlsx, csv | annual | — | — |
| [ine-microdatos](ine-microdatos.yaml) | INE – Microdatos anonimizados | download | none | csv, txt, zip, sql | quarterly | — | — |

- **ine-api-tempus**: Acceso programático a todas las operaciones estadísticas del INE: metadatos (operaciones, tablas, variables, valores) y datos de tablas y series (IPC, EPA, PIB, padrón, natalidad, empresas). JSON y CSV, sin autenticación.
- **ine-codigos-territoriales**: Relación oficial de municipios con código INE (5 dígitos, provincia + municipio + dígito de control), provincias, comunidades autónomas, NUTS, islas y variaciones anuales (altas, bajas, cambios de nombre). Es la clave para cruzar cualquier dataset territorial español.
- **ine-microdatos**: Ficheros de microdatos anonimizados de encuestas (EPA, Encuesta de Condiciones de Vida, Presupuestos Familiares, Estructura Salarial, Censo, Movimiento Natural de la Población) con diseño de registro y programas de lectura.
