## Context

Diseño técnico ajustado tras aplicar el protocolo de inspección (`Ajustar`) en Propose para el change `crear-turno-sin-solapamientos` (`C-06`). El alcance se mantiene estricto sobre la creación de turnos internos sin pasarelas externas de pago ni integraciones diferidas.

## Goals / Non-Goals

**Goals:**
- Garantizar cero solapamientos por `profesional_id` y por `sillon_id` dentro de cada `consultorio_id` usando intervalos semiabiertos `[inicio, fin)` y excluyendo turnos en estado `cancelado`.
- Proveer el script DDL PostgreSQL 15+ con `btree_gist` y dos constraints `EXCLUDE USING gist` (`RN-AG-03` y `RN-AG-04`).
- Implementar el servicio de dominio `AgendaTurnosService` y el endpoint FastAPI `POST /api/v1/turnos` con tipado estricto Pydantic v2, auditoría append-only (`RN-AU-05`) y cobertura completa de tests por escenario (`pytest`).

**Non-Goals:**
- Cobros online con Mercado Pago (diferido a v1.1 por `DD-03` / `IN-01`; pagos manuales corresponden a `C-12`).
- Reprogramación, transición posterior de estados, reserva pública (`C-07`), links `wa.me` (`C-08`) y sincronización Google Calendar (`C-09`).

## Decisions

1. **Intervalo semiabierto `[inicio, fin)` tanto en dominio como en PostgreSQL**:
   - En Python: dos intervalos se superponen si `a_inicio < b_fin and b_inicio < a_fin`.
   - En PostgreSQL: `tstzrange(inicio, fin, '[)') WITH &&` junto con `WHERE (estado <> 'cancelado')`.
   - **Justificación**: permite turnos consecutivos exactos (ej. `10:00–10:40` y `10:40–11:10`) sin falsos rechazos y libera recursos al instante cuando un turno se cancela.
2. **Doble defensa (Reglas de Dominio + DDL PostgreSQL `btree_gist`)**:
   - El servicio Python valida las reglas de negocio con excepciones semánticas claras (`SolapamientoProfesionalError`, `SolapamientoSillonError`, `BloqueoAgendaConflictError`), lo que permite ejecutar tests deterministas rápidos en memoria sin requerir servidor PostgreSQL levantado para clonar y correr `pytest`, mientras que `005_turnos_agenda_btree_gist.sql` documenta y garantiza la atomicidad ante concurrencia en PostgreSQL 15+.
3. **Timestamps estrictos con zona horaria (`TIMESTAMPTZ`)**:
   - Todo `datetime` de entrada sin `tzinfo` es rechazado en validación (`422`).
4. **Cero datos reales de pacientes**:
   - Todos los nombres, DNI, matrículas y teléfonos en fixtures y tests son ficticios (cumpliendo la regla propia del dominio en `AGENTS.md`).

## Risks / Trade-offs

- **Sin dependencia obligatoria de PostgreSQL en ejecución para correr la suite local**: los tests de la suite verifican la lógica exacta de `[inicio, fin)` y los casos de concurrencia lógica vía repositorio in-memory thread-safe + endpoint FastAPI; la ejecución física contra un motor PostgreSQL se apoya en el script SQL `005_turnos_agenda_btree_gist.sql` listo para migración Alembic.
