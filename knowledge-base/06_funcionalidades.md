# Funcionalidades

Organizadas por **épica** y por **historia de usuario** (`US-NNN`) para el alcance v1 (MVP).

---

## Épica 1: Configuración del Consultorio y Catálogo

### US-001 — Configurar consultorio, sillones y prestaciones
**Como** Dueño/a del consultorio
**Quiero** dar de alta los sillones/boxes, las prestaciones con su duración en minutos y valor de referencia, y los horarios de cada profesional
**Para** que la agenda y la reserva online reflejen la capacidad real del consultorio.

**Criterios de aceptación**:
- [ ] CA-1: Permite crear, editar y desactivar sillones/boxes (`Sillón 1`, `Sillón 2`, etc.).
- [ ] CA-2: Cada prestación exige `duracion_minutos > 0` y permite marcar si es visible para reserva online pública.
- [ ] CA-3: Permite configurar la anticipación mínima de cancelación en horas (default 24 hs).
- [ ] CA-4: Permite definir franjas semanales de disponibilidad y bloqueos puntuales por profesional o sillón.

**Reglas relacionadas**: RN-AU-01, RN-AG-01, RN-AG-02, RN-AG-05, RN-AG-06

### US-002 — Gestionar usuarios y roles del equipo
**Como** Dueño/a del consultorio
**Quiero** crear usuarios para odontólogos, recepción y administración asignando sus roles explícitos
**Para** controlar qué módulos y datos sensibles puede ver u operar cada integrante.

**Criterios de aceptación**:
- [ ] CA-1: Soporta roles `dueno`, `odontologo`, `recepcion`, `administracion` (y combinación explícita `dueno` + `odontologo` si atiende).
- [ ] CA-2: Un usuario `dueno` sin rol `odontologo` no puede abrir historia clínica ni odontograma.
- [ ] CA-3: Se puede desactivar un usuario sin borrar su historial ni sus turnos/evoluciones pasadas.

**Reglas relacionadas**: RN-AU-01, RN-AU-02, RN-AU-03

---

## Épica 2: Agenda Multi-profesional y por Sillón/Box

### US-003 — Visualizar agenda diaria y semanal por profesional y por sillón
**Como** Recepción / Odontólogo/a
**Quiero** ver la agenda en vista día y semana filtrable por profesional y por sillón/box
**Para** detectar huecos disponibles y organizar la jornada sin errores.

**Criterios de aceptación**:
- [ ] CA-1: La vista muestra franjas horarias con color por estado del turno (`reservado`, `confirmado`, `en_atencion`, `atendido`, `ausente`, `cancelado`).
- [ ] CA-2: Permite alternar agrupación por columnas de profesionales o por columnas de sillones/boxes.
- [ ] CA-3: El odontólogo ve su agenda propia rápidamente desde escritorio y celular (PWA responsive).

**Reglas relacionadas**: RN-AU-01, RN-AG-02, RN-AG-07

### US-004 — Crear y reprogramar turnos evitando solapamientos
**Como** Recepción
**Quiero** agendar o reprogramar un turno eligiendo paciente, prestación, profesional y sillón/box
**Para** asegurar la duración correcta y evitar dobles reservas.

**Criterios de aceptación**:
- [ ] CA-1: Al seleccionar la prestación, la hora de fin se calcula automáticamente según `duracion_minutos` (editable en agenda interna).
- [ ] CA-2: El sistema impide guardar si el profesional ya tiene otro turno o bloqueo superpuesto.
- [ ] CA-3: El sistema impide guardar si el sillón/box ya está ocupado por otro turno o bloqueo en ese horario.
- [ ] CA-4: Al confirmar la creación o reprogramación, se registra en auditoría y se encola la actualización en Google Calendar.

**Reglas relacionadas**: RN-AG-01, RN-AG-02, RN-AG-03, RN-AG-04, RN-AG-08, RN-GC-01, RN-AU-05

### US-005 — Gestionar estados del turno (confirmar, atender, ausente, cancelar)
**Como** Recepción / Odontólogo/a
**Quiero** actualizar el estado de cada turno a medida que avanza el día
**Para** medir ocupación, registrar ausentismo y liberar sillones ante cancelaciones.

**Criterios de aceptación**:
- [ ] CA-1: Solo permite transiciones válidas según la máquina de estados.
- [ ] CA-2: Al cancelar un turno se solicita motivo opcional y se libera el horario del profesional y del sillón/box.
- [ ] CA-3: Cada cambio de estado queda registrado en `auditoria_eventos`.

**Reglas relacionadas**: RN-AG-07, RN-GC-01, RN-AU-05

---

## Épica 3: Reserva Online del Paciente y Recordatorios WhatsApp

### US-006 — Reservar turno online mediante link público
**Como** Paciente
**Quiero** ingresar al link público del consultorio, elegir prestación, profesional y horario disponible y confirmar mis datos
**Para** sacar turno sin esperar respuesta manual por WhatsApp.

**Criterios de aceptación**:
- [ ] CA-1: Muestra únicamente prestaciones con `visible_publico = true` y slots reales libres considerando disponibilidad, profesional y al menos un sillón libre.
- [ ] CA-2: Solicita nombre, apellido, DNI, teléfono WhatsApp y checkbox de consentimiento (`opt_in_whatsapp`) para recibir recordatorios.
- [ ] CA-3: Genera un turno en estado `reservado` (`origen = 'publico'`), asigna sillón libre automáticamente y devuelve el enlace personal `/turno/{token}`.
- [ ] CA-4: Previene reservas concurrentes sobre el mismo slot mediante validación transaccional y constraint de BD.

**Reglas relacionadas**: RN-AG-01, RN-AG-02, RN-AG-03, RN-AG-04, RN-AG-05, RN-WA-01, RN-AU-04

### US-007 — Confirmar o cancelar turno online desde enlace personal
**Como** Paciente
**Quiero** abrir mi link `/turno/{token}` para confirmar asistencia o cancelar el turno
**Para** avisar al consultorio a tiempo sin llamar por teléfono.

**Criterios de aceptación**:
- [ ] CA-1: Muestra fecha, hora, prestación, profesional, dirección del consultorio y estado actual del turno.
- [ ] CA-2: Permite confirmar asistencia pasando el turno a `confirmado`.
- [ ] CA-3: Permite cancelar únicamente si cumple `anticipacion_minima_cancelacion_hs`; caso contrario muestra aviso y teléfono de recepción.

**Reglas relacionadas**: RN-AU-04, RN-AG-06, RN-AG-07, RN-GC-01

### US-008 — Enviar recordatorio asistido por WhatsApp en 1 clic
**Como** Recepción
**Quiero** abrir WhatsApp desde cada turno con un mensaje prearmado que incluya el link de confirmación/cancelación
**Para** reducir el ausentismo sin pagar costo por mensaje de API en v1.

**Criterios de aceptación**:
- [ ] CA-1: Solo habilita la acción directa si el paciente tiene `opt_in_whatsapp = true` (si es `false`, muestra advertencia explícita).
- [ ] CA-2: El enlace `wa.me` pre-carga nombre del paciente, fecha/hora, profesional y URL `/turno/{token}`.

**Reglas relacionadas**: RN-WA-01, RN-WA-02

---

## Épica 4: Sincronización con Google Calendar

### US-009 — Conectar cuenta de Google Calendar del profesional y sincronizar turnos
**Como** Odontólogo/a
**Quiero** vincular mi cuenta de Google Calendar una sola vez y ver mis turnos reflejados automáticamente
**Para** consultar mi agenda laboral desde el celular sin duplicar carga manual.

**Criterios de aceptación**:
- [ ] CA-1: Flujo OAuth 2.0 por profesional desde su perfil interno.
- [ ] CA-2: Alta, reprogramación y cancelación de turno crean, actualizan o eliminan el evento en Google Calendar (`Sistema → Google`).
- [ ] CA-3: El evento externo no incluye datos clínicos sensibles y muestra estado de sincronización en el sistema (con botón de reintento si hubo error).

**Reglas relacionadas**: RN-GC-01, RN-GC-02, RN-GC-03

---

## Épica 5: Ficha del Paciente, Historia Clínica y Odontograma

### US-010 — Gestionar ficha administrativa y cobertura de obra social del paciente
**Como** Recepción / Administración
**Quiero** buscar, crear y actualizar datos de contacto y obra social del paciente
**Para** mantener ordenada su identificación, opt-in y cobertura antes de atenderlo o liquidar.

**Criterios de aceptación**:
- [ ] CA-1: Búsqueda rápida por apellido, nombre, DNI o teléfono.
- [ ] CA-2: Permite cargar obra social, plan y número de afiliado (informativo en v1).
- [ ] CA-3: Muestra historial básico de turnos y saldo pendiente del paciente sin exponer historia clínica a roles no autorizados.

**Reglas relacionadas**: RN-AU-01, RN-AU-02, RN-WA-01, RN-OS-01

### US-011 — Registrar historia clínica y odontograma simple (solo Odontólogo/a)
**Como** Odontólogo/a
**Quiero** registrar evoluciones clínicas y actualizar el odontograma por pieza y cara dental
**Para** contar con una historia clínica ordenada, versionada y confidencial.

**Criterios de aceptación**:
- [ ] CA-1: Acceso estrictamente bloqueado (`403`) para usuarios sin rol `odontologo`.
- [ ] CA-2: Permite cargar motivo de consulta, antecedentes, diagnóstico y evolución asociada opcionalmente a un turno.
- [ ] CA-3: El odontograma interactivo (piezas permanentes y temporarias) guarda una nueva versión inmutable en cada actualización confirmada.

**Reglas relacionadas**: RN-AU-02, RN-AU-03, RN-CL-01, RN-AU-05

---

## Épica 6: Presupuestos, Pagos Manuales y Exportación

### US-012 — Crear planes de tratamiento y presupuestos versionados
**Como** Odontólogo/a
**Quiero** armar un plan de tratamiento y emitir un presupuesto con prestaciones, piezas y montos en ARS
**Para** registrar qué aprobó el paciente y conservar trazabilidad si cambia el plan.

**Criterios de aceptación**:
- [ ] CA-1: Permite agregar ítems desde el catálogo de prestaciones con precio editable y pieza dental opcional.
- [ ] CA-2: Al editar un presupuesto ya `emitido` o `aceptado`, genera versión `N+1` dejando la anterior como `reemplazado`.
- [ ] CA-3: Registra fecha de aceptación y calcula automáticamente saldo pendiente frente a pagos registrados.

**Reglas relacionadas**: RN-AU-02, RN-CL-01, RN-AU-05

### US-013 — Registrar señas y pagos manuales (y anular con motivo)
**Como** Administración / Recepción
**Quiero** registrar señas y pagos recibidos por transferencia, efectivo o tarjeta asociados a un turno o presupuesto
**Para** llevar cuenta corriente clara del paciente en el sistema.

**Criterios de aceptación**:
- [ ] CA-1: Permite cargar tipo (`sena`, `pago_parcial`, `pago_total`), medio de pago, monto en ARS y referencia de comprobante.
- [ ] CA-2: No permite borrar ni editar montos guardados; solo `administracion` o `dueno` puede anular con motivo obligatorio.
- [ ] CA-3: Todo registro y anulación genera entrada en auditoría.

**Reglas relacionadas**: RN-PG-01, RN-PG-02, RN-AU-05

### US-014 — Exportar datos para ARCA/Obras Sociales y consultar reportes operativos
**Como** Administración / Dueño/a
**Quiero** exportar en CSV/PDF los turnos atendidos, prestaciones, coberturas y pagos filtrados por rango de fechas, y ver ocupación y ausentismo
**Para** facturar fuera del sistema y tomar decisiones sobre la agenda del consultorio.

**Criterios de aceptación**:
- [ ] CA-1: Exportación CSV y resumen PDF de pagos/señas y prestaciones por fecha, profesional y obra social (sin datos de evolución clínica).
- [ ] CA-2: Tablero operativo básico para el Dueño/a: tasa de ocupación por profesional/sillón, cantidad de turnos atendidos, cancelados y ausentes, y total cobrado en el período.
- [ ] CA-3: Visor de `auditoria_eventos` filtrable por entidad, usuario y fecha para Dueño/a.

**Reglas relacionadas**: RN-AU-01, RN-AU-02, RN-OS-01, RN-AU-05
