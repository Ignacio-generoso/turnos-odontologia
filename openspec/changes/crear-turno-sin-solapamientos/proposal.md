## Why

En el informe de Discovery (`docs/discovery/market-research.md`, sección D.3) identificamos como primera funcionalidad **Must-Have (v1)** del MVP la *"Agenda multi-profesional con vista día/semana y prevención de solapamientos"*. Elegimos del roadmap `CHANGES.md` el núcleo de **`C-06` (`turnos-agenda`: Crear un turno evitando solapamientos por profesional y por sillón/box)** porque pertenece al MVP prioritario, posee reglas de negocio verificables (`RN-AG-01` a `RN-AG-05`, `RN-AU-01`, `RN-AU-05`) y es suficientemente acotado para completarse en un ciclo OPSX completo.

## What Changes

- Implementar el dominio y servicio transaccional para crear turnos odontológicos evitando solapamientos por profesional y por sillón/box.
- Calcular automáticamente la hora de fin (`fin = inicio + duracion_minutos`) a partir de la prestación o del ajuste interno explícito.
- Validar disponibilidad horaria del profesional, bloqueos de agenda, aislamiento por `consultorio_id` y estado activo de los recursos.
- **Incluir cobro automático de seña online con Mercado Pago al momento de crear el turno cuando la prestación tenga `requiere_sena = true`.** *(Nota: exceso de alcance en borrador inicial pendiente de revisión).*
- Definir el DDL PostgreSQL con constraints `EXCLUDE USING gist` (`btree_gist`) y exponer `POST /api/v1/turnos` en FastAPI con registro en `auditoria_eventos`.

## Capabilities

### New Capabilities
- `turnos-agenda`: Creación de turnos odontológicos sin solapamientos por profesional y por sillón/box, cálculo automático de duración, control de bloqueos/disponibilidad, auditoría append-only y cobro de seña.

### Modified Capabilities
<!-- Sin capacidades previas modificadas -->

## Impact

- `src/domain/models.py`: entidades, enums y excepciones del dominio de agenda.
- `src/domain/services.py`: servicio `AgendaTurnosService.crear_turno`.
- `src/infrastructure/sql/005_turnos_agenda_btree_gist.sql`: DDL PostgreSQL con `EXCLUDE USING gist`.
- `src/api/app.py`: endpoint FastAPI `POST /api/v1/turnos`.
- `tests/test_crear_turno_sin_solapamientos.py`: suite de tests por escenario.
