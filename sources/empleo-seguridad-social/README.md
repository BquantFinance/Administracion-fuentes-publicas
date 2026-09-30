# Empleo y Seguridad Social

Sector `empleo-seguridad-social` · 3 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Paro registrado, demandantes y contratos por municipio → `sepe-estadisticas`
- Afiliación a la Seguridad Social por régimen, actividad, provincia y municipio → `segsocial-estadisticas`
- Pensiones contributivas e Ingreso Mínimo Vital → `segsocial-estadisticas`
- Muestra Continua de Vidas Laborales → `segsocial-estadisticas` (no se descarga; se solicita bajo convenio)
- Convenios colectivos (REGCON), huelgas, accidentes de trabajo, regulación de empleo → `mites-estadisticas`
- Extranjeros con autorización de residencia y afiliados extranjeros → `segsocial-estadisticas` (afiliados extranjeros en EST292; las estadísticas de extranjería del Ministerio de Inclusión no están aún en el catálogo)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [mites-estadisticas](mites-estadisticas.yaml) | Ministerio de Trabajo – Estadísticas laborales y REGCON | download, portal | none | xlsx, pdf, html | monthly | tls-chain-incomplete, static-html, session-required | 2026-09-30 |
| [segsocial-estadisticas](segsocial-estadisticas.yaml) | Seguridad Social – Afiliación, pensiones, IMV y MCVL | download, portal | none | xlsx, pdf | monthly | waf-intermittent-403, url-drift, static-html | 2026-09-30 |
| [sepe-estadisticas](sepe-estadisticas.yaml) | SEPE – Paro registrado, contratos y prestaciones | download, portal | none | xls, pdf, html, rss | monthly | static-html, overwritten-in-place | 2026-09-30 |

- **mites-estadisticas**: Estadísticas de convenios colectivos, accidentes de trabajo, huelgas, regulación de empleo, ETT, cooperativas y mediación, con avances mensuales y monográficas anuales en xlsx, más REGCON, el registro de convenios, acuerdos y planes de igualdad con búsqueda pública por código, CNAE y denominación.
- **segsocial-estadisticas**: Afiliación (media mensual y último día) por régimen, provincia, CNAE, sexo y municipio; pensiones contributivas por clase e importe; Ingreso Mínimo Vital; bases de cotización; Muestra Continua de Vidas Laborales bajo solicitud. Excel mensuales y anuales servidos por un gestor de contenidos.
- **sepe-estadisticas**: Datos mensuales de paro registrado, demandantes, contratos y prestaciones por desempleo: avance mensual en xls con URL fija, series históricas, y desglose por municipio, actividad económica, sexo y edad en un xls por comunidad autónoma y mes.
