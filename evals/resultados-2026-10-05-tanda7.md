# Resultados de la evaluación · 2026-10-05 (séptima tanda: campo `code` de las fichas)

Mide si el campo `code` de las fichas (módulo del cliente, llamadas ejecutadas con «qué devuelve» y herramienta MCP
que lo envuelve) ahorra tiempo o errores a un agente que tiene el catálogo por MCP y el paquete instalado, frente al
mismo catálogo con `code` oculto. Claude Haiku 4.5 con Bash, el catálogo solo por `evals/mcp_cli.py` (que imprime las
`instructions` del servidor) y el paquete `fuentes-publicas-mcp` 0.9.0 en un venv cuya ruta se le dice al agente.
Condición C: `EVAL_SIN=almacen_sql,buscar.productos` (como B de la sexta tanda: sin almacén ni productos), con `code` en
`ficha` y su puntero en `buscar`. Condición S: lo mismo más `ficha.code,buscar.code`. Mismas tareas T17, T18 y T19 y
mismas referencias que la sexta tanda. Dos repeticiones por tarea y condición; cuando C falló por lo que decía una línea
de `code`, se corrigió la línea y se repitió (C+, C++), cada versión en su fila. Tokens de entrada reales con
`consumo.py`; «paquete» cuenta los agentes que importaron `fuentes_publicas.clientes` o ejecutaron `fuentes-almacen`.

| tarea | cond. | aciertos | usos (media) | tokens de entrada (media) | segundos (media) | paquete | error |
|---|---|---|---|---|---|---|---|
| T17 | C | 2/2 | 21,5 | 1.490.020 | 169 | 1 de 2 | el que importó `clientes.boe` tardó 207 s: ejecutó sus scripts con el python del sistema, sin el paquete, hasta que usó el del venv |
| T17 | S | 1/2 | 23,5 | 1.676.460 | 377 | 0 de 2 | 166 en vez de 174 (30/09 y 01/10 mal repartidos: 67 y 32) parseando el XML a mano |
| T18 | C | 2/2 | 8 | 402.062 | 94 | 0 de 2 | |
| T18 | S | 2/2 | 11 | 587.608 | 156 | 0 de 2 | |
| T19 | C | 0/2 | 22 | 1.447.556 | 531 | 1 de 2 | `placsp.entradas(max_paginas=30)` filtrando por `updated`: 530 publicadas y 1.238 M€; ZIP a mano por PublicationDate sin quedarse con la última versión: 479 y 445 M€ |
| T19 | C+ (línea con la fecha) | 0/2 | 18,5 | 1.097.935 | 569 | 2 de 2 | los dos filtraron bien por `fecha_publicacion`, pero `entradas(max_paginas=30)` son 450 MB y pasó de los 120 s del Bash; siguieron a mano con las cinco instantáneas del 01/10: 93 y 92 |
| T19 | C++ (almacén primero) | PENDIENTE | | | | | |
| T19 | S | 0/2 | 24,5 | 1.420.888 | 302 | 1 de 2 | feed filtrado por `updated`: 93; `fuentes-almacen sync` por su cuenta y cuenta sobre las tres sindicaciones juntas: 163 (37 del 1044) |

Referencias (sexta tanda): T17, 174 constituciones en Valencia y ACTIVOS E INVERSIONES MV con 24.448.370 €; T18, 37.420
concesiones por 395.511.451,37 € y la DG de Fondos Europeos con 166.215.950,19 €; T19, 126 licitaciones de obras con su
anuncio de licitación el 01/10, una anulada, 125 vigentes por 395.669.253,39 € (comprobado de nuevo el 2026-10-05 con
`fuentes-almacen sync --fuentes placsp --feeds 643 --desde 2026-10-01`, 13 páginas en 10 min 26 s desde esta nube, y la
consulta de la ficha: 126, 125 y 395.669.253,39; con los tres feeds el mismo sync pasó de 15 min). Una repetición de T19 S quedó fuera: encontró en el scratchpad un Parquet de la sexta tanda y contó
sobre él (los almacenes de pruebas se sacaron del alcance de los agentes para el resto).

## Conclusiones

- **`code` se queda**: en T17 y T18, 4 de 4 frente a 3 de 4, con un 16 % menos de tokens de entrada (946.041 frente a
  1.132.034 de media) y la mitad de tiempo (131 s frente a 267). Lo que ahorra no es ejecutar el cliente: en T18 ningún
  agente lo importó, pero los dos de C leyeron `bdns.altas(fechaRegInicio=...)` en la ficha y llamaron a la API con el
  parámetro correcto a la primera (8 usos frente a 11); en T17 uno de C importó `clientes.boe` y el otro fue a mano,
  y los dos acertaron.
- **Una línea de `code` es una instrucción, y se sigue al pie de la letra**: en T19 los agentes hicieron exactamente lo
  que decía la línea de `placsp.entradas`, incluido lo que faltaba. Con `max_paginas=1` y sin hablar de la fecha,
  filtraron por `updated` (530); con la fecha pero `max_paginas=30`, descargaron 450 MB que no caben en los 120 s de un
  Bash y se fueron a mano (93). Por eso la línea tiene que llevar la trampa y la medida (páginas de 15 MB, tres por
  día) y mandar al almacén para días atrás; lo que no diga la línea, el agente lo improvisa mal.
- **T19 sigue siendo la tarea que no sale sin almacén**: 0 de 6 en C y C+ y 0 de 2 en S, cada uno por una trampa
  distinta (filtrar por `updated`, cinco instantáneas de un día, versiones sin deduplicar, los tres feeds juntos). En la
  sexta tanda, con el almacén por MCP, 1 de 2.
- Fallos sacados por la tanda y corregidos el mismo día:
  - `fuentes-almacen sync --fuentes placsp` cargaba las tres sindicaciones y nada avisaba: ahora `almacen.sql` añade la
    pista de la columna `feed` (y la de versiones) por el MCP y por el CLI, `sync` admite `--feeds 643` y la ficha y la
    guía lo dicen con la cifra (163 por 126);
  - la línea de `code` de `placsp.entradas` (fecha y tamaño) y el bloque entero reordenado: almacén para días atrás,
    consulta SQL de un día y `entradas` solo para lo último;
  - del agente que escribió `code` (Opus): `ckan.comparar` daba `completo` con el datastore cargado dos veces (censo de
    instalaciones deportivas de Andalucía, 65.526 por 32.763) y ahora devuelve `sobran`, con alerta en la ficha;
    `bdns._get` rompía con JSONDecodeError si un error venía con Content-Type JSON y cuerpo que no lo era.
- Lo que no mide esta tanda: el paquete instalado desde el repo en vez de la release (0.9.0 no tiene `--feeds`); se
  reinstaló en el venv desde el árbol de trabajo para C++.
