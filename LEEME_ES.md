# Guía rápida de revisión

Abre `camera_picker.html` para elegir frontal, tres cuartos, lateral, abierto, cenital, bajo o espaldas y afinar azimut, elevación y distancia. Carga primero la ficha generada por `prepare`. El esquema representa una intención: no reconstruye el escenario ni controla una cámara exacta.

La imagen sigue siendo un paso **manual** en ChatGPT, FLUX u otra herramienta. Decide qué objetos deberían verse antes de pedir la imagen. Revisa postura inicial, manos, fondo, oclusiones y margen para el gesto; después completa la ficha y sus aprobaciones. No hay llamadas automáticas ni API de pago.

El README contiene los comandos de preparación, generación y comparación. `build` conserva la referencia original por separado y permite `--width`, `--height` y `--ref-image-size match|max`. Para empezar, 800×480/max tiene pruebas completadas en sentado y puente; consulta los resultados de960 antes de elegir. No se ha determinado el máximo absoluto de la GPU.

El nodo opcional `h3_camera_brief` añade controles dentro de ComfyUI y ya completó generaciones H3 por API. Requiere copiar su carpeta a custom_nodes y reiniciar cuando no haya trabajos; el kit no lo instala solo. Importa el workflow visual generado para cada ejecución y actualiza las listas del navegador. La aceptación interactiva del navegador sigue pendiente.

Usa siempre carpetas nuevas. No repitas una solicitud tras un timeout sin revisar historial y cola. Compara video fuente, guía y resultado: más resolución no corrigió la mano recortada ni el fallo de bajada del brazo mecánico del puente.

No se incluyen medios privados, pesos ni credenciales. No se ha publicado nada. El titular autorizó MIT para el código propio; consulta LICENSE; las restricciones de H3 y los derechos de los videos se mantienen.


Version23: consulta README.md para FLUX->H3 ya probado mediante transferencia manual, equipo y resultados800/960, limites y estado de licencias. La API2K esta documentada oficialmente pero no fue probada ni integrada. No se publico nada.
