# Gobierno abierto, transparencia y organización administrativa

Sector `gobierno-abierto-administracion` · 5 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [datos-gob-es-api](datos-gob-es-api.yaml) | datos.gob.es – Catálogo nacional de datos abiertos (API) | api-rest, sparql, portal | none | json, xml, csv, rdf | daily | waf-intermittent-403, errors-html-or-xml, static-html | 2026-09-30 |
| [dir3-directorio](dir3-directorio.yaml) | DIR3 – Directorio Común de Unidades Orgánicas y Oficinas | download, portal | none | xlsx, pdf | daily | session-required, user-agent-browser, static-html | 2026-09-30 |
| [face-facturas](face-facturas.yaml) | FACe – Facturas electrónicas al sector público y directorio DIR3 | api-rest, api-soap, download | none | json, csv, xml | realtime | — | 2026-09-30 |
| [pag-administracion-gob-es](pag-administracion-gob-es.yaml) | Punto de Acceso General – Trámites, SIA, empleo público y ayudas | portal | none | html, pdf | weekly | static-html, url-drift | 2026-09-30 |
| [transparencia-portal](transparencia-portal.yaml) | Portal de la Transparencia de la AGE | portal, download | none | html, xlsx, pdf | monthly | static-html, url-drift | 2026-09-30 |

- **datos-gob-es-api**: Catálogo federado de los datasets abiertos de todas las Administraciones (Estado, CCAA, EELL, universidades) con metadatos DCAT-AP, distribuciones con URL de descarga y publicador identificado por código DIR3. API REST JSON paginada; el endpoint SPARQL no respondió desde este entorno.
- **dir3-directorio**: Inventario oficial de unidades orgánicas, entidades y oficinas de todas las Administraciones con código DIR3, jerarquía, NIF, provincia y estado. Descarga pública en xlsx por nivel más catálogos auxiliares; es la clave de FACe, PLACSP, BDNS y datos.gob.es.
- **face-facturas**: Punto general de entrada de facturas electrónicas: API pública JSON y CSV con las 50000 relaciones oficina contable, órgano gestor y unidad tramitadora (DIR3 y NIF) de las Administraciones adheridas, y servicios SOAP con certificado para presentar y consultar facturas.
- **pag-administracion-gob-es**: Portal ciudadano de la AGE: boletín semanal de empleo público y boletín quincenal de ayudas y becas en PDF, buscador de trámites con código SIA, buscador de oficinas y directorio de sedes electrónicas. Sin API localizada ni descarga estructurada; útil como índice, no como fuente de datos.
- **transparencia-portal**: Publicidad activa de la AGE por materias (organización y empleo público, altos cargos, planificación, normativa, contratos, convenios, subvenciones) y estadísticas del derecho de acceso en xlsx. Portal Adobe Experience Manager con contenido por página; sin API localizada y pocas descargas.
