# Cultura y patrimonio

Sector `cultura-patrimonio` · 2 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Estadísticas culturales (empleo cultural, bibliotecas, museos, cine, bono cultural) → `cultura-culturabase` (PC-Axis con el patrón de descarga del INE; certificado con intermedia fuera de la lista FNMT)
- Catálogo bibliográfico de la BNE y patrimonio digital (Hispana) → `bne-datos` (datos.bne.es bloqueado desde el entorno; Hispana por OAI-PMH)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [bne-datos](bne-datos.yaml) | BNE – datos.bne.es (linked data, SPARQL) e Hispana (OAI-PMH) | oai-pmh, sparql, api-rest, download | none | xml, rdf, ttl, jsonld, json | monthly | waf-blocks-bots, url-drift | 2026-09-30 |
| [cultura-culturabase](cultura-culturabase.yaml) | Ministerio de Cultura – CULTURAbase y estadísticas culturales | download, portal | none | csv, px, xlsx, pdf, html | annual | tls-chain-incomplete, static-html, latin1, url-drift | 2026-09-30 |

- **bne-datos**: Catálogo bibliográfico y de autoridades de la BNE como datos enlazados (RDF, SPARQL, JSON-LD) e Hispana, agregador nacional de patrimonio digital con OAI-PMH (10,6 millones de registros, 124 sets, formatos oai_dc, edm, ese y didl). datos.bne.es respondió 403 desde este entorno; Hispana sí.
- **cultura-culturabase**: Sistema PC-Axis (el mismo software que INEbase) con las estadísticas culturales: empleo cultural, bibliotecas, museos, cine, comercio exterior, bono cultural, fundaciones y asuntos taurinos; cada tabla se descarga en CSV, px o xlsx con URL deducible. Más el Anuario en PDF.
