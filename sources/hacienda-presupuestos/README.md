# Hacienda, tributos y presupuestos

Sector `hacienda-presupuestos` · 4 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aeat-estadisticas](aeat-estadisticas.yaml) | AEAT – Estadísticas tributarias y descarga masiva | download, portal | none | csv, xlsx, html, pdf | monthly | — | 2026-09-30 |
| [aeat-servicios-web](aeat-servicios-web.yaml) | AEAT – Servicios web SII y VERI*FACTU | api-soap | certificate | xml | realtime | — | 2026-09-30 |
| [hacienda-ovef](hacienda-ovef.yaml) | Hacienda – Entidades locales, presupuestos, deuda viva, financiación y tributos | download, portal | none | xlsx, xls, pdf | annual | — | 2026-09-30 |
| [igae-ejecucion-presupuestaria](igae-ejecucion-presupuestaria.yaml) | IGAE – Ejecución presupuestaria y contabilidad nacional | download, portal | none | xlsx, pdf, html | monthly | — | 2026-09-30 |

- **aeat-estadisticas**: Estadísticas de declarantes de IRPF (nacional, por municipio y por código postal), IVA, Sociedades y Patrimonio, informes mensuales y anuales de recaudación, ventas, empleo y salarios en fuentes tributarias, comercio exterior. CSV masivos del anuario y series de recaudación en xlsx con URL estable.
- **aeat-servicios-web**: Servicios web SOAP con certificado electrónico para el Suministro Inmediato de Información del IVA (SII), los sistemas de facturación VERI*FACTU y la presentación de modelos. WSDL y XSD públicos, entorno de pruebas con host propio y portal de desarrolladores separado de la sede.
- **hacienda-ovef**: Datos de todas las entidades locales: deuda viva por ayuntamiento, entregas a cuenta y cesión de tributos, ejecución presupuestaria trimestral, liquidaciones y cumplimiento de estabilidad, periodo medio de pago y tipos impositivos municipales. Ficheros xlsx anuales y consultas web con sesión.
- **igae-ejecucion-presupuestaria**: Déficit y operaciones no financieras de las AAPP en contabilidad nacional (mensual por subsector, trimestral y anual), ejecución mensual del presupuesto del Estado en caja, cuentas anuales de las AAPP e inventario de entes públicos (INVENTE). Ficheros xlsx anuales con URL predecible.
