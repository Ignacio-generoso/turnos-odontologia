## Context

Borrador inicial de diseño técnico para el change `crear-turno-sin-solapamientos` (`C-06`).

## Goals / Non-Goals

**Goals:**
- Garantizar cero solapamientos por `profesional_id` y por `sillon_id` dentro de cada `consultorio_id`.
- Generar DDL PostgreSQL con `EXCLUDE USING gist` (`btree_gist`).
- Proveer servicio de dominio y endpoint FastAPI tipado con Pydantic v2.

**Non-Goals:**
- Gestión de reprogramación, cancelación pública, recordatorios WhatsApp (`C-08`) o Google Calendar sync (`C-09`).

## Decisions

1. **Validación en capa de dominio + respaldo DDL PostgreSQL (`btree_gist`)**: las reglas `RN-AG-03` y `RN-AG-04` se validan tanto en el servicio de dominio Python (permitiendo pruebas rápidas aisladas y mensajes de error claros) como mediante `EXCLUDE USING gist` en PostgreSQL.
2. **Integración Mercado Pago en creación** *(borrador inicial a revisar en protocolo de inspección)*: llamar al cliente de Mercado Pago en la creación del turno cuando la prestación requiera seña.

## Risks / Trade-offs

- La inclusión de Mercado Pago en el flujo síncrono de creación de turnos agrega acoplamiento externo no previsto en la v1.
