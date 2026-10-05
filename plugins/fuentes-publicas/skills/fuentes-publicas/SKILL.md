---
name: fuentes-publicas
description: Datos públicos de España para construir productos (BOE y BORME, INE, AEAT, contratación, subvenciones, Catastro y SIGPAC, AEMET, Banco de España, SEPE, CNMC, sanidad, comunidades y ayuntamientos). Úsala para encontrar, descargar o programar contra fuentes de la Administración española, montar un producto sobre ellas, cruzar códigos de municipio o empresa, o dar una cifra oficial; trae dónde está cada dato, cómo pedirlo, las trampas verificadas que cambian el resultado y código que lo trae resuelto.
---

# Fuentes públicas de España

Catálogo verificado con llamadas reales: https://github.com/BquantFinance/Administracion-fuentes-publicas

## Flujo

1. Localiza. Con el servidor MCP `catalogo-fuentes-publicas`, `buscar(texto)` devuelve a la vez fichas, recetas,
   necesidades, productos que se pueden construir e identificadores; el detalle de cualquiera, con `ficha(id)`. Sin MCP:
   `curl -s https://raw.githubusercontent.com/BquantFinance/Administracion-fuentes-publicas/main/llms-min.txt` y la
   ficha en `.../main/sources/<sector>/<id>.yaml`.
2. Lee primero `alerts` de la ficha: trampas silenciosas que dan una cifra incompleta o distinta sin error. Aplica la
   operación que indican antes de responder.
3. Trae el dato. Con MCP: `perfil_municipio`, `coyuntura`, `empresa_nif`, `boe_sumario`, `tabla_pcaxis`, `ckan_buscar`
   y `ckan_filas`, `socrata_filas`, `almacen_sql` si hay almacén local y `descargar(url)` para cualquier otra URL
   pública (certificados FNMT, codificación, bloqueos, rutas muertas). `perfil_municipio` y `empresa_nif` aceptan una
   lista y resuelven todo en una llamada; para comparar, mejor una llamada con la lista que una por elemento. En
   Python, los mismos clientes (abajo).
4. Si el usuario quiere montar un producto, mira `productos` en `buscar` (o `indices/productos.yaml`): fuentes, piezas
   de código, frescura, volumen, licencia y la trampa principal de cada uno.

## Código

```bash
pip install "fuentes-publicas-mcp @ git+https://github.com/BquantFinance/Administracion-fuentes-publicas"
```

```python
from fuentes_publicas.clientes import consulta, ckan, socrata, pcaxis, sepe, bdns, almacen
from fuentes_publicas.clientes.sesion import sesion   # requests.Session con FNMT, User-Agent, reintentos y bloqueos

consulta.perfil_municipio("Alcalá de Henares")  # códigos, padrón, renta, paro, contratos y criminalidad
consulta.coyuntura()                            # IPC (avance o definitivo), paro, PIB, Euríbor, prima de riesgo
consulta.empresa_nif("A02066116")               # sector público, BDNS, AEI, prohibiciones; contratos y BORME con almacén
pcaxis.tabla(24077)                             # tablas PC-Axis con números convertidos (None es sin dato, no cero)
list(ckan.filas("cnmc", resource_id))           # todas las filas aunque el portal recorte limit
list(bdns.altas("2026-09-29"))                  # concesiones dadas de alta ese día, cualquiera que sea su fecha
almacen.sql("select nif, nombre, sum(importe_sin_iva) from adjudicaciones_ultimo where not importe_compartido group by all order by 3 desc limit 5")
```

El almacén necesita duckdb y una carga previa: `fuentes-almacen sync --fuentes placsp,borme --desde AAAA-MM-DD`.
Proyectos que funcionan en `ejemplos/` del repo.

## Reglas que evitan los fallos más comunes

- Muchos .gob.es sirven el certificado FNMT sin la intermedia: no desactives TLS, usa `sesion()`.
- User-Agent de navegador siempre; el BOE exige además `Accept: application/json` o `application/xml`.
- Codificación: PC-Axis en UTF-8 aunque diga ISO-8859-15, el SEPE en Windows-1252 aunque diga UTF-8, BDNS y BOE en
  Latin-1; números con coma decimal y punto de miles.
- Topes silenciosos: CKAN 1.000 o 32.000, Socrata 1.000, BDNS 50 en la exportación sin pageSize, SIGPAC 250, GBIF 300.
- Municipio: SIGPAC y Catastro numeran distinto que el INE en más de la mitad (capitales 900), el INE Tempus filtra
  por Id interno y MINETUR y AEMET tienen ids propios; traduce con `perfil_municipio(..., solo_codigos=True)` o
  `datos/municipios.csv`.
- Catastro, datos.gob.es, REE, BNE y FEGA rechazan IP de centros de datos: si fallan desde la nube, prueba otra red
  antes de dar la fuente por caída.
- Antes de meter datos en un producto: licencia en `license` de la ficha; cita literal, licencias NC y SA, datos
  personales y datos que caducan (BDNS a los 4 años, PAC a los 2, deudores de la AEAT a los 3 meses) en
  `guides/reutilizacion.md`.
