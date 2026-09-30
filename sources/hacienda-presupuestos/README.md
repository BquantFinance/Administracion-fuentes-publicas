# Hacienda, tributos y presupuestos

Sector `hacienda-presupuestos` · 6 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Renta y declarantes de IRPF por municipio, código postal o tramo → `aeat-estadisticas`
- Recaudación tributaria mensual por figura → `aeat-estadisticas`
- Suministro Inmediato de Información, VERI*FACTU y presentación de modelos → `aeat-servicios-web` (SOAP con certificado electrónico)
- Presupuestos, liquidaciones y deuda viva de ayuntamientos y diputaciones → `hacienda-ovef`
- Tipos de IBI, IAE e IVTM por municipio → `hacienda-ovef` (consulta web con sesión (SGFAL))
- Déficit de las Administraciones Públicas y ejecución del presupuesto del Estado → `igae-ejecucion-presupuestaria`
- Inventario de entes del sector público (INVENTE) → `igae-ejecucion-presupuestaria`
- Presupuestos Generales del Estado por capítulos, políticas y programas (aprobados o proyecto) → `sepg-presupuestos-generales-estado` (presupuesto, no ejecución; la ejecución está en igae-ejecucion-presupuestaria)
- Periodo medio de pago a proveedores de todas las AAPP y financiación extraordinaria de las CCAA (FLA) → `hacienda-central-informacion`
- Calendario de publicación de las estadísticas de Hacienda, IGAE y AEAT → `hacienda-central-informacion`

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aeat-estadisticas](aeat-estadisticas.yaml) | AEAT – Estadísticas tributarias y descarga masiva | download, portal | none | csv, xlsx, html, pdf | monthly | static-html, overwritten-in-place | 2026-09-30 |
| [aeat-servicios-web](aeat-servicios-web.yaml) | AEAT – Servicios web SII y VERI*FACTU | api-soap | certificate | xml | realtime | — | 2026-09-30 |
| [hacienda-central-informacion](hacienda-central-informacion.yaml) | Hacienda – Central de Información (calendario, periodo medio de pago, financiación CCAA) | download, portal | none | xlsx, html, pdf | monthly | static-html, overwritten-in-place | 2026-09-30 |
| [hacienda-ovef](hacienda-ovef.yaml) | Hacienda – Entidades locales, presupuestos, deuda viva, financiación y tributos | download, portal | none | xlsx, xls, pdf | annual | static-html, session-required, url-drift | 2026-09-30 |
| [igae-ejecucion-presupuestaria](igae-ejecucion-presupuestaria.yaml) | IGAE – Ejecución presupuestaria y contabilidad nacional | download, portal | none | xlsx, pdf, html | monthly | static-html | 2026-09-30 |
| [sepg-presupuestos-generales-estado](sepg-presupuestos-generales-estado.yaml) | Secretaría de Estado de Presupuestos y Gastos – Presupuestos Generales del Estado en xlsx | download | none | xlsx, pdf | annual | static-html | 2026-09-30 |

- **aeat-estadisticas**: Estadísticas de declarantes de IRPF (nacional, por municipio y por código postal), IVA, Sociedades y Patrimonio, informes mensuales y anuales de recaudación, ventas, empleo y salarios en fuentes tributarias, comercio exterior. CSV masivos del anuario y series de recaudación en xlsx con URL estable.
- **aeat-servicios-web**: Servicios web SOAP con certificado electrónico para el Suministro Inmediato de Información del IVA (SII), los sistemas de facturación VERI*FACTU y la presentación de modelos. WSDL y XSD públicos, entorno de pruebas con host propio y portal de desarrolladores separado de la sede.
- **hacienda-central-informacion**: Portal que reúne las publicaciones económico-financieras de Hacienda e IGAE, con catálogo de informes y tres ficheros de URL estable: calendario de publicaciones (xlsx), periodo medio de pago a proveedores de todas las AAPP (xlsx mensual) y financiación extraordinaria de las CCAA (xlsx desde 2019).
- **hacienda-ovef**: Datos de todas las entidades locales: deuda viva por ayuntamiento, entregas a cuenta y cesión de tributos, ejecución presupuestaria trimestral, liquidaciones y cumplimiento de estabilidad, periodo medio de pago y tipos impositivos municipales. Ficheros xlsx anuales y consultas web con sesión.
- **igae-ejecucion-presupuestaria**: Déficit y operaciones no financieras de las AAPP en contabilidad nacional (mensual por subsector, trimestral y anual), ejecución mensual del presupuesto del Estado en caja, cuentas anuales de las AAPP e inventario de entes públicos (INVENTE). Ficheros xlsx anuales con URL predecible.
- **sepg-presupuestos-generales-estado**: Estadísticas de los Presupuestos Generales del Estado por ejercicio (2014 a 2025, proyectos con sufijo P): cinco libros xlsx por año (consolidados, Estado, Seguridad Social, organismos autónomos, resto de entes) con los cuadros de ingresos y gastos por capítulos, políticas y programas, más su PDF.
