# Resultados de la evaluación · 2026-10-05 (sexta tanda: almacén local y productos)

Mide si el almacén local (`almacen_sql` sobre Parquet y DuckDB) y el bloque `productos` de `buscar` ahorran tiempo o
errores frente al mismo MCP sin ellos. Claude Haiku 4.5 con Bash y el catálogo solo por `evals/mcp_cli.py`. Condición M:
MCP completo con un almacén sincronizado ese día (BOE, BORME y BDNS del 28/09 al 03/10; PLACSP 643 desde el 30/09).
Condición B: `EVAL_SIN=almacen_sql,buscar.productos` y sin almacén; las fichas, con sus alertas, siguen en las dos.
Referencias tomadas por dos vías que coinciden (almacén frente a API o XML crudo; `tareas.yaml`, sexta tanda). Dos
repeticiones por tarea y condición. Cuando M falló por cómo se exponía el almacén, se corrigió y se repitió: cada
versión va en su fila. Tokens de entrada reales con `consumo.py`.

Tareas: T17 sociedades-valencia-semana (BORME), T18 bdns-altas-tres-dias, T19 licitaciones-obras-dia (PLACSP),
T20 producto-avisos-licitaciones y T21 producto-riesgo-proveedores.

| tarea | cond. | aciertos | usos (media) | tokens de entrada (media) | segundos (media) | error |
|---|---|---|---|---|---|---|
| T17 | M inicial | 0/2 | 15,5 | 897.846 | 140 | no usaron almacen_sql: bajaron el XML y lo parsearon a mano (52 y 485) |
| T17 | M + pista en buscar | 0/2 | 23 | 1.480.064 | 164 | uno no pasó por buscar (115); otro contó sobre 500 de 626 filas truncadas (138) |
| T17 | M + truncado explícito | 1/2 | 10 | 491.132 | 81 | el que falla no pasó por buscar (166) |
| T17 | M final | 2/2 | 11,5 | 636.758 | 75 | |
| T17 | B | 2/2 | 19 | 1.153.657 | 182 | |
| T18 | M | 2/2 | 10,5 | 555.975 | 62 | |
| T18 | B | 2/2 | 13 | 704.951 | 159 | (uno con el importe 294.628 € corto, 0,07 %) |
| T19 | M, vista anterior | 0/2 | 19 | 998.621 | 107 | consultaron la tabla por versiones: 126 bien, «todas vigentes», 767 y 398,7 M€ |
| T19 | M final | 0/2 | 21,5 | 1.129.549 | 125 | uno con vigentes e importe exactos pero 125 publicadas (eran 126); otro sumó con UNNEST (767 M€) |
| T19 | M + pista de UNNEST | 1/2 | 27 | 1.679.837 | 199 | uno exacto en las tres cifras (89 s); el otro vio el aviso de buscar, bajó el ZIP a mano (567) y se saltó las reglas (leyó ficheros del repo) |
| T19 | B | 0/2 | 18,5 | 1.092.602 | 393 | filtraron el feed por updated: 521 y 530 publicadas, 1.344 y 979 M€ |
| T20 | M | 2/2 | 8,5 | 413.337 | 52 | |
| T20 | B | 0/2 | 14 | 762.878 | 110 | no encuentran la pieza (fuentes-radar): «no hay producto hecho»; uno inventa que el id ATOM cambia por estado |
| T21 | M | 2/2 | 10 | 500.535 | 74 | |
| T21 | B | 2/2 | 13,5 | 714.265 | 102 | |

Referencias: T17, 174 constituciones (32, 35, 28 y 79; el 02/10 no hay sección de Valencia) y ACTIVOS E INVERSIONES MV
con 24.448.370 €; T18, 37.420 concesiones por 395.511.451,37 € y la DG de Fondos Europeos con 166.215.950,19 €; T19, 126
licitaciones de obras con su primer anuncio DOC_CN el 01/10, una anulada el 02/10, 125 vigentes por 395.669.253,39 €.

## Conclusiones

- **Productos se queda**: 4 de 4 frente a 2 de 4, un 38 % menos de tokens de entrada (456.936 frente a 738.572) y 63 s
  frente a 106 s. Es lo único que dice qué pieza de código existe para un producto: sin él, T20 respondió dos veces que
  no había nada hecho cuando `fuentes-radar` lo hace. En T21 la herramienta (`empresa_nif`) se descubre por su nombre.
- **El almacén se queda, con lo que enseñó la tanda**: por sí solo no se descubría (T17, 0 de 4 hasta que `buscar`,
  `boe_sumario` y los errores SQL avisan de que el dato ya está en local). Con la versión final, T17 y T18 dan 4 de 4 con
  almacén y 4 de 4 sin él, pero con un 36 % menos de tokens y en 69 s frente a 170 s. En T19, sin almacén nadie acierta
  (los agentes filtran el feed por updated y se van a 521 o 530); con almacén y todas las correcciones, uno de dos da las
  tres cifras exactas en 89 s, y el otro ignora el aviso y lo hace a mano.
- La tanda sacó siete fallos de código, corregidos el mismo día:
  - la vista `empresas` rompía cualquier consulta en un almacén sin PLACSP;
  - la BDNS respondía 200 con `ERR_MANTENIMIENTO_BBDD` y sin content;
  - `descargar` decía `completo: true` junto a un texto truncado;
  - `almacen_sql` truncaba sin dar el total;
  - la cobertura de PLACSP solo daba los meses;
  - `fecha_publicacion` de PLACSP era la del primer anuncio y no la de licitación: 274 obras «publicadas» el 01/10 frente a 126, error que heredaban el radar y `licitaciones.py`;
  - `placsp_ultimo` perdía las anuladas.
- La referencia de T17 por PDF con pdftotext contaba 162: el orden de lectura mezcla entradas. El XML del BORME y el
  almacén coinciden (174).
