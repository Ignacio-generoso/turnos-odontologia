# Flujos Principales

Cada flujo se documenta extremo a extremo mostrando interacciones, reglas aplicadas y manejo de errores.

---

## Flujo 1: Reserva online de turno por el paciente

**Disparador**: el paciente abre el link público `/reservar/{consultorio_slug}`.
**Actor**: Paciente.

**Pasos**:
1. El frontend solicita `GET /api/v1/public/{slug}/catalogo` (prestaciones visibles y profesionales activos).
2. El paciente selecciona prestación y profesional (o "cualquier profesional disponible") y una fecha.
3. El frontend consulta `GET /api/v1/public/{slug}/disponibilidad?prestacion_id=...&fecha=...` y obtiene slots libres donde el profesional tiene disponibilidad y existe al menos un sillón libre durante `prestacion.duracion_minutos`.
4. El paciente completa sus datos (nombre, apellido, DNI, teléfono WhatsApp, opt-in opcional) y confirma.
5. El backend ejecuta una transacción: busca/crea ficha de paciente por `(consultorio_id, dni)`, selecciona un `sillon_id` disponible, inserta el turno en `estado = 'reservado'` con `token_publico_hash`, registra `auditoria_eventos` y encola evento en `google_calendar_sync_events`.
6. El backend devuelve la confirmación con resumen del turno y el link personal `/turno/{token}`.
7. El worker/tarea async sincroniza el nuevo evento en Google Calendar (`Sistema → Google`).

**Diagrama de secuencia**:
```
Paciente → React PWA → FastAPI Public API → PostgreSQL (TX + EXCLUDE) → Worker Google Sync → Google Calendar
                                                 │
                                                 └─ ← 201 Created + /turno/{token}
```

**Casos de error**:
- **Slot tomado concurrentemente**: PostgreSQL rechaza por constraint `EXCLUDE` (`IntegrityError` SQLSTATE `23P01`) → API responde `409 Conflict` y el frontend recarga slots disponibles.
- **Google Calendar falla o no está conectado**: el turno igualmente se guarda en PostgreSQL; `google_calendar_sync_events` queda en `error`/`pendiente` para reintento posterior (`RN-GC-02`).

---

## Flujo 2: Recordatorio por WhatsApp y confirmación/cancelación online

**Disparador**: recepción revisa la agenda del día siguiente para confirmar asistencia.
**Actor**: Recepción → Paciente.

**Pasos**:
1. Recepción abre la agenda del día siguiente y filtra turnos en estado `reservado`.
2. Para cada paciente con `opt_in_whatsapp = true`, recepción hace clic en **"Enviar recordatorio WhatsApp"**.
3. El sistema construye la URL `https://wa.me/{telefono}?text=...` con el resumen del turno y el link `/turno/{token}` y abre WhatsApp Web/App en una pestaña nueva.
4. Recepción envía el mensaje con 1 clic.
5. El paciente abre `/turno/{token}` desde su celular:
   - Si toca **Confirmar asistencia**: `POST /api/v1/public/turnos/{token}/confirmar` → estado pasa a `confirmado`, actualiza evento en Google Calendar y registra auditoría.
   - Si toca **Cancelar turno**: el backend verifica `(turno.inicio - now) >= anticipacion_minima_cancelacion_hs`:
     - Si cumple: pasa a `cancelado`, libera profesional y sillón, elimina evento en Google Calendar y registra auditoría.
     - Si no cumple: devuelve `422 Unprocessable Entity` indicando el mínimo de horas y mostrando el teléfono del consultorio para gestionar por recepción.

**Casos de error**:
- **Paciente sin opt-in (`opt_in_whatsapp = false`)**: el botón muestra advertencia de que no autorizó recordatorios por WhatsApp (`RN-WA-01`).
- **Token inválido o turno ya pasado**: el endpoint público responde `404` o `410` con mensaje claro sin exponer datos internos.

---

## Flujo 3: Carga y reprogramación de turno interno (por profesional y sillón/box)

**Disparador**: paciente llama o escribe por WhatsApp pidiendo turno o cambio de horario.
**Actor**: Recepción.

**Pasos**:
1. Recepción selecciona paciente existente (o lo crea rápido), prestación, profesional y sillón/box en la grilla horaria.
2. El formulario calcula automáticamente `fin = inicio + prestacion.duracion_minutos` (permitiendo ajustar duración si corresponde).
3. Al guardar (`POST /turnos` o `PATCH /turnos/{id}/reprogramar`), el backend verifica disponibilidad de **profesional** y **sillón/box** simultáneamente dentro de una transacción.
4. Si opcionalmente el paciente entregó una seña en efectivo/transferencia en ese acto, recepción registra el pago manual (`tipo = 'sena'`) vinculado al `turno_id`.
5. Se persiste auditoría y se crea/actualiza el evento en Google Calendar del profesional.

**Casos de error**:
- **Solapamiento de profesional o de sillón**: la API devuelve `409 Conflict` especificando claramente cuál recurso está ocupado (ej. *"El Sillón 1 ya tiene un turno asignado de 10:00 a 10:45"*).

---

## Flujo 4: Atención clínica, odontograma y presupuesto versionado

**Disparador**: el paciente llega al consultorio y pasa a atención.
**Actor**: Recepción (recepción en sala) → Odontólogo/a (atención clínica).

**Pasos**:
1. Recepción (o el profesional) cambia el estado del turno a `en_atencion`.
2. El Odontólogo/a abre la ficha del paciente en su dispositivo. El backend valida rol `odontologo` (`RN-AU-02`).
3. El Odontólogo/a registra la nueva evolución en `historias_clinicas` y, si corresponde, actualiza piezas/caras en `odontogramas` (creando `version = N + 1`).
4. Si define un nuevo plan o modifica un tratamiento acordado, crea o actualiza un `presupuestos` (si ya estaba `emitido`/`aceptado`, genera nueva versión y marca la anterior como `reemplazado`).
5. Al finalizar la consulta, el Odontólogo/a marca el turno como `atendido`.
6. Cada acción clínica y presupuestaria queda auditada con `usuario_id` y timestamp.

**Casos de error**:
- **Usuario `dueno` o `recepcion` intenta abrir endpoints clínicos**: backend responde `403 Forbidden` y registra el intento denegado si aplica.

---

## Flujo 5: Registro manual de pagos y exportación para ARCA / Obras Sociales

**Disparador**: el paciente abona seña/cuota o administración realiza cierre semanal/mensual.
**Actor**: Administración / facturación (o Recepción para señas).

**Pasos**:
1. En la vista de caja/presupuesto del paciente, administración registra el pago manual (`POST /pagos`) con medio de pago, monto en ARS y comprobante.
2. El sistema recalcula el saldo pendiente del presupuesto/turno y registra auditoría.
3. Si hubo un error de carga, administración anula el pago (`PATCH /pagos/{id}/anular`) ingresando motivo obligatorio (el registro original permanece visible como `anulado`).
4. A fin de período, administración ingresa a **Exportaciones**, filtra por rango de fechas, profesional u obra social, y descarga **CSV** (para planillas y carga manual en ARCA/obras sociales) o **PDF** resumen.

**Casos de error**:
- **Intento de edición de monto o borrado físico de un pago**: bloqueado por API (`405/403`); solo se admite anulación con motivo por `administracion` o `dueno`.
