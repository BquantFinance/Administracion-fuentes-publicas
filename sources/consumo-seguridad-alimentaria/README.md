# Consumo y seguridad alimentaria

Sector `consumo-seguridad-alimentaria` · 1 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Alertas alimentarias, registro sanitario de empresas alimentarias y laboratorios → `aesan-alertas-registros` (alertas solo en HTML; sin RSS ni API localizados)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aesan-alertas-registros](aesan-alertas-registros.yaml) | AESAN – Alertas alimentarias, registro sanitario de empresas y datos abiertos | portal, download, scraping | none | html, xlsx | irregular | static-html, url-drift, latin1 | 2026-09-30 |

- **aesan-alertas-registros**: Alertas alimentarias como páginas HTML con referencia, fecha y producto, buscador con filtros de fecha y paginación, Excel con composición y cuota de mercado de alimentos comercializados en 2022 por código EAN, lista de laboratorios RELSA y consulta del registro sanitario de empresas (JSP).
