# Turnos Odontología — SDD con OpenSpec y Active Stack

Sistema de gestión de turnos y agenda de pacientes para consultorios odontológicos chicos de Argentina (2–5 profesionales), desarrollado siguiendo el flujo completo de **Discovery → Knowledge Base → Roadmap → Skills/Reglas → Ciclo OPSX → Memoria Engram**.

---

## Estructura del Repositorio

```text
turnos-odontologia/
├── AGENTS.md                           # Reglas duras del proyecto para agentes
├── CLAUDE.md                           # Copia canónica de AGENTS.md
├── CHANGES.md                          # Roadmap de 19 changes (C-01..C-19)
├── .active-orchestrator-state.json     # Estado de las etapas de fundación y OPSX
├── .atl/
│   └── skill-registry.md               # Registro compacto de skills (FastAPI, PostgreSQL, Pytest)
├── .engram/                            # Chunks exportados de memoria persistente Engram
├── docs/
│   ├── etapa-0/                        # Capturas de evidencia de Etapa 0 (instalador Full y harnesses)
│   ├── discovery/                      # Investigación de mercado, fuentes y verificación
│   │   ├── informe-discovery.md
│   │   ├── informe-discovery.pdf
│   │   ├── discovery.md
│   │   ├── market-research.md
│   │   └── sources/
│   ├── engram/                         # Evidencia y snapshot de memoria persistente (Etapa 7)
│   │   ├── engram-export.json
│   │   └── etapa-7-memoria-engram.md
│   ├── opsx/                           # Trazabilidad Explore y reporte de Verify
│   │   ├── explore-crear-turno-sin-solapamientos.md
│   │   └── verify-report.md
│   └── Reflexiones.pdf                 # Reflexión escrita grupal (Entregable 4)
├── knowledge-base/                     # Los 10 documentos canónicos de dominio + README
├── openspec/
│   ├── config.yaml
│   ├── specs/
│   │   └── turnos-agenda/spec.md       # Especificación vigente promovida al archivar
│   └── changes/
│       └── archive/
│           └── 2026-11-23-crear-turno-sin-solapamientos/
│               ├── .openspec.yaml
│               ├── exploration.md
│               ├── proposal.md
│               ├── design.md
│               ├── tasks.md
│               └── specs/turnos-agenda/spec.md
├── src/
│   ├── api/app.py                      # API FastAPI (GET /api/v1/health, POST /api/v1/turnos)
│   ├── domain/
│   │   ├── models.py                   # Entidades Pydantic v2, enums y excepciones de dominio
│   │   └── services.py                 # Lógica transaccional AgendaTurnosService
│   └── infrastructure/sql/
│       └── 005_turnos_agenda_btree_gist.sql # DDL PostgreSQL 15+ con EXCLUDE USING gist
├── tests/
│   └── test_crear_turno_sin_solapamientos.py # Suite de tests automatizados por escenario
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Requisitos Previos

- **Python 3.11+** (verificado con Python 3.14.8) y `pip`
- **Git**
- *(Opcional para inspección OpenSpec / Engram)*: Node.js + `@fission-ai/openspec` y `engram` CLI

---

## Instalación y Ejecución de Tests (Paso a Paso)

Siguiendo únicamente estos pasos desde cualquier máquina tras clonar el repositorio:

```bash
# 1. Clonar el repositorio e ingresar al directorio
git clone https://github.com/Ignacio-generoso/turnos-odontologia.git
cd turnos-odontologia

# 2. (Recomendado) Crear y activar entorno virtual
python -m venv .venv
# En Windows PowerShell (si ExecutionPolicy bloquea Activate.ps1, usar directamente .\.venv\Scripts\python.exe):
.venv\Scripts\Activate.ps1
# En Windows CMD:
# .venv\Scripts\activate.bat
# En Linux/macOS:
# source .venv/bin/activate

# 3. Instalar dependencias del proyecto y testing (incluye tzdata para zonas horarias IANA en Windows)
python -m pip install -r requirements.txt
# (Alternativa en Windows sin activar script): .\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 4. Ejecutar toda la suite de tests automatizados
python -m pytest -v
# (Alternativa en Windows sin activar script): .\.venv\Scripts\python.exe -m pytest -v

# 5. (Opcional) Ejecutar con reporte de cobertura línea por línea
python -m pytest -v --cov=src --cov-report=term-missing
```

### Qué cubren los tests (`tests/test_crear_turno_sin_solapamientos.py`)

Todos los casos usan **datos 100 % ficticios** y validan el contrato completo de `openspec/specs/turnos-agenda/spec.md`:
1. **Camino feliz**: creación de turno (`reservado`), cálculo automático de `fin = inicio + duracion_minutos`, `token_publico_hash`, evento `TurnoCreado` y auditoría append-only (`RN-AU-05`).
2. **Error `RN-AG-03` (`409`)**: solapamiento por profesional aunque se intente en otro sillón.
3. **Error `RN-AG-04` (`409`)**: solapamiento por sillón/box entre profesionales distintos.
4. **Caso de borde `[inicio, fin)` (`201`)**: turno contiguo exacto que inicia en el mismo minuto en que termina el anterior (`10:40` tras `10:00–10:40`).
5. **Caso de borde cancelación (`201`)**: horario previamente ocupado por un turno `cancelado` queda liberado.
6. **Bloqueos y disponibilidad (`409` / `422` / `201`)**: respeto de `bloqueos_agenda`, validación de franjas horarias y `sobrecarga = true` restringida a `recepcion`/`dueno`.
7. **Seguridad y reglas duras (`403` / `422`)**: aislamiento multi-consultorio (`RN-AU-01`), control de rol RBAC y rechazo de fechas sin zona horaria (`TIMESTAMPTZ`).

---

## Verificación de OpenSpec y Memoria Engram

```bash
# Validar especificaciones vigentes y changes archivados en modo estricto
openspec validate --all --strict
openspec validate --archived

# Importar memorias versionadas en .engram/ y consultar contexto persistente
engram sync --import
engram search "solapamientos" --project turnos-odontologia
engram context turnos-odontologia
```
