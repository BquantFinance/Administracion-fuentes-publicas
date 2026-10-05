# Educación y universidades

Sector `educacion-universidades` · 3 fuentes · índice generado por `scripts/build.py`, no editar.

## Dónde está cada cosa

- Alumnado, profesorado y centros no universitarios → `educacion-estadisticas-ruct` (EDUCAbase con el patrón PC-Axis del INE)
- Universidades, matriculados y egresados por titulación, títulos oficiales (RUCT) → `educacion-estadisticas-ruct`
- Microdatos de PISA, TIMSS o PIAAC de España → `inee-bases-datos` (muestra española en rar o zip con SPSS y Stata; HEAD responde 403, usar GET con Range)
- Colegios e institutos cerca de una dirección o de unas coordenadas → `centros-docentes-ccaa` (Cataluña, Madrid, Comunitat Valenciana y Andalucía; perfil_municipio con la dirección da los de 1 km; el registro estatal no trae coordenadas)

| id | fuente | acceso | auth | formatos | actualización | quirks | verificada |
|---|---|---|---|---|---|---|---|
| [centros-docentes-ccaa](centros-docentes-ccaa.yaml) | Centros docentes con coordenadas – directorios autonómicos | api-rest, download | none | json, csv | irregular | user-agent-browser, url-drift | 2026-10-05 |
| [educacion-estadisticas-ruct](educacion-estadisticas-ruct.yaml) | Educación y Universidades – EDUCAbase (PC-Axis), SIIU, RUCT y registro de centros | download, portal | none | csv, px, xlsx, xls, html | annual | latin1, tls-chain-incomplete, url-drift, soft-errors-200 | 2026-10-01 |
| [inee-bases-datos](inee-bases-datos.yaml) | INEE – Bases de datos de PISA, TIMSS, PIAAC, ICILS y evaluaciones nacionales (España) | download | none | zip, rar, sav, dta, csv, xlsx | irregular | url-drift, static-html | 2026-10-01 |

- **centros-docentes-ccaa**: Centros docentes no universitarios con coordenadas, titularidad y enseñanzas en los directorios de Cataluña, Madrid, Comunitat Valenciana y Andalucía. El registro estatal (educacion-estadisticas-ruct) no trae coordenadas.
- **educacion-estadisticas-ruct**: Estadísticas de enseñanza no universitaria en EDUCAbase (PC-Axis idéntico al del INE, con descarga CSV, px y xlsx por tabla), estadísticas universitarias SIIU en xlsx (matriculados y egresados por titulación 2015-2024), y RUCT y Registro Estatal de Centros Docentes con exportación xls sin sesión.
- **inee-bases-datos**: Muestras españolas de las evaluaciones internacionales (PISA 2000-2022 con base conjunta 2000-2015, TIMSS 2023, PIAAC ciclo 1, ICILS, PISA para centros) y bases de las evaluaciones nacionales (EGD 2009 y 2010, Escuela 2.0, PROA, Enseñanzas Medias 1984-1989) en SPSS, Stata, xlsx y CSV sin registro.
