# Resultados de la evaluación · 2026-10-01 (segunda tanda)

> Corrección del 2026-10-01: la columna tokens es la que devuelve el arnés al terminar cada agente, que es el tamaño de su
> contexto final, no los tokens procesados (cada turno reenvía el contexto entero; un agente de prueba con 7 turnos marcó
> 44.535 y procesó 306.004 de entrada). Las comparaciones de tokens de este fichero no miden coste; las de llamadas,
> fallidas, usos de herramienta y tiempo siguen valiendo.

Tres preguntas que la primera tanda dejó abiertas: qué pasa en las tareas difíciles (clave de AEMET, CODICE de PLACSP, DataComex,
Atlas de renta del INE con filtro tv, API Saiku del portal de violencia de género), qué pasa con un modelo más barato (Claude Sonnet)
y cuánto ahorra una entrada ligera (`llms-min.txt`, 7 KB) frente a `llms.txt` entero (33 KB). Mismo protocolo que la primera tanda:
una ejecución por tarea y condición, agente con Bash, curl y python en un sandbox; A sin catálogo, B con `llms.txt` y las fichas,
C con `llms-min.txt` y las fichas. Credenciales de AEMET y DataComex disponibles en todas las condiciones.

## Tareas difíciles, modelo por defecto (Claude Fable)

A sin catálogo, B con catálogo.

| tarea | cond. | correcta | llamadas HTTP | fallidas | tokens | usos de herramienta | segundos |
|---|---|---|---|---|---|---|---|
| exportaciones-trigo | A | sí | 7 | 0 | 61.166 | 11 | 99 |
| exportaciones-trigo | B | sí | 3 | 0 | 70.938 | 9 | 79 |
| licitaciones-obras-hoy | A | sí | 16 | 0 | 110.380 | 28 | 594 |
| licitaciones-obras-hoy | B | sí | 11 | 0 | 121.976 | 13 | 1050 |
| llamadas-016-2024 | A | sí | 15 | 3 | 77.649 | 18 | 232 |
| llamadas-016-2024 | B | sí | 5 | 0 | 69.348 | 10 | 70 |
| prediccion-cuenca | A | sí | 2 | 0 | 48.658 | 4 | 38 |
| prediccion-cuenca | B | sí | 3 | 1 | 70.187 | 6 | 73 |
| renta-abengibre | A | sí | 10 | 1 | 56.640 | 13 | 193 |
| renta-abengibre | B | sí | 2 | 0 | 69.847 | 5 | 75 |

| total | cond. | correctas | llamadas | fallidas | tokens | usos de herramienta | segundos |
|---|---|---|---|---|---|---|---|
| 5 tareas | A | 5/5 | 50 | 4 | 354.493 | 74 | 1156 |
| 5 tareas | B | 5/5 | 24 | 1 | 402.296 | 43 | 1347 |

- exportaciones-trigo (A): acierta leyendo la página de ayuda de la API; descubre ObtenerPaises y ObtenerPeriodos, que no estaban en la ficha
- exportaciones-trigo (B): 29.164,8 € y 5.680 kg (julio 2026); códigos 003 y 28 de codigos.yaml; recortó el prefijo token:
- licitaciones-obras-hoy (A): respuesta más completa que la del feed: automatizó el buscador JSF del portal (viewstate) y encontró 11 anuncios nuevos de hoy; el feed iba 14 horas por detrás de la web
- licitaciones-obras-hoy (B): recorrió las 7 páginas del feed (3.122 entradas) y el agregado 1044; demostró que el feed 643 se regenera una vez al día hacia las 20:15 y el 1044 hacia las 03:00; páginas de unas 500 entradas y 14 a 16 MB
- llamadas-016-2024 (A): acierta tras leer el JavaScript del portal para deducir la ruta /saiku/rest; tres llamadas fallidas (404, 404, 500)
- llamadas-016-2024 (B): 106.196 por la API Saiku con el flujo de la ficha (cookie, MDX, CSV)
- prediccion-cuenca (A): conoce los dos pasos de AEMET; 22/15 y 100 % para el 2 de octubre, coincide con la referencia
- prediccion-cuenca (B): 22/15 y 100 %; un 429 por el límite por minuto (compartido con los otros agentes), esperó 65 s como dice la ficha
- renta-abengibre (A): acierta por la tabla nacional 30824 con dos filtros tv tras un intento sin filtro rechazado por volumen; cinco veces más llamadas
- renta-abengibre (B): 14.105 € (2023) con la tabla 30656 y tv=19:6124 de la receta

## Tareas difíciles, Claude Sonnet

Mismas tareas con un modelo más barato.

| tarea | cond. | correcta | llamadas HTTP | fallidas | tokens | usos de herramienta | segundos |
|---|---|---|---|---|---|---|---|
| exportaciones-trigo | A | sí | 8 | 0 | 53.557 | 12 | 91 |
| exportaciones-trigo | B | sí | 4 | 0 | 66.112 | 9 | 39 |
| licitaciones-obras-hoy | A | sí | 3 | 0 | 62.535 | 6 | 126 |
| licitaciones-obras-hoy | B | sí | 4 | 0 | 89.215 | 16 | 169 |
| llamadas-016-2024 | A | sí | 17 | 2 | 82.427 | 26 | 155 |
| llamadas-016-2024 | B | sí | 7 | 0 | 68.796 | 7 | 36 |
| prediccion-cuenca | A | sí | 2 | 0 | 47.990 | 3 | 24 |
| prediccion-cuenca | B | sí | 4 | 0 | 71.324 | 9 | 35 |
| renta-abengibre | A | sí | 5 | 0 | 53.226 | 6 | 49 |
| renta-abengibre | B | sí | 2 | 0 | 66.278 | 6 | 34 |

| total | cond. | correctas | llamadas | fallidas | tokens | usos de herramienta | segundos |
|---|---|---|---|---|---|---|---|
| 5 tareas | A | 5/5 | 35 | 2 | 299.735 | 53 | 445 |
| 5 tareas | B | 5/5 | 21 | 0 | 361.725 | 47 | 313 |

- exportaciones-trigo (A): Sonnet acierta vía WebSearch y la ayuda oficial; descubre ObtenerTarics (7,5 MB) y que la ayuda oficial llama horses al 1001
- exportaciones-trigo (B): 29.164,8 € y 5.680 kg; parámetros y códigos de la ficha a la primera
- licitaciones-obras-hoy (A): Sonnet parsea CODICE sin ayuda; detecta que el feed no tiene entradas de hoy a las 10:22 y lo dice sin inventar
- licitaciones-obras-hoy (B): revisó también el feed agregado 1044 que cita la ficha y encontró la única entrada de hoy con CPV 45 y más de un millón; señala que updated no es la fecha de publicación
- llamadas-016-2024 (A): Sonnet acierta tras leer cinco ficheros JavaScript del portal para deducir la API; 17 llamadas y 26 usos de herramienta frente a 7 y 7 con la ficha
- llamadas-016-2024 (B): 106.196 por la API Saiku siguiendo la ficha; verificación con una segunda sesión y CSV
- prediccion-cuenca (A): Sonnet conoce los dos pasos de AEMET; 22/15 y 100 %
- prediccion-cuenca (B): 22/15 y 100 %; confirmó el código INE de Cuenca con el maestro porque el catálogo no lo trae
- renta-abengibre (A): Sonnet acierta bajando la tabla provincial entera (780 KB) y la serie ADRH103925
- renta-abengibre (B): 14.105 € (2023) con tabla 30656 y tv de la receta

## Tareas fáciles con entrada ligera

Las cinco tareas de la primera tanda; A y B son las cifras del 2026-09-30, C es `llms-min.txt` el 2026-10-01.

| tarea | cond. | correcta | llamadas HTTP | fallidas | tokens | usos de herramienta | segundos |
|---|---|---|---|---|---|---|---|
| boe-disposiciones-dia | A | sí | 3 | 0 | 49.256 | 6 | 59 |
| boe-disposiciones-dia | B | sí | 4 | 0 | 71.022 | 9 | 110 |
| boe-disposiciones-dia | C (min) | sí | 3 | 0 | 56.635 | 8 | 83 |
| direccion-a-codigo-ine | A | sí | 1 | 0 | 46.780 | 3 | 35 |
| direccion-a-codigo-ine | B | sí | 1 | 0 | 65.863 | 5 | 52 |
| direccion-a-codigo-ine | C (min) | sí | 1 | 0 | 53.734 | 5 | 47 |
| gasolinera-mas-barata | A | sí | 2 | 0 | 50.511 | 5 | 55 |
| gasolinera-mas-barata | B | sí | 2 | 0 | 70.824 | 7 | 78 |
| gasolinera-mas-barata | C (min) | sí | 2 | 0 | 59.170 | 7 | 69 |
| ipc-ultimo | A | sí | 9 | 0 | 55.838 | 8 | 103 |
| ipc-ultimo | B | sí | 2 | 0 | 68.209 | 6 | 66 |
| ipc-ultimo | C (min) | sí | 4 | 0 | 56.591 | 6 | 66 |
| poblacion-abengibre | A | sí | 8 | 2 | 55.979 | 9 | 113 |
| poblacion-abengibre | B | sí | 2 | 0 | 70.554 | 5 | 66 |
| poblacion-abengibre | C (min) | sí | 4 | 0 | 60.820 | 7 | 195 |

| total | cond. | correctas | llamadas | fallidas | tokens | usos de herramienta | segundos |
|---|---|---|---|---|---|---|---|
| 5 tareas | A | 5/5 | 23 | 2 | 258.364 | 31 | 365 |
| 5 tareas | B | 5/5 | 11 | 0 | 346.472 | 32 | 372 |
| 5 tareas | C (min) | 5/5 | 14 | 0 | 286.950 | 33 | 460 |

- boe-disposiciones-dia (A): API del BOE con Accept de memoria; detecta que no hay sección I ese día
- boe-disposiciones-dia (B): sin sección I ese día; lo contrastó con XML, HTML y el día anterior como control
- boe-disposiciones-dia (C (min)): con llms-min; sin sección I ese día, contrastado con HTML y el día anterior
- direccion-a-codigo-ine (A): CartoCiudad de memoria; muniCode 28079, provinceCode 28
- direccion-a-codigo-ine (B): CartoCiudad desde la ficha cnig; leyó llms.txt, la ficha y una receta
- direccion-a-codigo-ine (C (min)): con llms-min; leyó necesidades.yaml por grep y la ficha cnig
- gasolinera-mas-barata (A): API MINETUR de memoria; 1,735 en Iniesta, coincide con la referencia
- gasolinera-mas-barata (B): 1,735 en Iniesta; leyó ficha, receta y códigos
- gasolinera-mas-barata (C (min)): con llms-min; 1,735 en Iniesta; códigos de provincia y producto de codigos.yaml
- ipc-ultimo (A): acierta al final, pero 6 de las 9 llamadas fueron a la serie IPC251852 (base 2021, cerrada en diciembre de 2025) que recordaba de memoria
- ipc-ultimo (B): 104,638 de 2026M08 con nult=2 por la trampa documentada; comprobó que septiembre solo tiene avance
- ipc-ultimo (C (min)): con llms-min; 104,638 de 2026M08; leyó solo la ficha del INE
- poblacion-abengibre (A): 753 (2025) por la tabla provincial 2855; dos URL de INEbase adivinadas dieron 404
- poblacion-abengibre (B): 753 (2025) con tv=19:6124 de la receta; comprobó vigencia de la tabla
- poblacion-abengibre (C (min)): con llms-min; obtuvo el Id 6124 con VALORES_VARIABLEOPERACION/19/22 como dice la ficha; 753 (2025)

## Lectura

- Acierto igual en todas las condiciones y modelos (todas las tareas resueltas). La diferencia vuelve a estar en el
  camino: en las tareas difíciles el catálogo reduce las llamadas HTTP a la mitad (50 a 24 con el modelo por defecto,
  35 a 21 con Sonnet) y casi elimina las fallidas o inútiles (ensayos de rutas, series cerradas, JavaScript del portal
  para deducir una API). El tiempo baja un 30 % con Sonnet; con el modelo por defecto sube en conjunto porque la
  tarea de PLACSP con catálogo recorrió 100 MB de feed (17 minutos) para ser exhaustiva.
- Con Sonnet la diferencia es mayor que con el modelo por defecto en las tareas con API no documentada (016: 17
  llamadas y 26 usos de herramienta sin catálogo frente a 7 y 7 con él).
- `llms-min.txt` deja el sobrecoste de tokens del catálogo en un 11 % sobre no usarlo (frente al 34 % de `llms.txt`),
  manteniendo la reducción de llamadas.
- PLACSP es la excepción que enseña algo: sin catálogo, el agente automatizó el buscador JSF del portal y encontró
  anuncios de hoy que el feed aún no tenía; con catálogo siguió la ficha (feed) y descubrió que el feed se regenera
  una vez al día hacia las 20:15. Las dos cosas están ahora en la ficha.
- Sigue siendo una ejecución por tarea y condición: orientan, no demuestran.
