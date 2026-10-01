# Consumo y seguridad alimentaria

Sector `consumo-seguridad-alimentaria` · 1 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Alertas alimentarias, registro sanitario de empresas alimentarias y laboratorios → `aesan-alertas-registros` (alertas solo en HTML; sin RSS ni API localizados)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [aesan-alertas-registros](aesan-alertas-registros.yaml) | AESAN – Alertas alimentarias, registro sanitario de empresas y datos abiertos | portal, download, scraping | none | html, xlsx | irregular | static-html, url-drift, latin1, session-required | 2026-10-01 |

- **aesan-alertas-registros**: Alertas alimentarias como páginas HTML con referencia, fecha y producto, buscador paginado desde enero de 2025, Excel de 29.575 alimentos comercializados en 2022 con EAN, cuota de mercado y nutrientes, laboratorios RELSA y búsqueda en el registro sanitario de empresas (RGSEAA, JSP con sesión).
