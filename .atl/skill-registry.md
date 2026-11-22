# Skill Registry

**Delegator use only.** Any agent that launches sub-agents reads this registry to resolve compact rules, then injects them directly into sub-agent prompts. Sub-agents do NOT read this registry or individual SKILL.md files.

## User Skills

| Trigger | Skill | Path |
|---|---|---|
| FastAPI APIs, Pydantic v2 models, dependencies (RBAC), routers, streaming | `fastapi` | `.agents/skills/fastapi/SKILL.md` |
| Designing or reviewing PostgreSQL schemas, data types, constraints (`EXCLUDE`), indexes | `postgresql-table-design` | `.agents/skills/postgresql-table-design/SKILL.md` |
| Running pytest tests with coverage, discovering uncovered lines, reaching full coverage | `pytest-coverage` | `.agents/skills/pytest-coverage/SKILL.md` |

## Compact Rules

Pre-digested rules per skill. Delegators copy matching blocks into sub-agent prompts as `## Project Standards (auto-resolved)`.

### fastapi
- Always use `Annotated[..., Path/Query/Header/Depends(...)]` for parameter and dependency declarations; define reusable type aliases for dependencies (e.g., `CurrentUserDep = Annotated[User, Depends(get_current_user)]`).
- Never use `...` (Ellipsis) as default value for required parameters or Pydantic fields.
- Declare explicit return types on path operations (`async def get_x() -> XSchema:`) or use `response_model` when the internal return differs from the public schema; Pydantic v2 serializes on Rust side.
- Never use deprecated `ORJSONResponse` or `UJSONResponse`.
- Declare `prefix`, `tags`, and shared `dependencies` directly on `APIRouter(...)` rather than `include_router()`.
- Never use `RootModel` when a standard Pydantic model or type alias suffices.
- Reuse generated OpenAPI SDK/clients when present; regenerate when schema changes instead of manual edits.

### postgresql-table-design
- Prefer `BIGINT GENERATED ALWAYS AS IDENTITY` for surrogate PKs (never `serial`); use `UUID` (`gen_random_uuid()`) only when global opacity/uniqueness is required (e.g., public tokens).
- Use `TIMESTAMPTZ` for all event/appointment timestamps (never `timestamp` without time zone or `timetz`); use `NUMERIC(p,s)` for ARS money (never `money` or float); use `TEXT` + `CHECK` instead of `varchar(n)`/`char(n)`.
- PostgreSQL does NOT auto-index foreign key columns: always create explicit indexes on FK columns and frequent filter/sort columns (`consultorio_id`, `profesional_id`, `inicio`).
- Use `EXCLUDE USING gist (...)` constraints (with `btree_gist`) to enforce zero-overlap guarantees at database level for `profesional_id` and `sillon_id` over `tstzrange(inicio, fin, '[)')` for active appointments (`WHERE (estado <> 'cancelado')`).
- Use `UNIQUE NULLS NOT DISTINCT` (PG15+) when NULLs should not duplicate; combine `NOT NULL` with `CHECK` constraints (since `CHECK` passes on NULL).
- Use `snake_case` unquoted identifiers; add `ON DELETE`/`ON UPDATE` explicitly on FKs; never delete clinical/financial records destructively.

### pytest-coverage
- Run coverage reports with `pytest --cov=<module> --cov-report=annotate:cov_annotate` (or `pytest --cov --cov-report=annotate:cov_annotate`).
- Inspect generated files in `cov_annotate/` for any source file below 100% coverage; lines prefixed with `!` are uncovered.
- Add targeted unit and integration tests for every uncovered branch (happy path, business rule errors, boundary/edge cases) until all critical paths are covered.
- Do not commit `cov_annotate/` or `.coverage` artifacts to git.

## Project Conventions

| File | Path | Notes |
|---|---|---|
| Knowledge Base (index) | `knowledge-base/README.md` | Índice de los 10 documentos canónicos del dominio |
| Reglas de negocio | `knowledge-base/05_reglas_de_negocio.md` | Códigos `RN-AU-*`, `RN-AG-*`, `RN-WA-*`, `RN-GC-*`, `RN-CL-*`, `RN-PG-*` |
| Arquitectura propuesta | `knowledge-base/08_arquitectura_propuesta.md` | Stack FastAPI + PostgreSQL + React + TS + Docker y estructura de módulos |
| Roadmap de changes | `CHANGES.md` | Árbol de dependencias `C-01`..`C-19` y paralelismo |
| Reglas del agente | `AGENTS.md` | Reglas duras del proyecto (se genera/actualiza en `agent-instruction`) |
| Reglas para Claude | `CLAUDE.md` | Copia idéntica de `AGENTS.md` |

Read the convention files listed above for project-specific patterns and rules.
