# Resultados de la evaluación · 2026-10-05 (cuarta tanda: herramientas que traen el dato)

Mide si `perfil_municipio`, `coyuntura` y `empresa_nif` ahorran tiempo o errores frente al mismo MCP sin ellas. Claude
Haiku 4.5 con Bash y el catálogo solo por `evals/mcp_cli.py`; dos condiciones: M (MCP completo) y B (el mismo MCP con
`EVAL_SIN=perfil_municipio,coyuntura,empresa_nif`, es decir buscar, ficha, descargar, tabla_pcaxis y demás). Dos
repeticiones por tarea y condición. Tokens de entrada reales con `consumo.py` (suma de la entrada de cada turno).
Referencias tomadas con llamadas reales el mismo día (`tareas.yaml`, cuarta tanda).

Tareas: T8 informe-ubicacion (Talavera de la Reina: padrón, renta, paro, criminalidad), T9 comparar-municipios (Getafe,
Leganés, Alcorcón y Fuenlabrada), T10 coyuntura-hoy (IPC con avance, EPA, PIB, Euríbor, prima de riesgo), T11
empresa-nif-perfil (B86566304: concesiones e importe, ayudas de Estado, minimis, prohibiciones).

| tarea | cond. | aciertos | usos de herramienta (media) | tokens de entrada (media) | segundos (media) | error |
|---|---|---|---|---|---|---|
| T8 | M | 2/2 | 5,5 | 260.893 | 92 | |
| T8 | B | 0/2 | 32,5 | 2.173.044 | 687 | población del Censo anual (84.413) y no del padrón; renta no encontrada; criminalidad de 2025 o de la columna de 2025 |
| T9 | M | 2/2 | 7 | 323.199 | 117 | |
| T9 | B | 2/2 | 17 | 940.867 | 202 | |
| T10 | M | 2/2 | 4,5 | 195.163 | 61 | |
| T10 | B | 0/2 | 14,5 | 740.423 | 118 | prima 86 pb: bono español de septiembre menos alemán de julio (46 pb con los dos de julio) |
| T11 | M antes | 0/2 | 3 | 127.592 | 55 | 7.693,36 € en vez de 10.074,23 €: sumaron las 5 filas visibles de 9 |
| T11 | M | 2/2 | 8,5 | 422.620 | 49 | |
| T11 | B | 2/2 | 17 | 894.241 | 133 | |

| cond. | aciertos | usos de herramienta (media) | tokens de entrada (media) | segundos (media) |
|---|---|---|---|---|
| M | 8/8 | 6,4 | 300.468 | 80 |
| B | 4/8 | 20,3 | 1.187.143 | 285 |

## Conclusiones

- Las tres herramientas se quedan: con ellas 8 de 8 frente a 4 de 8, una cuarta parte de los tokens de entrada (un 75 %
  menos) y un tercio del tiempo. Donde más ayudan es donde se cruzan fuentes con códigos distintos (T8: 0 de 2 sin
  `perfil_municipio`, con once minutos y 2,2 millones de tokens por intento) y donde hay una trampa de fechas (T10: la
  prima de riesgo con meses distintos).
- En T9 y T11 el MCP sin las herramientas acierta igual, pero con el triple de tokens y de llamadas.
- La propia evaluación encontró un fallo de `empresa_nif`: devolvía el número total de concesiones pero el importe total
  solo si cabían en las filas pedidas (5), y los dos agentes sumaron las visibles. Corregido el mismo día (0818d84): el
  total se suma sobre todas las filas y, si no se puede, `importe_total` es null con una nota. Con la corrección, 2 de 2.
- Sin medir: el índice de productos (`buscar` lo devuelve en las dos condiciones) y el almacén (exige una carga previa y
  PLACSP bloquea las ráfagas).
