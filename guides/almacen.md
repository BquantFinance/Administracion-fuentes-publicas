# Almacén local en Parquet

`scripts/clientes/almacen.py` baja BOE, BORME, BDNS, PLACSP y carburantes a una carpeta tuya, un Parquet por tabla y
mes. Se pone al día solo y se consulta con DuckDB. El repo no aloja datos: cada uno carga lo que necesita
(`almacen/` está en `.gitignore`). Sirve para lo que las APIs no permiten: contratos por NIF del adjudicatario, el BORME
por denominación, series de precios por gasolinera o cruces entre fuentes.

```bash
pip install duckdb                     # o pip install "fuentes-publicas-mcp[almacen] @ git+https://github.com/BquantFinance/Administracion-fuentes-publicas"
python scripts/clientes/almacen.py sync --fuentes boe,borme,bdns,placsp,carburantes --desde 2026-09-01
python scripts/clientes/almacen.py sync                 # cada día (cron): solo lo nuevo hasta ayer
python scripts/clientes/almacen.py zip-placsp 202608 202607 --feeds 643,1143   # meses que ya no están en la cadena del feed
python scripts/clientes/almacen.py empresa B37033297    # contratos, subvenciones y BORME de un NIF
python scripts/clientes/almacen.py sql "select nif, nombre, sum(importe_sin_iva) from adjudicaciones_ultimo where not importe_compartido group by all order by 3 desc limit 10"
```

La carpeta es `./almacen` o la que diga `FUENTES_ALMACEN`. `estado.json` guarda lo cargado: un corte (`--minutos`) no
deja huecos y repetir no baja nada dos veces. Con `pip install` el comando es `fuentes-almacen`.

## Tablas

| tabla | una fila por | clave | partición |
|---|---|---|---|
| `boe` | item del sumario (sección, departamento, título, URL del PDF y del XML) | identificador | fecha |
| `borme` | empresa de la sección A: denominación, tipos de acto, capital, datos registrales | documento, número | fecha |
| `bdns` | concesión, minimis o ayuda de Estado (`coleccion`), por fecha de alta | coleccion, id | fecha_alta |
| `placsp` | versión de un expediente (estado, órgano con DIR3 y NIF, importes, CPV) | id, updated | updated (UTC) |
| `placsp_adjudicaciones` | lote y adjudicatario (NIF, nombre, importes, pyme, ofertas) | id, updated, n | updated (UTC) |
| `carburantes` | estación y día, con los 23 productos en columnas | fecha, ideess | fecha |

`placsp_ultimo` y `adjudicaciones_ultimo` dejan solo el último estado de cada expediente: el feed trae una entrada por
cambio de estado. Desde la 0.9.0, `fecha_publicacion` es la del anuncio de licitación (DOC_CN); un almacén anterior
la tenía del primer anuncio, a menudo el de adjudicación, y relee PLACSP en la siguiente `sync` (los ZIP quedan en
`zips_por_releer` de estado.json; la cobertura lo avisa hasta entonces). `placsp_ultimo` es la última versión no anulada, con `anulada`, `anulada_el` y `motivo_baja` (las bajas
llegan como filas `borrado` sin datos: el 01/10/2026, 126 licitaciones de obras publicadas, una anulada al día siguiente). `adjudicaciones_ultimo` añade `adjudicatarios` (del lote) e `importe_compartido`: en los acuerdos marco
el importe del lote se repite en cada adjudicatario (en el 1044 de agosto de 2026, sumar por fila daba 33.302 M€ y contando
cada lote una vez 9.709 M€); para totales, `importe_sin_iva / adjudicatarios` si es compartido. El 1044 no trae fecha de
adjudicación: `coalesce(fecha_adjudicacion, fecha_contrato)`. En la BDNS, minimis no trae `importe`; su cifra es `ayuda_equivalente`.

## Lo medido el 2026-10-01

- **BOE**: un día, 213 filas y 23 KB.
- **BORME**: un día, 1.785 empresas y 100 KB.
- **BDNS**: un día de altas, 13.937 filas en 63 s y 279 KB.
- **Carburantes**: dos días, 23.000 filas y 0,75 MB, unos 20 s por día.
- **PLACSP, cadena de los tres feeds**: día y medio, 8.434 entradas en 2,5 minutos.
- **PLACSP, ZIP del 1143 de agosto**: 28.091 entradas en 40 s, que ocupan 2 MB y 0,9 MB de adjudicaciones.

Para cargar años enteros, el campo `sync` de cada ficha da el tamaño y el tiempo de la fuente completa.

## Datos personales

Sigue `guides/reutilizacion.md`:

- **BDNS y adjudicatarios de PLACSP**: las personas físicas (DNI, NIE o NIF enmascarado) se guardan sin NIF, nombre ni
  idPersona, con `persona_fisica` a true, para que los totales cuadren.
- **BORME**: se guarda el tipo de cada acto; el texto, solo de los que no llevan nombres (constitución, domicilio,
  capital, objeto, denominación, disolución...). Nombramientos, ceses, revocaciones, socio único, situación concursal y
  fe de erratas quedan solo como tipo.

## Agentes

Con el servidor MCP, `almacen_sql` ejecuta SQL de solo lectura sobre la carpeta: DuckDB no puede leer ni escribir fuera
de ella ni cargar extensiones. `empresa_nif` añade contratos y BORME del almacén si existe. Las consultas solo ven lo
cargado; `cobertura` dice qué meses hay.
