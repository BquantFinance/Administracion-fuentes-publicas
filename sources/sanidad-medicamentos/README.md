# Sanidad y medicamentos

Sector `sanidad-medicamentos` · 4 fuentes · índice generado por `scripts/build.py`, no editar.

| id | fuente | acceso | auth | formatos | actualización | verificada |
|---|---|---|---|---|---|---|
| [aemps-cima-api](aemps-cima-api.yaml) | AEMPS CIMA – API REST de medicamentos autorizados | api-rest, download | none | json, xml, pdf, html | daily | — |
| [aemps-otros-registros](aemps-otros-registros.yaml) | AEMPS – Registro de ensayos clínicos, productos sanitarios y cosméticos | portal, feed | none | html, pdf, rss, xlsx | daily | — |
| [isciii-cne](isciii-cne.yaml) | ISCIII – Centro Nacional de Epidemiología y vigilancia (RENAVE, SiVIRA) | portal, download | none | csv, xlsx, pdf, html | weekly | — |
| [sanidad-portal-estadistico](sanidad-portal-estadistico.yaml) | Ministerio de Sanidad – Portal Estadístico y Sistema de Información Sanitaria | portal, download | none | xlsx, csv, pdf, html | annual | — |

- **aemps-cima-api**: Todos los medicamentos autorizados en España: composición, principios activos, código ATC, código nacional, ficha técnica y prospecto en HTML/PDF, estado de comercialización, problemas de suministro, laboratorio. API REST JSON sin autenticación.
- **aemps-otros-registros**: Registro Español de Estudios Clínicos (REEC) con búsqueda y ficha por ensayo, distribuidores y fabricantes de productos sanitarios, alertas de seguridad y calidad, notas informativas y datos de farmacovigilancia.
- **isciii-cne**: Vigilancia epidemiológica nacional: boletines semanales de enfermedades de declaración obligatoria, sistema SiVIRA de infecciones respiratorias, MoMo (exceso de mortalidad diario), datos históricos COVID-19 por provincia.
- **sanidad-portal-estadistico**: Portal Estadístico del SNS: altas hospitalarias (RAE-CMBD), Indicadores Clave del SNS, gasto sanitario, recursos y actividad de hospitales y atención primaria (SIAP), consumo farmacéutico, encuestas de salud, catálogo de hospitales y centros. Consulta interactiva y descarga.
