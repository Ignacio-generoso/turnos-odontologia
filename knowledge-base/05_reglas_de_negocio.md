# Reglas de Negocio

Cada regla tiene un código único `RN-{DOMINIO}-{NN}` para trazabilidad con historias de usuario, pruebas y código.

---

## Dominio: Autenticación y Privacidad Clínica (RN-AU)

- **RN-AU-01 — Aislamiento lógico por consultorio**: toda consulta y mutación de datos privados debe filtrarse obligatoriamente por el `consultorio_id` asociado al usuario autenticado (o al `slug` en rutas públicas).
- **RN-AU-02 — Acceso exclusivo a Historia Clínica y Odontograma**: únicamente los usuarios con rol `odontologo` activo pueden consultar o crear registros en `historias_clinicas`, `odontogramas` y `planes_tratamiento`. Los roles `recepcion`, `administracion` y `dueno` (sin rol clínico `odontologo`) tienen denegado el acceso (`403 Forbidden`).
- **RN-AU-03 — No repudio y conservación de registros clínicos**: no se permite eliminar físicamente evoluciones clínicas ni snapshots de odontograma; toda corrección se registra como una nueva versión o nota aclaratoria vinculada al odontólogo autenticado.
- **RN-AU-04 — Acceso público acotado por token**: el paciente sin cuenta solo puede ver, confirmar o cancelar **su propio turno** mediante un `token_publico` único e impredecible, sin exponer datos de otros pacientes ni recursos internos (como el nombre del sillón si no es necesario).

---

## Dominio: Agenda, Prestaciones y Sillones (RN-AG)

- **RN-AG-01 — Duración variable según tipo de prestación**: todo turno toma su duración inicial (`duracion_minutos`) de la prestación seleccionada en el catálogo del consultorio (ej. control 20 min, limpieza 40 min, endodoncia 60 min). En carga interna (recepción u odontólogo), la duración puede ajustarse manualmente dentro de los límites válidos (`> 0`); en reserva pública online se aplica estrictamente la duración configurada de la prestación.
- **RN-AG-02 — Asignación obligatoria de sillón o box**: todo turno activo (`estado != 'cancelado'`) debe tener asignado tanto un `profesional_id` como un `sillon_id` pertenecientes al mismo `consultorio_id` y activos al momento de la reserva. En reserva pública online, el sistema asigna automáticamente el primer sillón/box libre compatible (priorizando el `sillon_preferido_id` de la disponibilidad del profesional si está libre).
- **RN-AG-03 — Prevención de solapamientos por profesional**: un profesional no puede tener dos turnos activos (`estado != 'cancelado'`) cuyos intervalos `[inicio, fin)` se superpongan, ni un turno que invada un `bloqueo_agenda` vigente para ese profesional. Se valida en aplicación y mediante constraint `EXCLUDE` en PostgreSQL para evitar condiciones de carrera.
- **RN-AG-04 — Prevención de solapamientos por sillón/box**: un sillón/box no puede tener dos turnos activos (`estado != 'cancelado'`) cuyos intervalos `[inicio, fin)` se superpongan (incluso si corresponden a profesionales distintos), ni un turno que invada un `bloqueo_agenda` vigente para ese sillón/box. Se garantiza también mediante constraint `EXCLUDE` en PostgreSQL.
- **RN-AG-05 — Disponibilidad horaria del profesional**: solo se ofrecen o validan turnos dentro de las franjas activas de `disponibilidades_profesional` (salvo sobrecarga explícita permitida solo a recepción/dueño en agenda interna para agendar fuera de las franjas habituales, respetando siempre sin excepciones `RN-AG-03` —sin solapamiento por profesional— y `RN-AG-04` —sin solapamiento por sillón/box—). En reserva pública nunca se permite sobrepasar la disponibilidad configurada.
- **RN-AG-06 — Anticipación mínima configurable para cancelar**: el paciente puede cancelar online desde `/turno/{token}` únicamente si falta al menos `consultorio.anticipacion_minima_cancelacion_hs` horas (por defecto `24` hs) respecto a `turno.inicio`. Pasado ese límite, la cancelación online se bloquea e informa que debe comunicarse por WhatsApp/teléfono con recepción; recepción sí puede cancelar o marcar `ausente` administrativamente registrando motivo.
- **RN-AG-07 — Máquina de estados del turno**:
  - Estados válidos: `reservado` → `confirmado` → `en_atencion` → `atendido`.
  - Transiciones alternativas permitidas: `reservado`/`confirmado` → `cancelado` (libera profesional, sillón y elimina/cancela el evento en Google Calendar) o `ausente` (cuando el paciente no asiste, sin liberar retroactivamente).
  - Un turno `atendido`, `ausente` o `cancelado` no puede reprogramarse; debe crearse un nuevo turno.
- **RN-AG-08 — Ventana de reprogramación**: reprogramar un turno mantiene su `id` y trazabilidad, actualiza `inicio`, `fin`, `sillon_id` y/o `profesional_id` validando `RN-AG-03` y `RN-AG-04`, registra auditoría y dispara actualización en Google Calendar.

---

## Dominio: WhatsApp y Notificaciones (RN-WA)

- **RN-WA-01 — Opt-in explícito para WhatsApp**: solo se habilita el botón de envío asistido (`wa.me`) para recordatorios si el paciente tiene `opt_in_whatsapp = true` (o si otorgó consentimiento al confirmar su reserva online). El rechazo/baja de opt-in debe quedar registrado con marca temporal.
- **RN-WA-02 — Envío asistido sin costo automático en v1**: en v1 el sistema genera la URL `https://wa.me/{telefono}?text={mensaje_codificado}` con los datos del turno (fecha, hora, profesional y link `/turno/{token}` para confirmar/cancelar). El envío efectivo lo ejecuta el operador en 1 clic sin consumo de API paga.

---

## Dominio: Integración Google Calendar (RN-GC)

- **RN-GC-01 — Sincronización unidireccional en v1**: todo turno creado, confirmado/reprogramado o cancelado para un profesional con cuenta de Google Calendar conectada dispara una sincronización `Sistema → Google Calendar` (crear, actualizar o eliminar evento). Los cambios hechos manualmente dentro de Google Calendar no modifican la agenda del sistema en v1.
- **RN-GC-02 — Resiliencia ante fallos de Google**: un fallo temporal de la API de Google Calendar **no** debe impedir guardar, reprogramar ni cancelar un turno en PostgreSQL. El evento queda en estado `pendiente` o `error` en `google_calendar_sync_events` para reintento automático o manual.
- **RN-GC-03 — Privacidad en el título del evento externo**: el evento creado en Google Calendar debe contener información operativa suficiente para el profesional (ej. prestación, inicial/nombre del paciente y estado) sin volcar diagnósticos ni contenido de historia clínica.

---

## Dominio: Clínica, Presupuestos, Pagos y Obras Sociales (RN-CL / RN-PG)

- **RN-CL-01 — Trazabilidad de versiones en odontograma y presupuestos**: cada modificación confirmada del odontograma genera una nueva versión incremental (`version + 1`) conservando el historial previo. Al modificar un presupuesto ya `emitido` o `aceptado`, se marca el anterior como `reemplazado` y se crea una nueva versión vinculada por `presupuesto_padre_id`.
- **RN-PG-01 — Registro manual de señas y pagos en v1**: las señas y pagos se cargan manualmente especificando `tipo`, `medio_pago`, `monto_ars > 0` y `fecha_pago`. No existe cobro automático con pasarela en v1.
- **RN-PG-02 — Inmutabilidad contable de pagos**: un pago registrado nunca se elimina ni se edita en su monto; ante error, solo `administracion` (o `dueno`) puede pasarlo a estado `anulado` indicando un `motivo_anulacion` obligatorio, generando evento en auditoría.
- **RN-OS-01 — Cobertura de obra social meramente informativa en v1**: el sistema permite asociar obras sociales/planes al paciente y registrar un `cupo_mensual_referencia` informativo por obra social, pero **no** bloquea ni rechaza turnos automáticamente al alcanzar ese número en v1 (solo muestra un indicador informativo en la pantalla de turno/exportación).
- **RN-AU-05 — Auditoría básica obligatoria**: toda creación/reprogramación/cancelación de turno, cambio de estado a `ausente`, emisión/aceptación/reemplazo de presupuesto, registro/anulación de pago y modificación de historia clínica/odontograma debe registrar una entrada en `auditoria_eventos`.
