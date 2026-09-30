# Gobierno abierto, transparencia y organización administrativa

Sector `gobierno-abierto-administracion` · 5 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [datos-gob-es-api](datos-gob-es-api.yaml) | datos.gob.es – Catálogo nacional de datos abiertos (API y SPARQL) | api-rest, sparql, download | none | json, xml, csv, rdf, ttl | daily | — | — |
| [dir3-directorio](dir3-directorio.yaml) | DIR3 – Directorio Común de Unidades Orgánicas y Oficinas | download, api-soap | none | csv, xlsx, xml | daily | — | — |
| [face-facturas](face-facturas.yaml) | FACe – Punto general de entrada de facturas electrónicas | api-soap, download | certificate | xml, xlsx | realtime | — | — |
| [pag-administracion-gob-es](pag-administracion-gob-es.yaml) | Punto de Acceso General – Trámites, sedes y empleo público | portal, feed | none | html, rss, xlsx | daily | — | — |
| [transparencia-portal](transparencia-portal.yaml) | Portal de la Transparencia de la AGE | portal, download | none | csv, xlsx, pdf, html | monthly | — | — |

- **datos-gob-es-api**: Catálogo federado de datasets abiertos de todas las Administraciones españolas (más de 90.000 conjuntos) con metadatos DCAT-AP. API REST para buscar datasets, distribuciones y publicadores, y endpoint SPARQL.
- **dir3-directorio**: Inventario oficial de todas las unidades orgánicas, organismos y oficinas de registro y atención de las Administraciones españolas con código DIR3 único, jerarquía y estado. Es la clave que usan facturación electrónica (FACe), contratación, subvenciones y notificaciones.
- **face-facturas**: Servicios web para presentar y consultar facturas electrónicas (Facturae 3.2.x) a las Administraciones adheridas, directorio de unidades receptoras (DIR3) y estadísticas de facturación.
- **pag-administracion-gob-es**: Catálogo de procedimientos y servicios de la AGE (SIA), convocatorias de empleo público, directorio de sedes electrónicas y organigramas. Base para localizar el trámite y la sede competentes.
- **transparencia-portal**: Publicidad activa de la AGE: altos cargos y sus retribuciones, agendas, contratos, convenios, subvenciones, presupuestos, informes, y estadísticas de solicitudes de derecho de acceso. Muchos datasets en CSV/XLSX.
