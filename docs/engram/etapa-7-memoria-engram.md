# Etapa 7 — Memoria Persistente del Agente con Engram

**Proyecto:** `turnos-odontologia`  
**Fecha:** 2026-11-23  
**Responsable:** Tomás Basabe  

---

## 1. Qué quedó guardado en Engram sobre este proyecto

Se registraron **5 observaciones estructuradas** bajo `--project turnos-odontologia` y `--scope project` en la base local (`C:\Users\Hp\.engram\engram.db`), sincronizadas además al repositorio en `.engram/` (chunk `3822f934`) y exportadas en JSON legible en [`docs/engram/engram-export.json`](engram-export.json):

| ID | Tipo | Topic Key | Título y contenido resumido |
|---|---|---|---|
| `#1` | `discovery` | `discovery-mvp` | **Discovery: hallazgos y MVP Turnos Odontologia AR** — Relevamiento de 24 sistemas, correcciones manuales de Dentia/Dentatools y definición de MVP v1 (`wa.me`, pagos manuales, aislamiento clínico, residencia AR). |
| `#2` | `architecture` | `arquitectura-btree-gist` | **Arquitectura y DDL PostgreSQL btree_gist** — Stack FastAPI + Pydantic v2 + PostgreSQL 15+, `TIMESTAMPTZ`, `NUMERIC(12,2)` y dos constraints `EXCLUDE USING gist` sobre `tstzrange(inicio, fin, '[)')` excluyendo `cancelado`. |
| `#3` | `convention` | `convenciones-reglas` | **Convenciones y reglas duras del proyecto** — Cero datos reales de pacientes, aislamiento `consultorio_id` (`RN-AU-01`), bloqueo clínico `403` (`RN-AU-02`), reglas de FastAPI y contrato OPSX. |
| `#4` | `decision` | `opsx-ajuste-propose` | **Ajuste en Propose del change C-06 crear-turno-sin-solapamientos** — Registro de la aplicación de `Ajustar`: exclusión de Mercado Pago (diferido a v1.1), corrección a intervalo semiabierto `[inicio, fin)` y cobertura de 7 escenarios. |
| `#5` | `pattern` | `opsx-cierre-c06` | **Cierre OPSX: crear-turno-sin-solapamientos archivado y verificado** — Ubicación del archivo archivado, spec vigente en `openspec/specs/turnos-agenda/spec.md`, módulos implementados y resultado `9/9 passed` (`100 %` cobertura). |

---

## 2. Evidencia de consulta real ejecutada

Comandos reales ejecutados contra la base de Engram para recuperar contexto entre sesiones:

### 2.1 Estadísticas y listado de proyectos (`engram stats` y `engram projects list`)
```text
Engram Memory Stats
  Sessions:     1
  Observations: 5
  Prompts:      0
  Projects:     turnos-odontologia
  Database:     C:\Users\Hp\.engram/engram.db

Projects (1):
  turnos-odontologia                5 obs     1 session      0 prompts
```

### 2.2 Búsqueda semántica/FTS (`engram search "solapamientos" --project turnos-odontologia`)
```text
Found 4 memories:

[1] #5 (pattern) — Cierre OPSX: crear-turno-sin-solapamientos archivado y verificado
    Change C-06 archivado en openspec/changes/archive/2026-11-23-crear-turno-sin-solapamientos/ ...
[2] #4 (decision) — Ajuste en Propose del change C-06 crear-turno-sin-solapamientos
    Protocolo de inspeccion en Propose -> Ajustar: se detectaron 3 errores en el borrador inicial ...
[3] #2 (architecture) — Arquitectura y DDL PostgreSQL btree_gist
    Stack elegido (DD-04): FastAPI + Pydantic v2 + PostgreSQL 15+ ...
[4] #1 (discovery) — Discovery: hallazgos y MVP Turnos Odontologia AR
    Se relevaron 24 sistemas odontologicos (19 con evidencia + 5 SPA) ...
```

### 2.3 Búsqueda específica por decisión (`engram search "Mercado Pago" --project turnos-odontologia`)
```text
Found 1 memories:

[1] #4 (decision) — Ajuste en Propose del change C-06 crear-turno-sin-solapamientos
    Protocolo de inspeccion en Propose -> Ajustar: se detectaron 3 errores en el borrador inicial:
    (1) incluia cobro automatico con Mercado Pago que estaba diferido a v1.1 (DD-03/IN-01);
    (2) usaba intervalo cerrado [inicio, fin] rechazando turnos contiguos exactos (10:40 tras 10:00-10:40);
    (3) faltaban escenarios de bloqueos y aislamiento multi-consultorio.
```

### 2.4 Recuperación de contexto completo de sesión (`engram context turnos-odontologia`)
```text
## Memory from Previous Sessions

### Recent Sessions
- **turnos-odontologia** (2026-11-23 11:18:53) [5 observations]

### Recent Observations
- [pattern] **Cierre OPSX: crear-turno-sin-solapamientos archivado y verificado** ...
- [decision] **Ajuste en Propose del change C-06 crear-turno-sin-solapamientos** ...
- [convention] **Convenciones y reglas duras del proyecto** ...
- [architecture] **Arquitectura y DDL PostgreSQL btree_gist** ...
- [discovery] **Discovery: hallazgos y MVP Turnos Odontologia AR** ...
```

---

## 3. Cómo evita que el agente arranque de cero entre sesiones

Cuando un agente inicia una nueva sesión (por ejemplo, para implementar el siguiente change del roadmap como `C-07 public-booking` o `C-08 whatsapp-reminders`), normalmente pierde el contexto conversacional de sesiones previas y corre riesgo de repetir errores ya descartados (como volver a sugerir Mercado Pago en v1 o usar intervalos cerrados `[inicio, fin]`).

Al consultar **Engram** mediante `engram context turnos-odontologia` o `engram search "..."` (o mediante MCP `mem_context` / `mem_search` cuando el agente corre conectado al servidor MCP de Engram):
1. **Recupera decisiones y descartes previos sin re-leer todo el historial**: recuerda al instante que Mercado Pago y Meta WhatsApp API están diferidos a v1.1 (`DD-02`, `DD-03`) y por qué se ajustó `C-06`.
2. **Mantiene coherencia arquitectónica entre sesiones y personas del equipo**: mediante `engram sync` (`.engram/`), cualquier integrante que clone el repositorio puede importar los chunks (`engram sync --import`) y disponer de las mismas decisiones (`btree_gist`, `TIMESTAMPTZ`, `RN-AU-02`) sin volver a explicarlas en cada prompt.
3. **Reduce tokens y ambigüedad**: complementa a `AGENTS.md` (reglas estáticas) y a `knowledge-base/` (especificación del dominio) aportando la memoria episódica de lo que ya se probó, corrigió y archivó.

---

## 4. Comandos rápidos para reproducir en otro equipo (Video de Defensa)

Si un integrante clona el repositorio en una computadora nueva antes de grabar el video:

```bash
# 1. Importar las memorias versionadas desde .engram/ a la DB local del equipo
engram sync --import

# 2. Verificar estado y proyectos cargados
engram stats
engram projects list

# 3. Ejecutar las consultas reales frente a cámara
engram search "solapamientos" --project turnos-odontologia
engram search "Mercado Pago" --project turnos-odontologia
engram context turnos-odontologia
engram timeline 4
```
