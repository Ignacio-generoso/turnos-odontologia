# Explore — Relevamiento previo: `crear-turno-sin-solapamientos`

Copia de trazabilidad en `docs/opsx/` del relevamiento inicial de la fase **Explore** de OpenSpec.  
El documento canónico del change reside en `openspec/changes/crear-turno-sin-solapamientos/exploration.md` (y luego en `openspec/changes/archive/` al completar el ciclo).

- **Change seleccionado del roadmap (`CHANGES.md`)**: `C-06` (alcance acotado a creación de turnos sin solapamientos por profesional y por sillón/box).
- **Reglas de negocio relevadas**: `RN-AU-01`, `RN-AG-01`, `RN-AG-02`, `RN-AG-03`, `RN-AG-04`, `RN-AG-05`, `RN-AU-05`.
- **Restricciones verificadas**: intervalo semiabierto `[inicio, fin)`, exclusión de turnos `cancelado`, obligatoriedad de `TIMESTAMPTZ`, cero datos reales de pacientes y exclusión de pasarelas de pago online (`DD-03` / `IN-01`).
