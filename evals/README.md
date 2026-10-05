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
(11 frente a 23) y cero fallidas o inútiles (frente a 8).

Segunda tanda (`resultados-2026-10-01.md`): tareas difíciles con el modelo por defecto y con Claude Sonnet, y entrada
ligera. Acierto igual; con catálogo, la mitad de llamadas y casi ninguna fallida.

Tercera tanda (`resultados-2026-10-01-tanda3.md`): siete trampas silenciosas con Claude Haiku, condición MCP, tres
repeticiones y tokens medidos con `consumo.py`. Sin catálogo 3 de 21, con ficheros 10 de 21 y con MCP 13 de 21, con un
30 % y un 43 % menos de tokens de entrada. Con el campo `alerts`, las tres trampas que seguían fallando pasan de 5 a 18
de 18 cuando la alerta dice la operación exacta con un ejemplo numérico.

Cuarta tanda (`resultados-2026-10-05-tanda4.md`): `perfil_municipio`, `coyuntura` y `empresa_nif` con Haiku, MCP completo
frente al mismo MCP sin ellas (`EVAL_SIN` en `mcp_cli.py`). 8 de 8 frente a 4 de 8, un 75 % menos de tokens de entrada y
un tercio del tiempo; encontró y corrigió un importe total de `empresa_nif` que faltaba con más de 5 concesiones.

Quinta tanda (`resultados-2026-10-05-tanda5.md`): bloques nuevos de `perfil_municipio` (compraventa, certificados
energéticos, cerca y viviendas turísticas) con Haiku, MCP completo frente al mismo MCP sin esos bloques
(`EVAL_SIN=perfil_municipio.bloque`). 9 de 10 frente a 7 de 10, un 59 % menos de tokens de entrada y un 60 % menos de
tiempo; encontró tres trampas que las fichas no decían o decían mal, corregidas el mismo día.

La columna tokens de las dos primeras tandas es el contexto final de cada agente que devuelve el arnés, no el consumo: cada turno
reenvía el contexto entero, así que los tokens procesados crecen con el número de pasos, que el catálogo reduce en las
tareas difíciles. La tercera tanda ya suma la entrada de cada turno desde la transcripción del agente (campo usage de
cada mensaje, `consumo.py`).

## Qué mide y qué no

Mide llamadas evitadas, errores evitados y tokens gastados en tareas típicas; no mide cobertura (para eso está
`indices/necesidades.yaml`) ni frescura (para eso está `verificacion.yml`). Ejecutarla cuesta llamadas de API del
modelo; no hay ejecutor automático en el repo. `python scripts/check_recetas.py` no la ejecuta: las `check` de aquí
son la referencia para puntuar a mano o con el arnés que se use.

Sexta tanda (`resultados-2026-10-05-tanda6.md`): almacén local (`almacen_sql`) y bloque `productos` de `buscar` con Haiku,
MCP completo frente al mismo MCP sin ellos (`EVAL_SIN=almacen_sql,buscar.productos`). Productos, 4 de 4 frente a 2 de 4 y
un 38 % menos de tokens: sin él no se encuentra la pieza que ya hace un producto. El almacén no se descubría solo (0 de 4
en el BORME hasta avisar desde `buscar`, `boe_sumario` y los errores SQL); con los avisos, 4 de 4 en BORME y BDNS igual
que sin él, pero con un 36 % menos de tokens y en 69 s frente a 170 s. Licitaciones de obras de un día, 0 de 4 con y sin
almacén. Sacó siete fallos de código, entre ellos la fecha de publicación de PLACSP (274 obras frente a 126).
