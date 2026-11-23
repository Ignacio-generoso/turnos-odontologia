## Purpose
Permitir la creación segura de turnos odontológicos en la agenda del consultorio garantizando la duración adecuada por prestación y previniendo solapamientos por profesional y por sillón/box.

## ADDED Requirements

### Requirement: Creación de turno con duración calculada y asignación obligatoria de recursos
El sistema MUST crear un turno en estado inicial `reservado` asignando `profesional_id` activo (con rol `odontologo`), `sillon_id` activo y `prestacion_id` activa pertenecientes al mismo `consultorio_id`, calculando `fin = inicio + duracion_minutos` y registrando el alta en `auditoria_eventos`.

#### Scenario: Creación exitosa con cálculo automático de fin según prestación
- **GIVEN** un consultorio con un profesional odontólogo activo, un sillón activo (`Sillón 1`), una prestación activa (`Limpieza`, `40` minutos) y disponibilidad horaria cargada
- **WHEN** recepción solicita crear un turno a las `10:00-03:00`
- **THEN** el sistema crea el turno de `10:00-03:00` a `10:40-03:00` en estado `reservado` y registra la entrada en `auditoria_eventos`

### Requirement: Prevención de solapamientos por profesional y por sillón/box
El sistema MUST rechazar cualquier intento de crear un turno cuyo rango horario `[inicio, fin]` cerrado se superponga con otro turno existente del mismo profesional o del mismo sillón/box, o con un bloqueo de agenda vigente.

#### Scenario: Rechazo por solapamiento del mismo profesional en distinto sillón
- **GIVEN** un turno existente para la Dra. García de `10:00-03:00` a `10:40-03:00` en `Sillón 1`
- **WHEN** se intenta agendar otro turno para la Dra. García de `10:15-03:00` a `10:45-03:00` en `Sillón 2`
- **THEN** el sistema rechaza la operación con error de conflicto (`409`) indicando solapamiento de profesional

#### Scenario: Rechazo por solapamiento del mismo sillón entre distintos profesionales
- **GIVEN** un turno existente para la Dra. García de `10:00-03:00` a `10:40-03:00` en `Sillón 1`
- **WHEN** se intenta agendar un turno para el Dr. Pérez de `10:20-03:00` a `10:50-03:00` en `Sillón 1`
- **THEN** el sistema rechaza la operación con error de conflicto (`409`) indicando solapamiento de sillón/box

#### Scenario: Turno contiguo en el límite exacto
- **GIVEN** un turno existente de `10:00-03:00` a `10:40-03:00`
- **WHEN** se intenta crear un turno de `10:40-03:00` a `11:10-03:00`
- **THEN** el sistema evalúa el intervalo `[inicio, fin]` y rechaza por coincidencia en el minuto `10:40`

### Requirement: Cobro automático de seña con Mercado Pago al crear el turno
Cuando una prestación tenga `requiere_sena = true`, el sistema MUST generar una preferencia de cobro en Mercado Pago al crear el turno.

#### Scenario: Generación de link de pago Mercado Pago en creación de turno
- **GIVEN** una prestación con `requiere_sena = true`
- **WHEN** se crea el turno
- **THEN** el sistema invoca la API de Mercado Pago y adjunta `checkout_url`
