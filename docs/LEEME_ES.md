# Guía de uso de la versión experimental publicada

El código está publicado en [Continuity-reframe](https://github.com/LokoJeans27/Continuity-reframe). Consulta [QUICKSTART](QUICKSTART.md) para requisitos y comandos; se ejecutan desde la raíz del repositorio. No se incluye un instalador completo ni un par de video/guía listo para generar con H3.

## Dos formas de elegir la intención de cámara

- Abre `ui/camera_picker.html`, carga la ficha creada por `prepare`, elige un plano y ajusta los controles. El esquema es conceptual. Conserva el texto manual y exporta una ficha nueva que todavía requiere revisión.
- Para el visor girable, empieza por [el ejemplo sintético](../examples/camera_intent/README.md): incluye un JPEG válido, un proxy y `studio.html` listo para abrir localmente. Es geometría artificial de prueba, no una reconstrucción de una escena real. Para tu propio fotograma debes preparar el proxy externamente y seguir [CAMERA_INTENT](CAMERA_INTENT.md). El kit no convierte video en splat ni estima profundidad automáticamente.

La imagen guía sigue siendo un paso **externo y manual** en ChatGPT, FLUX u otra herramienta autorizada. El visor exporta coordenadas y un prompt editable, no una imagen nueva. Adjunta el original manualmente; usa la captura del proxy solo si ayuda a expresar orientación. Su JSON no sustituye a `scene-reviewed.json` de H3.

Decide qué objetos deberían verse antes de pedir la guía. Revisa postura inicial, manos, fondo, oclusiones y margen del gesto; después completa los campos y las aprobaciones booleanas de la ficha. No hay llamadas automáticas a ChatGPT ni a una API de pago.

`build` conserva la referencia original por separado y admite `--width`, `--height` y `--ref-image-size match|max`. Hay ensayos a 800×480 y 960×576, pero no se ha determinado el máximo absoluto de la GPU. Los [ensayos recientes](CAMERA_INTENT_TRIAL.md) con guías moderada y cenital completaron H3 y conservaron rasgos generales de actuación; también mostraron errores de pose, mano y espacio inferido. No validan fidelidad exacta.

El nodo opcional `h3_camera_brief` añade texto/control de cámara dentro de ComfyUI. Las generaciones comprobadas usaron la **API local de ComfyUI**, no la API pagada de MiniMax. La imagen sigue siendo externa; la instalación del nodo y la importación del workflow visual son manuales.

Usa carpetas nuevas. Tras un timeout revisa cola e historial antes de repetir una solicitud. Ejecuta `compare` solo después de que `collect` indique `COLLECTED`. El audio de comparación corresponde al clip preparado; no demuestra sincronía labial exacta.

Se incluyen capturas ilustrativas autorizadas, el tutorial anterior y el ejemplo sintético. No se incluyen videos privados, guías personales ejecutables, pesos ni credenciales. MIT cubre el código propio; los modelos y medios conservan sus términos separados. La opción oficial de API 2K está documentada, pero no integrada ni probada. El tutorial grabado es anterior al nuevo visor y no lo demuestra.
