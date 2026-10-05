# Resultados de la evaluación · 2026-10-05 (quinta tanda: bloques nuevos de perfil_municipio)

Mide si los bloques que `perfil_municipio` ganó el 2026-10-05 (compraventa, certificados energéticos, cerca y
viviendas turísticas) ahorran tiempo o errores frente al mismo MCP sin ellos. Claude Haiku 4.5 con Bash y el catálogo
solo por `evals/mcp_cli.py`; dos condiciones: M (MCP completo) y B (el mismo MCP con
`EVAL_SIN=perfil_municipio.compraventa,perfil_municipio.certificados_energeticos,perfil_municipio.cerca,perfil_municipio.viviendas_turisticas`,
que quita esos bloques de la respuesta; las fichas, con sus alertas, siguen en las dos). Dos repeticiones por tarea y
condición. Tokens de entrada reales con `consumo.py`. Referencias tomadas con llamadas reales el mismo día
(`tareas.yaml`, quinta tanda).

Tareas: T12 compraventa-palma, T13 certificados-edificio (calle Colón 10, València), T14 colegios-cerca-madrid (calle
Alcalá 50), T15 recarga-cerca-alicante (calle Torres Quevedo 42), T16 viviendas-turisticas-madrid.

| tarea | cond. | aciertos | usos de herramienta (media) | tokens de entrada (media) | segundos (media) | error |
|---|---|---|---|---|---|---|
| T12 | M | 2/2 | 7,5 | 347.865 | 63 | |
| T12 | B | 1/2 | 15 | 801.480 | 140 | 1.080 compraventas: la columna de 2026-T1, no la de 2026-T2 (año y trimestre en dos filas de cabecera) |
| T13 | M | 2/2 | 3,5 | 154.741 | 62 | |
| T13 | B | 2/2 | 14 | 755.498 | 185 | (una repetición añadió una cuarta vivienda con certificado caducado del CSV del IVACE, bien explicada) |
| T14 | M | 2/2 | 9 | 450.236 | 85 | |
| T14 | B | 1/2 | 9,5 | 486.198 | 134 | 17 centros y el «más cercano» a 8,5 km: dirección mal geocodificada |
| T15 | M | 1/2 | 9,5 | 475.898 | 111 | 7 emplazamientos: no usó perfil_municipio y geocodificó con Nominatim, que pone la calle en Elche |
| T15 | B | 1/2 | 21,5 | 1.263.184 | 336 | 17 «emplazamientos»: sumó puntos de recarga (refillPoint), como sugería la alerta |
| T16 | M | 2/2 | 3,5 | 175.168 | 40 | |
| T16 | B | 2/2 | 11 | 581.986 | 94 | |

| cond. | aciertos | usos de herramienta (media) | tokens de entrada (media) | segundos (media) |
|---|---|---|---|---|
| M | 9/10 | 6,6 | 320.782 | 72 |
| B | 7/10 | 14,2 | 777.669 | 178 |

## Conclusiones

- Los cuatro bloques se quedan: con ellos 9 de 10 frente a 7 de 10, un 59 % menos de tokens de entrada y un 60 %
  menos de tiempo. Sin ellos, las alertas de las fichas bastan a menudo (T13 y T16, 2 de 2), pero con el doble o el
  triple de llamadas, y fallan donde hay que geocodificar y calcular distancias (T14, T15) o leer una cabecera rara (T12).
- La evaluación encontró tres trampas que las fichas no decían o decían mal, corregidas el mismo día (0fba0f1 y el
  commit de este informe): la cabecera de 34010210 (2026-T1 frente a 2026-T2), una alerta de la DGT que llevaba a sumar
  puntos de recarga como emplazamientos, y que el WFS valenciano no conserva todos los certificados caducados.
- El único fallo de M fue de descubrimiento: el agente buscó «recarga eléctrico», abrió la ficha de la DGT y no llegó
  a `perfil_municipio`. La ficha lleva ahora un tip que lo dice y avisa de que Nominatim sitúa «Torres Quevedo 42
  Alicante» en Elche.
