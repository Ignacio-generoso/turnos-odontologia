## 1. Dominio y Persistencia SQL

- [ ] 1.1 Definir entidades, enums (`EstadoTurno`, `OrigenTurno`, `RolUsuario`), excepciones de negocio y schemas Pydantic v2 en `src/domain/models.py` (validando `TIMESTAMPTZ` y datos 100 % ficticios en ejemplos).
- [ ] 1.2 Crear DDL PostgreSQL 15+ en `src/infrastructure/sql/005_turnos_agenda_btree_gist.sql` con `btree_gist`, `tstzrange(inicio, fin, '[)')` y `EXCLUDE USING gist` para `profesional_id` y `sillon_id` con `WHERE (estado <> 'cancelado')`.

## 2. Servicio de Agenda y API FastAPI

- [ ] 2.1 Implementar `AgendaTurnosService.crear_turno` en `src/domain/services.py` con aislamiento por `consultorio_id` (`RN-AU-01`), cálculo de duración (`RN-AG-01`), validación de recursos activos (`RN-AG-02`), intervalo semiabierto `[inicio, fin)` excluyendo `cancelado` (`RN-AG-03`, `RN-AG-04`), disponibilidad y `sobrecarga` (`RN-AG-05`), `token_publico_hash`, evento `TurnoCreado` y registro en `auditoria_eventos` (`RN-AU-05`).
- [ ] 2.2 Exponer `GET /api/v1/health` y `POST /api/v1/turnos` en `src/api/app.py` usando `Annotated[..., Depends(...)]`, return types explícitos y mapeo de errores (`403`, `409`, `422`).

## 3. Pruebas Automatizadas (Verify)

- [ ] 3.1 Implementar `tests/test_crear_turno_sin_solapamientos.py` cubriendo los 7 escenarios del spec aprobado (camino feliz, solapamiento profesional, solapamiento sillón, turno contiguo exacto, turno previo cancelado, bloqueos/disponibilidad/sobrecarga, y aislamiento multi-consultorio + timezone).
- [ ] 3.2 Ejecutar `python -m pytest -v --cov=src` y registrar el resultado completo en `docs/opsx/verify-report.md`.
