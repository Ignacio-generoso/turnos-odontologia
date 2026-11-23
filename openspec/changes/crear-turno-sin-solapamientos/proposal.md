## Why

En el informe de Discovery (`docs/discovery/market-research.md`, sección D.3) identificamos como primera funcionalidad **Must-Have (v1)** del MVP la *"Agenda multi-profesional con vista día/semana y prevención de solapamientos"*. Elegimos del roadmap `CHANGES.md` el núcleo de **`C-06` (`turnos-agenda`: Crear un turno evitando solapamientos por profesional y por sillón/box)** porque pertenece al MVP prioritario, posee reglas de negocio críticas y 100 % verificables (`RN-AG-01` a `RN-AG-05`, `RN-AU-01`, `RN-AU-05`), y es lo suficientemente acotado para completarse como una única funcionalidad de principio a fin dentro del ciclo OPSX.

## What Changes

- Implementar el modelo de dominio y servicio transaccional `AgendaTurnosService.crear_turno` para crear turnos odontológicos evitando solapamientos por profesional y por sillón/box.
- Calcular automáticamente la hora de fin (`fin = inicio + duracion_minutos`) a partir de la prestación (`RN-AG-01`), admitiendo ajuste manual válido (`> 0`) en carga interna.
- Garantizar la semántica de intervalo semiabierto `[inicio, fin)` excluyendo turnos en estado `cancelado`, de modo que turnos contiguos exactos (ej. `10:00–10:40` y `10:40–11:10`) sean válidos y los turnos cancelados liberen disponibilidad.
- Validar disponibilidad horaria del profesional (`RN-AG-05`, con sobrecarga explícita permitida solo a `recepcion`/`dueno`), bloqueos de agenda (`RN-AG-03`/`RN-AG-04`), estado activo de los recursos (`RN-AG-02`), timestamps con zona horaria (`TIMESTAMPTZ`) y aislamiento lógico por `consultorio_id` (`RN-AU-01`).
- Registrar cada creación en `auditoria_eventos` (`RN-AU-05`) y emitir evento de dominio `TurnoCreado`.
- Definir el DDL PostgreSQL 15+ con constraints `EXCLUDE USING gist` (`btree_gist`) y exponer `POST /api/v1/turnos` en FastAPI con tipado estricto Pydantic v2.

## Capabilities

### New Capabilities
- `turnos-agenda`: Creación de turnos odontológicos sin solapamientos por profesional y por sillón/box mediante intervalos semiabiertos `[inicio, fin)`, validación de bloqueos, disponibilidad, aislamiento multi-consultorio y auditoría append-only.

### Modified Capabilities
<!-- Sin capacidades previas modificadas -->

## Impact

- `src/domain/models.py`: entidades, enums, excepciones de negocio y schemas tipados.
- `src/domain/services.py`: servicio `AgendaTurnosService.crear_turno` con reglas `RN-AG-01..05`, `RN-AU-01`, `RN-AU-05`.
- `src/infrastructure/sql/005_turnos_agenda_btree_gist.sql`: DDL PostgreSQL con `btree_gist` y `EXCLUDE USING gist`.
- `src/api/app.py`: API FastAPI (`GET /api/v1/health`, `POST /api/v1/turnos`).
- `tests/test_crear_turno_sin_solapamientos.py`: pruebas automatizadas por cada escenario de la especificación.

## Protocolo de Inspección (Revisión y Ajuste)

- **Decisión tomada tras revisar el borrador inicial de Propose**: **Ajustar**.
- **Qué estaba mal en el borrador inicial**:
  1. **Exceso de alcance fuera de v1**: el borrador inicial incluía generar un link de cobro automático con Mercado Pago al crear el turno. Al contrastarlo con `knowledge-base/09_decisiones_y_supuestos.md` (`DD-03`) y `10_preguntas_abiertas.md` (`IN-01`), Mercado Pago quedó diferido a **v1.1** y los pagos pertenecen al change `C-12` (`pagos-manuales`), no a `C-06`.
  2. **Error lógico en el intervalo de solapamiento**: el borrador inicial especificaba el intervalo cerrado `[inicio, fin]`, lo que rechazaba erróneamente un turno contiguo que comienza en el minuto exacto en que finaliza el turno anterior (`10:40` tras `10:00–10:40`), contradiciendo `tstzrange(inicio, fin, '[)')` definido en `04_modelo_de_datos.md`.
  3. **Falta de cobertura de escenarios críticos**: faltaban los escenarios verificables de colisión con `bloqueos_agenda`, liberación por estado `cancelado`, sobrecarga autorizada y aislamiento por `consultorio_id` (`RN-AU-01`).
- **Qué se corrigió**: se eliminó toda referencia a Mercado Pago del alcance, se fijó el intervalo semiabierto `[inicio, fin)` y la exclusión de `estado = 'cancelado'`, y se amplió `specs/turnos-agenda/spec.md` a **7 escenarios verificables** alineados con la Knowledge Base y las reglas duras de `AGENTS.md`.
