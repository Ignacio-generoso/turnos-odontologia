## 1. Dominio y Persistencia SQL

- [ ] 1.1 Definir modelos Pydantic/dominio en `src/domain/models.py` y excepciones de negocio.
- [ ] 1.2 Crear DDL PostgreSQL `src/infrastructure/sql/005_turnos_agenda_btree_gist.sql` con `EXCLUDE USING gist`.

## 2. Servicio de Agenda y API FastAPI

- [ ] 2.1 Implementar `AgendaTurnosService.crear_turno` en `src/domain/services.py` con validaciones de solapamiento, bloqueos, disponibilidad, aislamiento `consultorio_id` y auditoría.
- [ ] 2.2 Implementar integración de cobro con Mercado Pago al crear el turno.
- [ ] 2.3 Exponer `POST /api/v1/turnos` y `GET /api/v1/health` en `src/api/app.py`.

## 3. Pruebas Automatizadas (Verify)

- [ ] 3.1 Implementar `tests/test_crear_turno_sin_solapamientos.py` cubriendo los escenarios del spec aprobado.
- [ ] 3.2 Ejecutar `python -m pytest -v --cov=src` y registrar evidencia en `docs/opsx/verify-report.md`.
