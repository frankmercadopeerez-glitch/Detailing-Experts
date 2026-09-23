# Publicación y pendientes — 23 de septiembre de 2026

## Publicado

Sitio: https://detailing-experts.vercel.app/

Portal: https://detailing-experts.vercel.app/portal/

Se publicaron el favicon original azul, los iconos de instalación y las correcciones de la auditoría del 15 de septiembre. Esta actualización sustituye el estado «solo local» de aquel informe. El primer despliegue de esta entrega fue `dpl_HmoWt8mvcx8y2h3v1wFZ3hiGE9vf`, estado READY, desde el código `8df8b29`. La comprobación visual detectó además una regla CSS que mostraba el acceso por SMS pese a estar deshabilitado; se corrigió respetando el atributo `hidden`.

## Evidencia

- Compilación correcta y 24 pruebas unitarias/API aprobadas en esta sesión.
- Auditoría estructural: 236 páginas, 2.894 referencias locales y 596 bloques JSON-LD sin incidencias en las comprobaciones implementadas.
- Dominio público: inicio, servicios, contacto, artículo de muestra, portal, administración, manifiestos e iconos responden 200.
- El favicon publicado coincide byte a byte con el archivo del logo original. El portal publicado contiene las acciones de vinculación de clientes y respuesta de privacidad.
- El API privado rechaza peticiones anónimas con 401. Portal y administración entregan CSP y `noindex`.
- Producción sigue declarando `photos:false`, `payments:false`, `notifications:false`.
- Revisión de acceso y registro con navegador de escritorio emulando tamaños móviles y PC. Esto no sustituye probar Safari/iPhone, Android ni una sesión real de cliente y administrador. Las pantallas privadas se verificaron anteriormente con datos de demostración y pruebas de servidor, no con una nueva sesión real en esta publicación.

## Prioridad 1 — completar recorridos reales

| Área | Qué falta | Criterio para darlo por terminado |
| --- | --- | --- |
| Fotografías | Conectar ImageKit y verificar acceso privado | Subir antes/proceso/después en PRB001 desde móvil y PC; verlas desde la cuenta correspondiente; otra cuenta no puede acceder |
| Registro | Probar correo, Google, verificación, recuperación y vinculación con cuentas de prueba | El cliente entra, recupera acceso y encuentra únicamente su historial; el administrador completa la vinculación |
| Avisos | Configurar push/VAPID y ejecución programada de recordatorios | Llega un aviso real al dispositivo y al portal; desactivar preferencias detiene push; no hay duplicados |
| Pagos | Conectar Wompi si se usarán pagos en línea y añadir registro auditado de efectivo/transferencia si el taller los acepta | El saldo cambia solo tras confirmación válida; se conserva quién registró cada pago y su referencia |
| Datos personales | Procedimiento efectivo de exportación/eliminación | El equipo entrega o elimina lo correspondiente y registra la respuesta; el botón actual solo gestiona la solicitud |

## Prioridad 2 — cada cosa en su sitio

### Cliente móvil

- Concentrar la navegación en cuatro o cinco destinos principales y un menú «Más». Actualmente la barra desplaza horizontalmente sus secciones.
- Dar prioridad a estado del vehículo, próxima cita, fotos y contacto; agrupar configuración y privacidad dentro de Mi cuenta.
- Mostrar con claridad el avance de vinculación y la diferencia entre fecha solicitada y cita confirmada.
- Probar teclado abierto, errores de formulario, texto ampliado, pérdida de conexión y aplicación instalada en dispositivos reales.

### Administrador móvil y PC

- Menú lateral persistente en PC y menú compacto en móvil, especialmente para las diez secciones administrativas.
- Completar edición y archivo de clientes/vehículos; hoy hay creación y vinculación, pero no un recorrido completo de corrección de datos desde la interfaz.
- Sustituir el checklist escrito con `[x]` por controles visuales para marcar, añadir y ordenar tareas.
- Añadir búsqueda sobre todos los registros, filtros persistentes y totales globales. La búsqueda actual opera sobre las páginas cargadas.
- Agenda con duración, disponibilidad y capacidad de atención; la protección actual evita coincidencias de hora exacta, no todos los solapamientos de trabajos.
- Gestión de fotografías erróneas: vista ampliada, corrección de descripción y eliminación con confirmación; atender cargas fallidas y reservas de almacenamiento pendientes.
- Definir permisos por función si trabajarán varias personas y probar recuperación de acceso administrativo.

## Prioridad 3 — cierre de calidad

- Probar Chrome/Edge en PC y Safari/Chrome en teléfonos reales, orientación horizontal, teclado, zoom y lector de pantalla.
- Medir rendimiento móvil y corregir las causas observadas; no hay una medición nueva de Core Web Vitals en esta entrega.
- Confirmar copias de seguridad, restauración y un procedimiento para errores de integraciones.
- Realizar un recorrido completo: registro → vinculación → solicitud → cita → trabajo → fotos → aviso → cobro → entrega → revisión.

## Orden recomendado

Primero fotos y cuentas reales; después navegación y gestión administrativa; luego avisos, pagos y agenda; finalmente pruebas de dispositivos y operación. La interfaz publicada es utilizable, pero no corresponde afirmar que todo está completo mientras esas integraciones y recorridos sigan pendientes.
