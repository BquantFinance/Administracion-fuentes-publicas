# Resultados de la evaluación · 2026-10-01 (tercera tanda: trampas silenciosas)

Siete tareas en las que la vía directa da una cifra plausible y errónea sin ningún error, resueltas por Claude Haiku
4.5 con Bash, curl y python en tres condiciones: A sin catálogo, C con `llms-min.txt` y las fichas en disco, M con el
servidor MCP (por `evals/mcp_cli.py`). Tres repeticiones por tarea y condición (63 agentes). Los tokens son por primera
vez el consumo real: suma de la entrada de cada turno, con `evals/consumo.py` sobre las transcripciones.

Tareas (en `tareas.yaml`): T1 paro-municipio (Abengibre, SEPE), T2 SIGPAC del punto de la Puerta del Sol (municipio
Catastro 900 frente a INE 28079), T3 dir3-ayuntamiento-madrid (FACe, 99 unidades), T4 criminalidad-trimestre (balance
acumulado), T5 encina-gbif (Quercus rotundifolia), T6 referencia-catastral-direccion (Catastro bloquea IP de nube),
T7 padron-cm-datastore (datastore recortado y antiguo). Corrección automática por la cifra o código esperado.

## Antes de las alertas

| tarea | cond. | aciertos | llamadas (mediana) | fallidas | usos de herramienta (media) | tokens de entrada (media) | segundos (media) |
|---|---|---|---|---|---|---|---|
| T1 | A | 0/3 | 35 | 41 | 29 | 1.708.387 | 263 |
| T1 | C | 3/3 | 2 | 0 | 15 | 830.328 | 84 |
| T1 | M | 3/3 | 2 | 0 | 10 | 501.684 | 81 |
| T2 | A | 0/3 | 13 | 54 | 17 | 968.681 | 236 |
| T2 | C | 3/3 | 2 | 0 | 8 | 469.931 | 50 |
| T2 | M | 3/3 | 4 | 2 | 11 | 674.162 | 79 |
| T3 | A | 0/3 | 18 | 25 | 19 | 1.111.258 | 163 |
| T3 | C | 1/3 | 3 | 0 | 14 | 812.598 | 133 |
| T3 | M | 2/3 | 2 | 0 | 8 | 420.195 | 66 |
| T4 | A | 0/3 | 50 | 82 | 19 | 1.021.225 | 233 |
| T4 | C | 1/3 | 2 | 0 | 9 | 544.115 | 83 |
| T4 | M | 0/3 | 1 | 0 | 9 | 443.675 | 59 |
| T5 | A | 0/3 | 1 | 0 | 4 | 200.074 | 25 |
| T5 | C | 0/3 | 2 | 1 | 9 | 468.023 | 50 |
| T5 | M | 0/3 | 2 | 0 | 7 | 376.843 | 47 |
| T6 | A | 0/3 | 12 | 29 | 8 | 446.374 | 89 |
| T6 | C | 1/3 | 2 | 4 | 11 | 590.842 | 76 |
| T6 | M | 2/3 | 2 | 6 | 9 | 479.760 | 92 |
| T7 | A | 3/3 | 3 | 1 | 14 | 737.336 | 116 |
| T7 | C | 1/3 | 2 | 1 | 11 | 614.942 | 81 |
| T7 | M | 3/3 | 3 | 2 | 11 | 626.428 | 59 |

| cond. | aciertos | llamadas (mediana) | fallidas | usos de herramienta (media) | tokens de entrada (media) |
|---|---|---|---|---|---|
| A | 3/21 | 16 | 232 | 15.6 | 884.762 |
| C | 10/21 | 2 | 6 | 11.1 | 618.683 |
| M | 13/21 | 2 | 10 | 9.2 | 503.250 |

- Sin catálogo, Haiku acierta 3 de 21: falla en descubrir la fuente (paro, SIGPAC, FACe, Interior, Catastro) y gasta
  mediana de 16 llamadas con 232 fallidas en total. Con catálogo, 10 de 21 (C) y 13 de 21 (M), con 2 llamadas de
  mediana y casi ninguna fallida.
- Tokens de entrada reales: C un 30 % menos que A y M un 43 % menos. El MCP es la condición más barata.
- Las trampas silenciosas no se resolvían aunque el agente leyera la ficha: T5 0 de 9 en las tres condiciones (todos
  21.322), T4 1 de 9 (el acumulado 75.461), y en T7 el catálogo empeoró el resultado (C 1 de 3 frente a A 3 de 3) porque
  llevó al datastore, recortado y antiguo; la trampa estaba en gotchas, entre otras diez.

## Después de las alertas

Las trampas silenciosas pasaron a un campo `alerts` que va tras el resumen de la ficha y que el MCP devuelve lo primero.
Mismas tareas T4, T5 y T7, tres repeticiones más por condición.

| tarea | cond. | aciertos | llamadas (mediana) | fallidas | usos de herramienta (media) | tokens de entrada (media) | segundos (media) |
|---|---|---|---|---|---|---|---|
| T4 | C | 0/3 | 1 | 0 | 7 | 417.091 | 60 |
| T4 | M | 2/3 | 2 | 0 | 10 | 522.160 | 88 |
| T5 | C | 3/3 | 6 | 1 | 10 | 570.677 | 98 |
| T5 | M | 3/3 | 7 | 2 | 9 | 500.352 | 166 |
| T7 | C | 3/3 | 3 | 0 | 13 | 698.475 | 59 |
| T7 | M | 3/3 | 2 | 0 | 10 | 577.946 | 73 |

La primera alerta de T4 describía la trampa («acumulados desde enero; el trimestre suelto sale restando») y los agentes
restaban mal o no restaban. Reescrita con los ficheros, la fila y un ejemplo con números («09006 menos 09003 en la fila
III. TOTAL INFRACCIONES PENALES, Barcelona 2026, 75.461 - 37.913 = 37.548»):

| tarea | cond. | aciertos | llamadas (mediana) | fallidas | usos de herramienta (media) | tokens de entrada (media) | segundos (media) |
|---|---|---|---|---|---|---|---|
| T4 | C | 3/3 | 2 | 0 | 8 | 462.838 | 68 |
| T4 | M | 3/3 | 2 | 0 | 10 | 536.036 | 79 |

## Conclusiones

- Las alertas funcionan: en las tres trampas que el catálogo no evitaba, de 5 de 18 aciertos (C y M) a 18 de 18 con la
  versión final (T5 6 de 6, T7 6 de 6, T4 6 de 6 con la alerta explícita).
- Una alerta tiene que decir qué hacer, con nombres de fichero, fila o identificador y un ejemplo con números; describir
  la trampa no basta para un modelo pequeño.
- El catálogo multiplica el acierto de Haiku en tareas con trampa (3 de 21 sin catálogo, 13 de 21 con MCP antes de las
  alertas) y reduce llamadas, fallidas y tokens; el MCP acierta más que los ficheros (13 frente a 10 de 21) y gasta un
  19 % menos de entrada, con las mismas llamadas de mediana.
- Limitaciones: tres repeticiones, un solo modelo, corrección por cadena esperada; T6 depende de que CartoCiudad dé la
  referencia porque el Catastro rechaza la IP del entorno.
