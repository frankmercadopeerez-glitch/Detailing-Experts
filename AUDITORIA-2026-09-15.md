# Auditoría del sitio y portal — 15 de septiembre de 2026

## Entrega

Cambios locales en el proyecto `C:\Users\Dell\PROYECTOS WEB\Detailing-Experts`. Sin push, despliegue, cambios de configuración remota ni modificaciones de clientes reales.

## Correcciones implementadas

- El favicon faltaba en la compilación: la URL pública devolvía 404. Ahora se incluye en `dist`.
- El formulario de contacto ahora incorpora teléfono y vehículo al mensaje de WhatsApp. Explica que el usuario debe enviar el mensaje en WhatsApp.
- En móvil se oculta el botón flotante que tapaba texto; permanecen los botones de contacto dentro de las páginas.
- El menú móvil restablece `aria-expanded` al seleccionar un enlace.
- Nueva acción **Clientes → Vincular cuenta** para asociar un contacto creado por el administrador a una cuenta registrada. Requiere comprobar la identidad con el cliente, migra el historial en una transacción, registra auditoría y crea un aviso. No concede acceso automáticamente por coincidencia de placa o correo. Los historiales de más de 400 registros requieren migración asistida.
- El cliente recién registrado recibe una explicación del paso pendiente de vinculación. Se muestra su nombre del perfil. Los correos de recuperación y verificación incluyen regreso al portal.
- Se oculta el acceso por SMS mientras está deshabilitado.
- Se rechazan placas repetidas al crear vehículos para clientes existentes, citas solicitadas duplicadas y nuevas solicitudes de datos mientras exista una pendiente.
- Corregida la cancelación de trabajos: editar una cita ya cancelada no elimina la reserva de otra cita que ocupa su antiguo horario.
- La creación de trabajos y cobros comprueba también el propietario dentro de la transacción para detectar una vinculación concurrente.
- Los nuevos cobros generan un aviso dentro del portal.
- Las solicitudes de privacidad se consultan y responden desde administración; el cliente ve estado y respuesta en Mi cuenta. Marcar atendida registra la respuesta, no realiza una exportación o eliminación automática.
- Notificaciones push: el botón refleja su disponibilidad real. Los avisos internos siguen disponibles.
- Las fotos requieren ambas variables de ImageKit para figurar habilitadas. Un error al cargarlas deja un mensaje recuperable.
- Se corrige la ruta del API de fotos y la respuesta 400 para JSON preprocesado inválido.
- Se distingue un guardado correcto de un fallo posterior al actualizar la pantalla, evitando inducir al usuario a duplicar registros.
- Se limpian datos locales al cerrar sesión y se añade paginación visible a solicitudes, privacidad y mantenimientos.

## Verificación

- Compilación TypeScript/Vite.
- 24 pruebas unitarias/API: autenticación, permisos, validación, firmas y conciliación Wompi, compresión y formatos de imágenes, registro y clientes.
- 2 pruebas de integración en Firestore local: persistencia y aislamiento, reglas, conflictos, vinculación, cancelación de citas, duplicados y gestión de privacidad. No se utilizaron datos de producción.
- `node scripts/audit-public.mjs`: 236 páginas, 2.894 referencias locales y 596 bloques JSON-LD; sin destinos locales faltantes ni errores en las comprobaciones de H1, título, descripción, canonical y sintaxis JSON-LD. El informe automático se guarda en `test-results/public-audit.json`.
- Navegación de las 10 secciones administrativas y 7 del cliente en modo demostración a 390 × 844: sin desbordamiento horizontal ni errores de JavaScript observados.
- Inspección visual de inicio, contacto, catálogo, servicio, artículo, acceso, registro y formulario de vehículo. Acceso/registro revisados también a 1366 × 768 y 1920 × 900. No constituye una captura individual de las 236 páginas.

## Estado público comprobado y trabajo externo pendiente

`https://detailing-experts.vercel.app/api/portal?action=status` devolvió `configured: true`, `payments: false`, `photos: false`, `notifications: false`. Inicio y portal respondieron 200. El favicon público respondió 404 antes de publicar estas correcciones.

1. Publicar el código y verificar la versión desplegada; esta entrega está en local.
2. Comprobar un registro real con recepción de correo, verificación, recuperación y Google/App Check. La lógica se revisó, pero no se creó una cuenta real ni se enviaron correos de prueba.
3. Conectar ImageKit y probar carga y lectura privada reales. La compresión y autorización se probaron localmente.
4. Configurar push/VAPID y la ejecución programada de `/api/reminders`; verificar recepción en un dispositivo. No hay programación de cron declarada en `vercel.json`; debe comprobarse si existe un planificador externo.
5. Configurar Wompi y verificar webhook y un pago real antes de activar los pagos. Las pruebas de firmas no acreditan funcionamiento del comercio.
6. La solicitud de privacidad requiere que el equipo gestione efectivamente la copia o eliminación y registre una respuesta; el portal no automatiza ese procedimiento.

No se midieron Core Web Vitals, indexación de Google ni entrega real de WhatsApp/correo/push. Las comprobaciones estructurales de SEO no certifican posicionamiento ni la calidad editorial individual de todos los artículos.

## Flujo recomendado para el equipo

1. Registrar cliente y vehículo si todavía no existe su cuenta.
2. Pedirle que cree y verifique su cuenta, declarando su placa.
3. En Clientes, abrir Vincular cuenta en el contacto original, comprobar la cuenta con el cliente y confirmar.
4. Registrar trabajos, fechas y cobros. Las actualizaciones aparecen en Avisos; push depende de la integración pendiente.
5. Revisar Solicitudes para responder citas y solicitudes sobre datos. Una solicitud de cita atendida requiere registrar la fecha y hora confirmadas en el trabajo.
