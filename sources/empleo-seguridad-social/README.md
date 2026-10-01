# Empleo y Seguridad Social

Sector `empleo-seguridad-social` · 3 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Paro registrado, demandantes y contratos por municipio → `sepe-estadisticas` (CSV anual de datos abiertos con todos los municipios y meses desde 2006 (Paro, Contratos, Dtes_empleo); Oza-Cesuras y Cerdedo-Cotobade van con sus códigos anteriores a la fusión)
- Afiliación a la Seguridad Social por régimen, actividad, provincia y municipio → `segsocial-estadisticas` (municipal en MUNCNAE{MM}{AA}.xlsx con URL fija; «<5» como texto y municipio sin cero inicial)
- Pensiones contributivas e Ingreso Mínimo Vital → `segsocial-estadisticas` (el IMV tiene sección propia con nóminas por CCAA y provincia; no está en otras prestaciones (EST45))
- Muestra Continua de Vidas Laborales → `segsocial-estadisticas` (no se descarga; se solicita bajo convenio)
- Convenios colectivos (REGCON), huelgas, accidentes de trabajo, regulación de empleo → `mites-estadisticas` (REGCON exporta todas las filas de una búsqueda en SpreadsheetML (?_exportarExcelPublicoXML=1))
- Extranjeros con autorización de residencia y afiliados extranjeros → `segsocial-estadisticas` (afiliados extranjeros en EST292; las estadísticas de extranjería del Ministerio de Inclusión no están aún en el catálogo)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [mites-estadisticas](mites-estadisticas.yaml) | Ministerio de Trabajo – Estadísticas laborales y REGCON | download, portal | none | xlsx, xls, pdf, html | monthly | tls-chain-incomplete, static-html, session-required | 2026-10-01 |
| [segsocial-estadisticas](segsocial-estadisticas.yaml) | Seguridad Social – Afiliación, pensiones, IMV y MCVL | download, portal | none | xlsx, pdf | monthly | waf-intermittent-403, url-drift, static-html | 2026-10-01 |
| [sepe-estadisticas](sepe-estadisticas.yaml) | SEPE – Paro registrado, contratos y prestaciones | download, portal | none | csv, xls, pdf, html, rss | monthly | latin1, static-html, overwritten-in-place, url-drift | 2026-10-01 |

- **mites-estadisticas**: Estadísticas de convenios colectivos, accidentes de trabajo, huelgas, regulación de empleo, ETT, cooperativas y mediación, con avances mensuales y monográficas anuales en xlsx y xls, más REGCON, el registro de convenios, acuerdos y planes de igualdad con búsqueda pública y exportación a Excel.
- **segsocial-estadisticas**: Afiliación (media mensual y último día) por régimen, provincia, CNAE, sexo y municipio, la municipal en un xlsx largo con URL fija; pensiones contributivas por clase e importe; nómina del Ingreso Mínimo Vital; bases de cotización; Muestra Continua de Vidas Laborales bajo solicitud.
- **sepe-estadisticas**: Paro registrado, contratos, demandantes y prestaciones, mensuales: todos los municipios con código INE en un CSV anual desde 2006, avances en xls con URL fija y series desde 2001, y desglose por CNAE, sexo y edad de capitales y municipios de más de 20.000.
