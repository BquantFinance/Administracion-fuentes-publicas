---
name: fuentes-publicas
description: Datos públicos de España (BOE y BORME, INE, AEAT, contratación, subvenciones, Catastro y SIGPAC, AEMET, Banco de España, CNMC, sanidad, comunidades y ayuntamientos). Úsala para encontrar, descargar o programar contra fuentes de la Administración española, cruzar códigos de municipio o empresa, o dar una cifra oficial; trae dónde está cada dato, cómo pedirlo y las trampas verificadas que cambian el resultado.
---

# Fuentes públicas de España

Catálogo verificado con llamadas reales: https://github.com/BquantFinance/Administracion-fuentes-publicas

## Flujo

1. Localiza la fuente. Con el servidor MCP `catalogo-fuentes-publicas`: `necesidad` o `buscar_fuentes`, y después
   `ficha(id)`. Sin MCP: `curl -s https://raw.githubusercontent.com/BquantFinance/Administracion-fuentes-publicas/main/llms-min.txt`
   y la ficha en `.../main/sources/<sector>/<id>.yaml`.
2. Lee primero `alerts` de la ficha: trampas silenciosas que dan una cifra incompleta o distinta sin ningún error
   (acumulados desde enero, topes de filas sin aviso, datastores recortados, taxones o códigos que no son el esperado).
   Aplica la operación que indican antes de responder.
3. Trae el dato. Con MCP: `descargar(url)` (certificados FNMT, codificación, bloqueos y resumen del CSV, JSON, xlsx o
   ZIP), `tabla_pcaxis`, `boe_sumario`, `subvenciones_nif`, `ckan_buscar`, `ckan_filas`, `socrata_filas`, `municipio`.
   En Python, los mismos clientes (abajo). Con curl, el `example` de cada endpoint de la ficha.
4. Si cruzas fuentes, busca una receta (`buscar_recetas` o `.../main/indices/recetas.yaml`) y el identificador común
   (`identificador(id)`): suelen encadenar dos o tres fichas con un paso que no es obvio.

## Código

```bash
pip install "fuentes-publicas-mcp @ git+https://github.com/BquantFinance/Administracion-fuentes-publicas"
```

```python
from fuentes_publicas.clientes import consulta, ckan, socrata, pcaxis, arcgis, ogc, boe, bdns, ine_tempus, placsp
from fuentes_publicas.clientes.sesion import sesion, texto   # requests.Session con todo lo de abajo resuelto

consulta.descargar(url)                      # dict: estado, formato, resumen, texto
consulta.buscar_municipio("Alcalá de Henares")  # INE, SIGPAC/Catastro, DIR3, NIF, NUTS3, coordenadas
pcaxis.tabla(24077)                          # tablas PC-Axis (INE, Interior, Educación, Cultura) con números
list(ckan.filas("cnmc", resource_id))        # todas las filas aunque el portal recorte limit
list(socrata.filas("gn9e-3qhr"))             # Generalitat: todas, no las 1.000 por defecto
ine_tempus.id_municipio("28079")             # el INE filtra por Id interno (tv=19:Id), no por el código
```

Ejemplos que funcionan, en `ejemplos/` del repo: carburante más barato cerca, BOE del día filtrado, licitaciones nuevas
por CPV, ficha de un municipio, subvenciones de una empresa por NIF.

## Reglas que evitan los fallos más comunes

- Muchos .gob.es sirven el certificado FNMT sin la intermedia: no desactives TLS, usa `sesion()` o el bundle de
  `python scripts/fnmt_bundle.py`.
- User-Agent de navegador siempre; el BOE exige además `Accept: application/json` o `application/xml`.
- Codificación: CSV de PC-Axis en UTF-8 con BOM aunque la cabecera diga ISO-8859-15; BDNS y BOE en Latin-1 o
  windows-1252; números con coma decimal y punto de miles.
- Topes silenciosos: CKAN 1.000 o 32.000, Socrata 1.000, BDNS 50 en la exportación sin pageSize, SIGPAC 250, GBIF 300.
- Municipio: el INE usa 5 dígitos (más dígito de control en algunos ficheros); SIGPAC y Catastro numeran distinto en
  más de la mitad (capitales 900); el INE Tempus filtra por Id interno; MINETUR y AEMET tienen ids propios. Traduce
  con `municipio` o `datos/municipios.csv`.
- Catastro, datos.gob.es, REE, BNE y FEGA rechazan IP de centros de datos: si fallan desde la nube, prueba otra red
  antes de dar la fuente por caída, y mira `ruta_muerta(url)` si una URL recordada ya no responde.
