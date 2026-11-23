# Explore — Relevamiento previo: `crear-turno-sin-solapamientos`

**Change roadmap asociado:** `C-06` (`turnos-agenda` — funcionalidad nuclear: crear un turno evitando solapamientos por profesional y por sillón/box)  
**Fecha:** 2026-11-23  
**Responsable:** Tomás Basabe  

---

## 1. Estado actual del repositorio

Al iniciar la **Etapa 6 (Ciclo OPSX)**, el proyecto completó las etapas de fundación (Etapas 1 a 5):

- `docs/discovery/discovery.md` y `docs/discovery/market-research.md`: investigación de mercado verificada sobre 24 sistemas odontológicos; sección D.3 ubica en **#1 Must-Have (v1)** la *"Agenda multi-profesional con vista día/semana y prevención de solapamientos"*.
- `knowledge-base/`: los 10 documentos canónicos del dominio (`04_modelo_de_datos.md`, `05_reglas_de_negocio.md`, `06_funcionalidades.md`, `07_flujos_principales.md`, `08_arquitectura_propuesta.md`, `09_decisiones_y_supuestos.md`, `10_preguntas_abiertas.md`).
- `CHANGES.md`: roadmap con 19 changes (`C-01` a `C-19`), donde `C-06` (`turnos-agenda`) concentra la regla crítica del dominio (`EXCLUDE USING gist` con `btree_gist`).
- `AGENTS.md` / `CLAUDE.md` y `.atl/skill-registry.md`: definen reglas duras del stack (FastAPI + Pydantic v2 + PostgreSQL 15+ `TIMESTAMPTZ` + `btree_gist`, cero datos reales de pacientes, tests automatizados por escenario con `pytest`).
- Código fuente (`src/`) y pruebas (`tests/`): aún vacíos (proyecto sin código previo al primer change OPSX).

---

## 2. Problema a resolver

En consultorios odontológicos chicos de Argentina (2–5 profesionales), la coordinación manual por WhatsApp y teléfono genera **dobles reservas**:
1. Dos pacientes citados con el mismo odontólogo en el mismo horario.
2. Dos odontólogos distintos asignados al mismo sillón/box físico en el mismo rango horario.
3. Turnos agendados sobre bloqueos de agenda o fuera de la franja horaria del profesional, o sin cálculo consistente de duración por prestación.

---

## 3. Reglas de negocio aplicables (`knowledge-base/05_reglas_de_negocio.md`)

| Código | Regla | Impacto técnico |
|---|---|---|
| `RN-AU-01` | Aislamiento lógico por `consultorio_id` | Todos los recursos vinculados al turno (profesional, sillón, prestación, paciente) deben pertenecer al mismo `consultorio_id`. |
| `RN-AG-01` | Duración variable según prestación | `fin = inicio + duracion_minutos`. Toma la duración base de `prestacion.duracion_minutos` (en agenda interna puede ajustarse manualmente si es `> 0`). |
| `RN-AG-02` | Asignación obligatoria de profesional y sillón/box | Todo turno activo requiere `profesional_id` (usuario activo con rol `odontologo`) y `sillon_id` activo del mismo consultorio. |
| `RN-AG-03` | Prevención de solapamientos por profesional | Ningún profesional puede tener dos turnos activos (`estado != 'cancelado'`) con intervalos `[inicio, fin)` superpuestos ni invadir un `bloqueo_agenda` vigente para ese profesional. |
| `RN-AG-04` | Prevención de solapamientos por sillón/box | Ningún sillón/box puede tener dos turnos activos (`estado != 'cancelado'`) superpuestos (aun de profesionales distintos) ni invadir un `bloqueo_agenda` vigente para ese sillón. |
| `RN-AG-05` | Disponibilidad horaria del profesional | El turno debe encuadrar dentro de una franja activa de `disponibilidades_profesional`, salvo `sobrecarga=True` explícita autorizada a `recepcion` o `dueno` (manteniendo sin excepciones `RN-AG-03` y `RN-AG-04`). |
| `RN-AU-05` | Auditoría básica obligatoria | Toda creación de turno registra un evento append-only en `auditoria_eventos`. |

---

## 4. Hallazgos técnicos y casos de borde detectados

1. **Semántica de intervalo semiabierto `[inicio, fin)`**:
   - En `knowledge-base/04_modelo_de_datos.md` y `05_reglas_de_negocio.md`, los constraints de PostgreSQL usan `tstzrange(inicio, fin, '[)') WITH &&`.
   - Dos intervalos `[A, B)` y `[C, D)` se solapan si y solo si `A < D AND C < B`.
   - Por lo tanto, un turno de `10:00` a `10:40` y otro de `10:40` a `11:10` **no se solapan** (`10:00 < 11:10` pero `10:40 < 10:40` es falso).
2. **Turnos cancelados (`estado == 'cancelado'`)**:
   - Tanto la lógica de dominio como el índice parcial `WHERE (estado <> 'cancelado')` en PostgreSQL liberan inmediatamente profesional y sillón cuando un turno pasa a `cancelado`.
3. **Timestamps con zona horaria (`TIMESTAMPTZ`)**:
   - Regla dura de `AGENTS.md`: prohibido usar `datetime` naive sin zona horaria; todas las fechas deben incluir `tzinfo` explícito (ej. `America/Argentina/Buenos_Aires` `-03:00` o UTC).
4. **Restricciones de alcance (`DD-02`, `DD-03`, `IN-01`)**:
   - En v1 no se integra pasarela de pago online (Mercado Pago queda diferido a v1.1) ni API automática de Meta WhatsApp. El change debe acotarse estrictamente a la creación de turnos y su validación anti-solapamientos.
5. **Privacidad (`AGENTS.md` — Regla propia del dominio)**:
   - Todos los datos de pacientes en código, fixtures y tests deben ser **100 % ficticios**.

---

## 5. Conclusión del Explore

El change está listo para pasar a **Propose** con una especificación centrada en `POST /api/v1/turnos` y el servicio de dominio `AgendaTurnosService.crear_turno`, acompañado por el DDL PostgreSQL `EXCLUDE USING gist` (`btree_gist`) y pruebas automatizadas por cada escenario.
