"""Código listo para las fuentes del catálogo.

- sesion: requests.Session con las CA de FNMT, User-Agent de navegador, reintentos y detección de bloqueos de WAF.
- ckan, socrata, pcaxis, arcgis, ogc: clientes de las plataformas que comparten muchos portales, sin topes silenciosos.
- boe, bdns, aemet, ine_tempus, placsp, datacomex, saiku: cargadores de las fuentes más traicioneras.

Cada módulo usa solo requests y la biblioteca estándar, resuelve las trampas documentadas en las fichas y se puede
ejecutar como script para ver un ejemplo real. Importables como fuentes_publicas.clientes.<modulo> tras pip install,
o como clientes.<modulo> desde scripts/.
"""
