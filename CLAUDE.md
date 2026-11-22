# Turnos Odontología — Instrucciones para Agentes

> Este archivo (y su copia `CLAUDE.md`) es lo PRIMERO que todo agente lee al entrar al repo.
> Generado a partir de `knowledge-base/` y `CHANGES.md`. No editar a mano sin re-sincronizar ambos archivos.

---

## Stack Tecnológico

| Capa | Tecnología | Versión mínima recomendada |
|---|---|---|
| **Frontend** | React + TypeScript + Vite (PWA responsive) | React 18+, TS 5+ |
| **Backend / API** | Python + FastAPI + Pydantic v2 | Python 3.11+, FastAPI 0.110+ |
| **ORM / Migraciones** | SQLAlchemy 2.0 + Alembic | SQLAlchemy 2.0+, Alembic 1.13+ |
| **Base de datos** | PostgreSQL (`btree_gist` para anti-solapamientos) | PostgreSQL 15+ |
| **Background / Jobs** | Worker ligero Python (APScheduler / tareas async) | — |
| **Contenerización** | Docker + Docker Compose | Docker 24+ |
| **Proxy / TLS** | Nginx o Caddy | — |
| **Integraciones v1** | Google Calendar API v3 (1-way), WhatsApp (`wa.me` asistido), Exportación CSV/PDF (ARCA/OS) | — |

Detalle completo: [knowledge-base/02_descripcion_general.md](knowledge-base/02_descripcion_general.md)

---

## Base de Conocimiento

La fuente de verdad del dominio vive en `knowledge-base/`. **Leé el archivo relevante ANTES de implementar.**

| Archivo | Cuándo leerlo |
|---|---|
| [01_vision_y_objetivos.md](knowledge-base/01_vision_y_objetivos.md) | Entender propósito, alcance v1 y diferido post-MVP |
| [03_actores_y_roles.md](knowledge-base/03_actores_y_roles.md) | Auth, RBAC y bloqueo clínico estricto |
| [04_modelo_de_datos.md](knowledge-base/04_modelo_de_datos.md) | Entidades, `consultorio_id`, constraints `btree_gist`, migraciones |
| [05_reglas_de_negocio.md](knowledge-base/05_reglas_de_negocio.md) | Reglas codificadas (`RN-AU-*`, `RN-AG-*`, `RN-WA-*`, `RN-GC-*`, `RN-CL-*`, `RN-PG-*`) |
| [06_funcionalidades.md](knowledge-base/06_funcionalidades.md) | Historias de usuario (`US-001` a `US-014`) por épica |
| [07_flujos_principales.md](knowledge-base/07_flujos_principales.md) | Flujos end-to-end |
| [08_arquitectura_propuesta.md](knowledge-base/08_arquitectura_propuesta.md) | Patrones, estructura de directorios, seguridad, residencia en AR, env vars |
| [09_decisiones_y_supuestos.md](knowledge-base/09_decisiones_y_supuestos.md) | Decisiones (`DD-01`..`DD-07`) y supuestos (`SU-01`..`SU-05`) |
| [10_preguntas_abiertas.md](knowledge-base/10_preguntas_abiertas.md) | ⚠️ Inconsistencias y preguntas de prioridad Alta a resolver antes de codear |

> ⚠️ Resolver las preguntas de prioridad **Alta** de `knowledge-base/10_preguntas_abiertas.md` antes de arrancar la implementación productiva.

---

## Skills Disponibles

| Agente | Rol | Skills que carga |
|---|---|---|
| **Backend Core** | FastAPI / SQLAlchemy / PostgreSQL / Tests | `fastapi`, `postgresql-table-design`, `pytest-coverage` |
| **Backend Aux** | Servicios, integraciones, seguridad | `fastapi`, `postgresql-table-design`, `pytest-coverage` |
| **Orquestación** | SDD / OPSX | `openspec-explore`, `openspec-propose`, `openspec-apply-change`, `openspec-archive-change` |

Cargá la skill correspondiente al contexto ANTES de escribir código.

> Los compact rules de cada skill los resuelve el orquestador desde [.atl/skill-registry.md](.atl/skill-registry.md) (generado por `skill-registry`). Esta tabla solo mapea skill → rol.

---

## Roadmap de Changes

El plan de implementación completo está en [CHANGES.md](CHANGES.md). Resumen:

- **Total**: 19 changes (`C-01` a `C-19`), organizados en gates paralelizables para hasta 3 agentes.
- **Camino crítico** (10 changes): `C-01 → C-02 → C-03 → C-04 → C-06 → C-10 → C-11 → C-12 → C-13 → C-19`.
- **Primer change**: `C-01` (`foundation-setup`), que desbloquea los modelos core y la agenda sin solapamientos (`C-06`).

**Antes de cualquier `/opsx:propose`**: leé [CHANGES.md](CHANGES.md), identificá las dependencias del change y los archivos indicados en "Leer antes".

---

## Reglas Duras (específicas del proyecto)

> No se detectó `~/.claude/CLAUDE.md` global en el entorno; las reglas de flujo, dominio y stack aplicables al repositorio quedan consolidadas explícitamente a continuación. Son contrato; romperlas es un defecto.

### Stack Tecnológico
- **Validación estricta en API**: NUNCA definir schemas Pydantic sin tipado explícito ni omitir validación de entrada → usar Pydantic v2 con tipos estrictos, `Annotated[..., Depends(...)]` en FastAPI y return types explícitos en endpoints.
- **Fechas y dinero en PostgreSQL**: NUNCA usar `timestamp` sin zona horaria ni `float`/`money` para importes → usar siempre `TIMESTAMPTZ` (zona horaria consistente) y `NUMERIC` para montos en ARS.
- **Prevención de solapamientos a nivel BD**: NUNCA validar superposición de turnos solo en Python → garantizarla también con constraints `EXCLUDE USING gist` (`btree_gist`) en PostgreSQL por `profesional_id` y por `sillon_id` para turnos activos (`estado != 'cancelado'`).
- **Tipado estricto en Frontend**: NUNCA usar `any` en TypeScript → mantener `tsconfig` estricto y componentes React en `PascalCase`.
- **Tests reales por escenario**: NUNCA dar por terminado un change sin tests automatizados en verde (`pytest`) que cubran al menos camino feliz, error de negocio y caso borde de la especificación.

### Dominio Odontológico (Reglas Propias)
- **Cero datos reales de pacientes en el código/repo**: NUNCA hardcodear ni subir datos reales de pacientes (nombres, DNI, teléfonos, historias clínicas) al repositorio, `seeds`, tests o capturas → usar siempre datos 100 % ficticios en desarrollo y pruebas (los datos reales solo existen en la base de datos de producción).
- **Aislamiento lógico por consultorio (`RN-AU-01`)**: NUNCA consultar o mutar entidades de negocio sin filtrar por `consultorio_id` del usuario autenticado (o por `slug` en rutas públicas).
- **Aislamiento clínico estricto (`RN-AU-02` / `DD-06`)**: NUNCA permitir acceso a historia clínica, odontograma o planes de tratamiento a roles no clínicos → exigir rol `odontologo` activo (incluso `dueno`, `recepcion` o `administracion` sin rol clínico deben recibir `403 Forbidden`).
- **Trazabilidad y no borrado destructivo (`RN-AU-03` / `RN-PG-02`)**: NUNCA eliminar físicamente evoluciones clínicas, odontogramas ni pagos → versionar o anular con motivo obligatorio y registrar el evento en `auditoria_eventos`.
- **Privacidad en integraciones externas (`RN-GC-03`)**: NUNCA enviar diagnósticos ni datos clínicos en eventos de Google Calendar → incluir solo horario, prestación y referencia mínima del turno.

### Flujo de Trabajo y Repositorio
- **Trabajo guiado por specs (OPSX)**: NUNCA improvisar funcionalidad fuera del spec aprobado en `openspec/` → si algo cambia durante `Apply`, volver a `Propose` y marcar `[x]` en `CHANGES.md` recién al archivar.
- **Secretos y configuración**: NUNCA commitear claves, tokens OAuth ni archivos `.env` reales → usar `.env.example` y mensajes de commit descriptivos por etapa/change.

---

## Flujo de Trabajo

```
1. Leer la KB relevante (knowledge-base/)        → entender el dominio y las RN-XX-NN
2. Identificar el change en CHANGES.md           → respetar dependencias y "Leer antes"
3. /opsx:explore + /opsx:propose <change>        → proposal + design + specs + tasks
4. Implementar las tasks (cargando skills)       → respetando las reglas duras y tests
5. Verificar y /opsx:archive <change>            → tests en verde + marcar [x] en CHANGES.md
```

Aplicar TODAS las reglas duras en cada paso. Ante conflicto entre la KB y este archivo, las reglas duras prevalecen.
