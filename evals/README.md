# Medir lo que aporta el repo

`tareas.yaml` son 20 peticiones reales con la respuesta que debe darse, las fichas que la resuelven, una llamada de
referencia y la trampa que hace fallar a quien no conoce la fuente. Sirven para comparar un agente con y sin el repo.

## Protocolo

1. Mismo modelo, misma petición literal (`ask`), un solo intento por condición, sin ayuda humana.
2. Condición A (sin repo): el agente tiene navegación y ejecución de código, nada más.
3. Condición B (con repo): además recibe `llms.txt` en el contexto, o tiene el servidor MCP (`guides/servidor-mcp.md`).
4. Se registran por tarea: correcta (sí o no, comparando con `expected` y con el valor que devuelve `check` en ese
   momento), llamadas HTTP hechas, llamadas fallidas (código distinto de 2xx o cuerpo inservible), tokens de entrada
   y salida, y tiempo.
5. Resultado: tabla por tarea y totales de las dos condiciones en `evals/resultados-AAAA-MM-DD.md`.

Las tareas con `check.status: 401` (DataComex) se puntúan por el procedimiento (login, token, códigos), no por el
valor. La de AEMET exige `AEMET_KEY` en las dos condiciones.

## Resultados

`resultados-2026-09-30.md`: cinco tareas, una ejecución por condición. Mismo acierto (5 de 5), la mitad de llamadas HTTP
(11 frente a 23), cero fallidas o inútiles (frente a 8) y un 34 % más de tokens por leer `llms.txt` entero.

Segunda tanda (`resultados-2026-10-01.md`): tareas difíciles con el modelo por defecto y con Claude Sonnet, y entrada
ligera. Acierto igual; con catálogo, la mitad de llamadas y casi ninguna fallida; `llms-min.txt` deja el sobrecoste de tokens
en un 11 %.

## Qué mide y qué no

Mide llamadas evitadas, errores evitados y tokens gastados en tareas típicas; no mide cobertura (para eso está
`indices/necesidades.yaml`) ni frescura (para eso está `verificacion.yml`). Ejecutarla cuesta llamadas de API del
modelo; no hay ejecutor automático en el repo. `python scripts/check_recetas.py` no la ejecuta: las `check` de aquí
son la referencia para puntuar a mano o con el arnés que se use.
