# Telecomunicaciones y sociedad digital

Sector `telecomunicaciones-digital` · 1 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Cobertura de fibra, HFC y 5G por municipio → `mtdfp-cobertura-banda-ancha` (fracciones 0-1 por hogares o por viviendas, no comparables entre bases; la CNMC da líneas, no cobertura)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [mtdfp-cobertura-banda-ancha](mtdfp-cobertura-banda-ancha.yaml) | SETELECO – Cobertura de banda ancha por municipio, provincia y CCAA | download, api-rest | none | xlsx, json, geojson, pdf, html | annual | static-html, url-drift | 2026-10-01 |

- **mtdfp-cobertura-banda-ancha**: Dos xlsx con la fracción de hogares o viviendas con cobertura por tecnología (FTTH, HFC, inalámbrico, 4G, 5G) y velocidad (30 Mbps a 1 Gbps) por municipio (código INE), provincia y CCAA de 2013 a 2025 y por entidad singular hasta 2020, capas ArcGIS consultables del último año e informes en PDF.
