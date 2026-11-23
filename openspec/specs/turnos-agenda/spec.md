# turnos-agenda Specification

## Purpose
Permitir la creación segura de turnos odontológicos en la agenda del consultorio garantizando la duración adecuada por prestación, el aislamiento por consultorio y la prevención estricta de solapamientos por profesional y por sillón/box mediante intervalos semiabiertos `[inicio, fin)`.

## Requirements

### Requirement: Creación de turno con duración calculada y asignación obligatoria de recursos
El sistema MUST crear un turno en estado inicial `reservado` asignando `profesional_id` activo (con rol `odontologo`), `sillon_id` activo, `prestacion_id` activa y `paciente_id` activo pertenecientes al mismo `consultorio_id`, exigiendo `inicio` con zona horaria (`TIMESTAMPTZ`), calculando `fin = inicio + duracion_minutos` (tomando por defecto `prestacion.duracion_minutos` o el ajuste interno `> 0`), generando `token_publico_hash` y registrando el alta en `auditoria_eventos`.

#### Scenario: Creación exitosa con cálculo automático de fin según prestación
- **GIVEN** un consultorio activo con la Dra. Sofía García (rol `odontologo` activo) disponible de `09:00-03:00` a `13:00-03:00`, el recurso `Sillón 1` activo, la prestación `Limpieza` (`40` minutos) y una paciente ficticia activa del mismo consultorio
- **WHEN** un usuario con rol `recepcion` solicita crear un turno para esa paciente el lunes a las `10:00-03:00` sin sobreescribir la duración
- **THEN** el sistema crea el turno con `estado = 'reservado'`, `duracion_minutos = 40`, `fin = 10:40-03:00`, `token_publico_hash` no vacío, emite `TurnoCreado` y registra una entrada `accion = 'crear'` en `auditoria_eventos`

### Requirement: Prevención de solapamientos por profesional y por sillón/box en intervalo semiabierto
El sistema MUST rechazar con conflicto (`409`) cualquier intento de crear un turno activo cuyo intervalo semiabierto `[inicio, fin)` se superponga (`inicio_a < fin_b AND inicio_b < fin_a`) con otro turno activo (`estado != 'cancelado'`) del mismo profesional o del mismo sillón/box dentro del consultorio, permitiendo turnos contiguos exactos (`nuevo.inicio == existente.fin`) y reutilización de horarios cuyo turno previo esté `cancelado`.

#### Scenario: Rechazo por solapamiento del mismo profesional aunque cambie de sillón
- **GIVEN** un turno activo (`reservado`) para la Dra. Sofía García de `10:00-03:00` a `10:40-03:00` en `Sillón 1`
- **WHEN** se solicita crear otro turno para la Dra. Sofía García de `10:15-03:00` a `10:45-03:00` en `Sillón 2`
- **THEN** el sistema rechaza la creación con conflicto de profesional (`409 Conflict`) y no inserta turno ni evento de auditoría

#### Scenario: Rechazo por solapamiento del mismo sillón entre profesionales distintos
- **GIVEN** un turno activo (`confirmado`) para la Dra. Sofía García de `10:00-03:00` a `10:40-03:00` en `Sillón 1`
- **WHEN** se solicita crear un turno para el Dr. Martín Pérez de `10:20-03:00` a `10:50-03:00` en `Sillón 1`
- **THEN** el sistema rechaza la creación con conflicto de sillón/box (`409 Conflict`) indicando el recurso ocupado

#### Scenario: Caso de borde con turno contiguo exacto sin solapamiento
- **GIVEN** un turno activo para la Dra. Sofía García de `10:00-03:00` a `10:40-03:00` en `Sillón 1`
- **WHEN** se solicita crear un turno para la misma Dra. Sofía García y el mismo `Sillón 1` de `10:40-03:00` a `11:10-03:00` (prestación `Consulta`, `30` minutos)
- **THEN** el sistema permite la creación (`201 Created`) porque los intervalos `[10:00, 10:40)` y `[10:40, 11:10)` no se superponen

#### Scenario: Caso de borde con horario liberado por turno cancelado
- **GIVEN** un turno previo para la Dra. Sofía García en `Sillón 1` de `10:00-03:00` a `10:40-03:00` cuyo estado actual es `cancelado`
- **WHEN** se solicita crear un nuevo turno en el mismo horario `10:00-03:00` a `10:40-03:00` para la misma profesional y sillón
- **THEN** el sistema permite la creación (`201 Created`) sin falsos conflictos

### Requirement: Respeto de bloqueos de agenda y disponibilidad horaria del profesional
El sistema MUST rechazar turnos que invadan un `bloqueo_agenda` vigente del profesional o del sillón/box (`409`), y MUST validar que el turno encuadre dentro de una franja activa de `disponibilidades_profesional`, salvo cuando el operador (`recepcion` o `dueno`) indique `sobrecarga = true` sin violar solapamientos ni bloqueos.

#### Scenario: Rechazo por bloqueo de agenda y fuera de disponibilidad, con sobrecarga autorizada
- **GIVEN** un `bloqueo_agenda` sobre `Sillón 1` de `12:00-03:00` a `13:00-03:00` y una franja de disponibilidad de `09:00-03:00` a `13:00-03:00`
- **WHEN** se solicita un turno de `12:15-03:00` a `12:45-03:00` en `Sillón 1`, o un turno a las `13:30-03:00` sin `sobrecarga = true`
- **THEN** el sistema rechaza ambos intentos (`409` por bloqueo y `422` por fuera de disponibilidad), y únicamente permite el turno de `13:30-03:00` cuando `recepcion` o `dueno` envía `sobrecarga = true` sin solapamientos

### Requirement: Aislamiento multi-consultorio, control de rol y obligatoriedad de zona horaria
El sistema MUST impedir el cruce de entidades entre distintos `consultorio_id` (`RN-AU-01`), restringir la creación interna a roles autorizados (`recepcion`, `odontologo`, `dueno`) y rechazar fechas `inicio` sin zona horaria (`TIMESTAMPTZ`).

#### Scenario: Rechazo por cruce de consultorio o timestamp sin zona horaria
- **GIVEN** un usuario operador perteneciente al `consultorio_A` y un `Sillón X` perteneciente al `consultorio_B`
- **WHEN** intenta crear un turno combinando recursos del `consultorio_A` con el sillón del `consultorio_B`, o envía un `inicio` sin `tzinfo`
- **THEN** el sistema rechaza la operación (`403 Forbidden` por aislamiento de consultorio y `422 Unprocessable Entity` por fecha sin zona horaria)
