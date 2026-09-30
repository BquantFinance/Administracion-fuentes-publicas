# Demografía, migraciones y sociedad

Sector `demografia-migraciones-sociedad` · 4 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Feminicidios por comunidad autónoma, provincia, año y mes → `igualdad-estadisticas-violencia-genero` (API Saiku sin clave; crear consulta MDX y exportar CSV; territorios por nombre, sin código INE)
- Llamadas al 016 por provincia y mes → `igualdad-estadisticas-violencia-genero` (cubo 040 Servicio 016 con medidas de llamadas, WhatsApp, correo y chat)
- Casos activos en VioGén y órdenes de protección → `igualdad-estadisticas-violencia-genero` (cubos 090 y 120; el origen es Interior y el CGPJ)
- Dependencia (SAAD): solicitudes, dictámenes, prestaciones por grado y CCAA, lista de espera → `imserso-dependencia` (xlsx mensual estsisaad_{AAAAMMDD} con URL deducible; la encuesta EDAD es del INE)
- Personas con discapacidad reconocida por provincia, sexo, edad y grado → `imserso-dependencia` (BEDPCD en CSV largo 2019-2024 (bdepcd_2024-1-))
- Pensiones no contributivas por provincia → `imserso-dependencia` (csv y xlsx sobreescritos cada mes; las contributivas están en segsocial-estadisticas)
- Microdatos de un barómetro o encuesta del CIS → `cis-estudios` (MD{n}.zip sin registro desde contentUrl del JSON-LD de la página del estudio; el catálogo es JavaScript con anti-bot, enumerar por sitemap.xml)
- Serie de estimación de voto del CIS → `cis-estudios` (solo PDF {n}_Estimacion.pdf por barómetro; las series web cargan por JavaScript sin API localizada)
- Indicadores de igualdad por sexo (empleo, salarios, poder, salud) → `inmujeres-mujeres-cifras` (un xls por indicador en inmujeres.gob.es aunque el HTML enlace al host antiguo inmujer.es)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [cis-estudios](cis-estudios.yaml) | CIS – Catálogo de estudios y microdatos de barómetros y encuestas (MD{n}.zip) | download, scraping | none | zip, sav, csv, xlsx, pdf, html, jsonld, xml | monthly | js-rendered, waf-blocks-bots, static-html | 2026-09-30 |
| [igualdad-estadisticas-violencia-genero](igualdad-estadisticas-violencia-genero.yaml) | Ministerio de Igualdad – Portal estadístico de violencia de género (Saiku) y boletines | api-rest, download, portal | none | json, csv, xlsx, pdf, html | monthly | session-required, errors-html-or-xml, static-html, url-drift | 2026-09-30 |
| [imserso-dependencia](imserso-dependencia.yaml) | IMSERSO – Estadísticas del SAAD (dependencia), PNC, discapacidad y residencias | download, portal | none | xlsx, csv, docx, pdf, html | monthly | static-html, overwritten-in-place, latin1, user-agent-browser | 2026-09-30 |
| [inmujeres-mujeres-cifras](inmujeres-mujeres-cifras.yaml) | Instituto de las Mujeres – Mujeres en cifras (indicadores por sexo en xls) | download, scraping | none | xls, pdf, html | annual | static-html, latin1 | 2026-09-30 |

- **cis-estudios**: Microdatos de los estudios del CIS (barómetros, preelectorales, postelectorales y encuestas temáticas) sin registro como MD{n}.zip con .sav, CSV y texto de ancho fijo, más cuestionario, ficha técnica, tabulaciones xlsx y estimación de voto en PDF; cada página de estudio lleva JSON-LD con las URL.
- **igualdad-estadisticas-violencia-genero**: Portal OLAP (Saiku 2.5) con 17 cubos consultables sin clave por API REST: feminicidios desde 2003, menores, llamadas al 016, ATENPRO, VioGén, denuncias, órdenes de protección y ayudas, por CCAA, provincia, año y mes, con exportación CSV y xlsx. Boletines mensuales en PDF y DERA en xlsx.
- **imserso-dependencia**: Ficheros xlsx y csv con URL deducible: estadística mensual del SAAD (solicitudes, dictámenes, prestaciones por grado y CCAA, lista de espera, cuidadores), nómina mensual de PNC, Base Estatal de Personas con Discapacidad en CSV largo, censo de residencias y servicios sociales para mayores.
- **inmujeres-mujeres-cifras**: Indicadores por sexo elaborados sobre datos de INE, SEPE y Seguridad Social en 13 temas (demografía, educación, empleo y prestaciones, salarios, conciliación, poder y decisiones, violencia, salud, ciencia); un xls por indicador con hoja reciente e histórica 1998-2021, más informes PDF.
