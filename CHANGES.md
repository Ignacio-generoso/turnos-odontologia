# CHANGES — Secuencia de Implementación

> Índice canónico de todos los changes del proyecto **Turnos Odontología** (MVP v1).
> Cada change es atómico: un agente puede implementarlo en una sesión (~4-6 horas).
> **Leer este archivo antes de empezar un item.**

---

## Cómo usar este documento

1. Identificar el item a implementar y verificar que sus dependencias figuran completas en este roadmap.
2. Leer los docs de la `knowledge-base/` indicados en "Leer antes".
3. Acordar el alcance y los criterios de aceptación del item.
4. Implementar, verificar los criterios acordados y registrar la evidencia.
5. Marcar el checkbox `[x]` en este archivo al completar la verificación técnica.

Conservá los IDs de las fichas al editar o reordenar. Si el proyecto usa ClickUp,
este roadmap conserva el alcance y las dependencias. Consultá el responsable y el estado operativo
en ClickUp y el último dato confirmado en `.active-stack/roadmap-state.json`.

---

## Árbol de dependencias

```
C-01 foundation-setup
  └── C-02 core-models-audit
        └── C-03 auth-rbac                               ← desbloquea configuración y pacientes
              │
              ├── C-04 consultorio-config
              │     └── C-14 frontend-shell-config       ← shell PWA + auth + config
              │
              ├── C-05 pacientes-coberturas              ← paralelo con C-04
              │
              └── [C-04 + C-05]
                    └── C-06 turnos-agenda               ← CORE: agenda sin solapamientos
                          │
                          ├── [C-14] → C-17 frontend-pacientes
                          │
                          ├── C-07 public-booking
                          │     └── C-15 frontend-public-booking
                          │
                          ├── C-08 whatsapp-reminders    ← wa.me 1 clic con opt-in
                          │
                          ├── C-09 google-calendar-sync  ← sync 1-way Sistema → Google (C-06 + C-07)
                          │     └── [C-08 + C-09 + C-14]
                          │           └── C-16 frontend-agenda
                          │
                          └── [C-05 + C-06]
                                └── C-10 clinica-odontograma  ← solo rol odontologo
                                      ├── [C-14 + C-17] → C-18 frontend-clinica
                                      └── [C-04] → C-11 presupuestos-versionados
                                            └── [C-06] → C-12 pagos-manuales
                                                  └── C-13 exportaciones-reportes
                                                        └── [C-11 + C-12 + C-14 + C-17]
                                                              └── C-19 frontend-pagos-reportes
```

### Paralelismo por fase

> Cada "gate" es un punto de sincronización. Los changes dentro de un grupo pueden ejecutarse en paralelo.

```
GATE 0: ninguna
  → C-01 foundation-setup                        [Agente A]

GATE 1: C-01 ✓
  → C-02 core-models-audit                       [Agente A]

GATE 2: C-02 ✓
  → C-03 auth-rbac                               [Agente A]

GATE 3: C-03 ✓                                   ← PRIMER FORK
  → C-04 consultorio-config                      [Agente A]
  → C-05 pacientes-coberturas                    [Agente B]

GATE 4: C-04 ✓
  → C-14 frontend-shell-config                   [Agente C]
  → C-06 turnos-agenda                           [Agente A — si C-05 ✓]

GATE 5: C-06 ✓                                   ← FORK PRINCIPAL (5 paralelos)
  → C-07 public-booking                          [Agente B]
  → C-08 whatsapp-reminders                      [Agente B]
  → C-10 clinica-odontograma                     [Agente A — si C-05 ✓]
  → C-17 frontend-pacientes                      [Agente C — si C-05 + C-14 ✓]

GATE 6: C-07 ✓
  → C-09 google-calendar-sync                    [Agente B — si C-06 ✓]
  → C-15 frontend-public-booking                 [Agente C — si C-01 ✓]

GATE 7: C-10 ✓
  → C-11 presupuestos-versionados                [Agente A — si C-04 ✓]
  → C-18 frontend-clinica                        [Agente C — si C-14 + C-17 ✓]

GATE 8: C-08 + C-09 + C-14 ✓
  → C-16 frontend-agenda                         [Agente C]

GATE 9: C-11 ✓
  → C-12 pagos-manuales                          [Agente A — si C-06 ✓]

GATE 10: C-12 ✓
  → C-13 exportaciones-reportes                  [Agente A]

GATE 11: C-11 + C-12 + C-13 + C-14 + C-17 ✓
  → C-19 frontend-pagos-reportes                 [Agente C]
```

### Camino crítico (10 changes — mínimo irreducible)

```
C-01 → C-02 → C-03 → C-04 → C-06 → C-10 → C-11 → C-12 → C-13 → C-19
```

### Plan óptimo con 3 agentes

```
Paso │ Agente A (Backend Core)        │ Agente B (Backend Aux)      │ Agente C (Frontend)
─────┼────────────────────────────────┼─────────────────────────────┼──────────────────────────────────
  1  │ C-01 foundation-setup          │             —               │             —
  2  │ C-02 core-models-audit         │             —               │             —
  3  │ C-03 auth-rbac                 │             —               │             —
  4  │ C-04 consultorio-config        │ C-05 pacientes-coberturas   │             —
  5  │ C-06 turnos-agenda             │             —               │ C-14 frontend-shell-config
  6  │ C-10 clinica-odontograma       │ C-07 public-booking         │ C-17 frontend-pacientes
  7  │ C-11 presupuestos-versionados  │ C-09 google-calendar-sync   │ C-15 frontend-public-booking
  8  │ C-12 pagos-manuales            │ C-08 whatsapp-reminders     │ C-18 frontend-clinica
  9  │ C-13 exportaciones-reportes    │             —               │ C-16 frontend-agenda
 10  │             —                  │             —               │ C-19 frontend-pagos-reportes
```

---

## FASE 0 — Cimientos e Infraestructura

### [C-01] `foundation-setup`
- **Estado**: `[ ]` pendiente
- **Scope**: Scaffolding del monorepo modular + infraestructura Docker local desplegable en Argentina
  - Estructura de directorios: `backend/` (FastAPI monolito modular `app/core`, `app/shared`, `app/modules/*`), `frontend/` (Vite + React 18+ + TypeScript + PWA), `docker-compose.yml`, `.env.example` en raíz, `backend/` y `frontend/`
  - `backend/`: FastAPI mínima con `GET /api/v1/health` (verifica conectividad PostgreSQL), `app/core/config.py` (Pydantic Settings con variables `${VAR}` sin secretos hardcodeados), `app/core/db.py` (SQLAlchemy 2.0 async), `app/shared/` (`exceptions.py`, `pagination.py`, `logger.py`, `events.py` bus de eventos internos in-process), Alembic inicializado
  - `frontend/`: scaffolding React + TypeScript + Vite PWA responsive, proxy `/api` a backend, `src/shared/api/client.ts` y formateadores ARS/fecha (`America/Argentina/Buenos_Aires`)
  - Contenedores y residencia AR: `docker-compose.yml` con PostgreSQL 15+, backend, frontend y reverse proxy Caddy/Nginx + script/runbook de backup diario cifrado (`pg_dump` + GPG/age) en infraestructura alojada en Argentina
  - CI: workflow con jobs paralelos de lint + test backend (`pytest`) y typecheck/build frontend (`tsc` + `vite build`)
  - Riesgo / pendiente (`SU-05`): proveedor VPS concreto en Argentina por confirmar según presupuesto antes del despliegue productivo
  - Tests: `GET /api/v1/health` devuelve 200 con DB activa; build frontend sin errores
- **Dependencias**: ninguna
- **Governance**: BAJO
- **Leer antes**:
  - `knowledge-base/01_vision_y_objetivos.md` §Propósito del sistema y Alcance v1
  - `knowledge-base/02_descripcion_general.md` §Stack tecnológico y Arquitectura general
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios propuesta, Seguridad y Residencia de Datos en Argentina y Variables de entorno
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-04 y SU-05
  - `knowledge-base/10_preguntas_abiertas.md` §Preguntas abiertas del proyecto

---

### [C-02] `core-models-audit`
- **Estado**: `[ ]` pendiente
- **Scope**: Modelos core multi-consultorio (`consultorio_id`), base de auditoría append-only y seed piloto
  - Modelos SQLAlchemy: `Consultorio`, `Usuario`, `UsuarioRol` (ENUM `'dueno'`, `'odontologo'`, `'recepcion'`, `'administracion'`), `AuditoriaEvento` (append-only)
  - `TenantAuditMixin` (`consultorio_id` FK, `created_at` y `updated_at` UTC `TIMESTAMPTZ`, borrado lógico `activo`), `BaseRepository[T]`, `UnitOfWork`, y servicio `audit_logger.log(...)`
  - Migración `001_core_tables.py`: habilitación de extensión PostgreSQL `btree_gist` y creación de `consultorios`, `usuarios`, `usuario_roles`, `auditoria_eventos` con `UNIQUE(slug)`, `UNIQUE(consultorio_id, email)`, `UNIQUE(usuario_id, rol)`
  - Seed idempotente inicial: 1 consultorio piloto (`slug: "consultorio-piloto"`, `zona_horaria: "America/Argentina/Buenos_Aires"`, `anticipacion_minima_cancelacion_hs: 24`) y 1 usuario inicial con rol `dueno`
  - Tests: unicidad de `slug` y `(consultorio_id, email)`, aislamiento lógico por `consultorio_id`, escritura append-only en `auditoria_eventos`, idempotencia del seed
- **Dependencias**: `C-01`
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Entidades (`consultorios`, `usuarios`, `auditoria_eventos`) y Seed data inicial
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: Autenticación y Privacidad Clínica (RN-AU) y RN-AU-05
  - `knowledge-base/08_arquitectura_propuesta.md` §Patrones aplicados
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-01

---

## FASE 1 — Autenticación, RBAC y Configuración del Consultorio

### [C-03] `auth-rbac`
- **Estado**: `[ ]` pendiente
- **Scope**: Autenticación JWT con Argon2id, RBAC estricto y gestión de usuarios/roles (`US-002`)
  - `POST /api/v1/auth/login` — verificación Argon2id, JWT access (15–30 min) + refresh token rotativo en cookie `HttpOnly` (`Secure`, `SameSite=Lax`), rate limiting por IP+email
  - `POST /api/v1/auth/refresh` y `POST /api/v1/auth/logout` — rotación y revocación en tabla `refresh_tokens`
  - `GET /api/v1/auth/me` — perfil, `consultorio_id` y roles activos
  - Migración `002_refresh_tokens.py`: tabla `refresh_tokens` con expiración y estado de revocación
  - Dependencias FastAPI: `get_current_user` (valida estado `activo` en BD), `require_roles(*roles)` con filtro obligatorio `consultorio_id` (`RN-AU-01`), y guard clínico `require_odontologo()` (`403 Forbidden` incluso para `dueno` sin rol `odontologo`, `RN-AU-02`)
  - CRUD usuarios/roles para `dueno` (`US-002`): `GET/POST /api/v1/usuarios`, `PATCH /api/v1/usuarios/{id}` (soporta rol dual `dueno`+`odontologo` y desactivación lógica sin borrar historial)
  - Tests: login exitoso/fallido, rate limit, rotación/revocación de refresh token, bloqueo `403` para `dueno` sin rol `odontologo`, gestión de roles y baja lógica
- **Dependencias**: `C-02`
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §RBAC — Matriz de permisos y Regla crítica de privacidad clínica
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: Autenticación y Privacidad Clínica (RN-AU)
  - `knowledge-base/06_funcionalidades.md` §US-002
  - `knowledge-base/08_arquitectura_propuesta.md` §Seguridad y Residencia de Datos en Argentina

---

### [C-04] `consultorio-config`
- **Estado**: `[ ]` pendiente
- **Scope**: Configuración del consultorio, sillones/boxes, prestaciones y disponibilidad horaria (`US-001`)
  - Modelos: `Sillon`, `Prestacion`, `DisponibilidadProfesional`, `BloqueoAgenda`
  - Migración `003_consultorio_config.py`: tablas `sillones`, `prestaciones`, `disponibilidades_profesional`, `bloqueos_agenda` con checks (`duracion_minutos > 0`, `hora_fin > hora_inicio`, `fin > inicio`, `profesional_id` o `sillon_id` no nulo en bloqueos)
  - Seed de catálogo base: 2 sillones (`Sillón 1`, `Sillón 2`) y 6 prestaciones estándar (`Consulta` 30m, `Limpieza` 40m, `Obturación` 45m, `Endodoncia` 60m, `Extracción` 45m, `Control` 20m)
  - Endpoints (`dueno` muta, equipo interno lee): `GET/PUT /api/v1/consultorio` (`anticipacion_minima_cancelacion_hs`), `GET/POST/PATCH/DELETE(lógico) /api/v1/sillones`, `GET/POST/PATCH/DELETE(lógico) /api/v1/prestaciones`, `GET/POST/PATCH/DELETE /api/v1/profesionales/horarios`, `GET/POST/DELETE /api/v1/bloqueos-agenda`
  - Riesgo / pendiente (`10_preguntas_abiertas.md`): validar si `anticipacion_minima_cancelacion_hs = 24` hs coincide con la política real del consultorio piloto
  - Tests: validación de duración > 0, rangos horarios válidos en disponibilidades/bloqueos, unicidad de nombre de sillón por consultorio, RBAC de escritura exclusivo para `dueno`
- **Dependencias**: `C-03`
- **Governance**: BAJO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §`sillones`, `prestaciones`, `disponibilidades_profesional`, `bloqueos_agenda` y Seed data inicial
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: Agenda, Prestaciones y Sillones (RN-AG)
  - `knowledge-base/06_funcionalidades.md` §US-001
  - `knowledge-base/10_preguntas_abiertas.md` §Preguntas abiertas del proyecto

---

## FASE 2 — Pacientes y Agenda Multi-profesional sin Solapamientos

> `C-04` y `C-05` pueden ejecutarse en paralelo luego de `C-03`. Ambos convergen en `C-06`.

### [C-05] `pacientes-coberturas`
- **Estado**: `[ ]` pendiente
- **Scope**: Ficha administrativa del paciente, consentimiento WhatsApp y cobertura informativa de obra social (`US-010`)
  - Modelos: `Paciente`, `ObraSocial`, `PacienteCobertura`
  - Migración `004_pacientes_coberturas.py`: tablas `pacientes`, `obras_sociales` (`cupo_mensual_referencia` meramente informativo `RN-OS-01`), `paciente_coberturas`; constraint `UNIQUE(consultorio_id, dni)` parcial (`dni IS NOT NULL`) e índices por `(consultorio_id, apellido, nombre)` y `(consultorio_id, telefono_whatsapp)`
  - Seed de obra social genérica: `Particular / Sin cobertura`
  - Endpoints: `GET/POST /api/v1/pacientes` (búsqueda rápida por apellido, nombre, DNI o teléfono), `GET/PATCH /api/v1/pacientes/{id}`, `PATCH /api/v1/pacientes/{id}/opt-in-whatsapp` (registra `opt_in_whatsapp` y `opt_in_whatsapp_at`), `GET/POST/PATCH /api/v1/obras-sociales`, `POST/PATCH /api/v1/pacientes/{id}/coberturas`
  - Riesgo / pendiente (`IN-02`, `10_preguntas_abiertas.md`): obras sociales prioritarias y valores de `cupo_mensual_referencia` a confirmar con administración (siempre sin bloqueo automático en v1)
  - Tests: búsqueda multi-campo, unicidad de DNI por consultorio, trazabilidad temporal de opt-in/baja de WhatsApp, aislamiento de datos clínicos (sin acceso a historias clínicas)
- **Dependencias**: `C-03`
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §RBAC — Matriz de permisos
  - `knowledge-base/04_modelo_de_datos.md` §`pacientes`, `obras_sociales` y `paciente_coberturas`
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: WhatsApp y Notificaciones (RN-WA) y RN-OS-01
  - `knowledge-base/06_funcionalidades.md` §US-010
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-07

---

### [C-06] `turnos-agenda`
- **Estado**: `[x]` slice nuclear implementado y archivado (`openspec/changes/archive/2026-11-23-crear-turno-sin-solapamientos/`) — *Nota: completada la funcionalidad atómica `POST /api/v1/turnos` y prevención de solapamientos (`RN-AG-01`..`05`, `RN-AU-01`, `RN-AU-05`) con DDL `btree_gist` y 9 tests en verde (100 % cobertura). Restan `GET /turnos`, `GET /disponibilidad`, `PATCH /reprogramar` y `PATCH /estado` en iteraciones posteriores.*
- **Scope**: Gestión interna de turnos con prevención transaccional de solapamientos por profesional y sillón/box (`US-003`, `US-004`, `US-005`)
  - Modelo `Turno` con `estado` (`reservado`, `confirmado`, `en_atencion`, `atendido`, `ausente`, `cancelado`), `origen` (`interno`, `publico`), `token_publico_hash`, `profesional_id`, `sillon_id`, `prestacion_id`, `paciente_id`
  - Migración `005_turnos_agenda.py`: tabla `turnos` con `CHECK (fin > inicio)`, `CHECK (duracion_minutos > 0)`, índice `(consultorio_id, inicio, estado)` y **exclusion constraints `EXCLUDE USING gist`** (`WHERE (estado <> 'cancelado')`) sobre `(consultorio_id, profesional_id, tstzrange(inicio, fin, '[)'))` (`RN-AG-03`) y `(consultorio_id, sillon_id, tstzrange(inicio, fin, '[)'))` (`RN-AG-04`)
  - Endpoints internos:
    - `GET /api/v1/turnos` — filtrado por rango de fechas, profesional, sillón y estado (incluye indicador informativo de cupo de obra social `RN-OS-01`)
    - `GET /api/v1/disponibilidad` — cálculo de slots libres cruzando `disponibilidades_profesional`, `bloqueos_agenda` y turnos activos
    - `POST /api/v1/turnos` — cálculo automático de `fin` por prestación (`RN-AG-01`, duración ajustable en agenda interna), asignación obligatoria de `sillon_id` (`RN-AG-02`), validación de bloqueos y sobrecarga interna permitida solo a `recepcion`/`dueno` (`RN-AG-05`), token público opaco hasheado
    - `PATCH /api/v1/turnos/{id}/reprogramar` — mantiene `id`, valida solapamientos/bloqueos y prohíbe reprogramar `atendido`/`ausente`/`cancelado` (`RN-AG-08`)
    - `PATCH /api/v1/turnos/{id}/estado` — máquina de estados estricta (`RN-AG-07`), cancelación libera profesional y sillón
  - Emisión de eventos de dominio (`TurnoCreado`, `TurnoReprogramado`, `TurnoEstadoCambiado`) vía `shared/events.py` (para desacoplar `C-09` Google Calendar sin acoplar la transacción de turnos), manejo de `IntegrityError` (`23P01`) retornando `409 Conflict` con detalle del recurso en conflicto (profesional vs sillón) y registro en `auditoria_eventos` (`RN-AU-05`)
  - Riesgo / pendiente (`SU-03`): confirmar con el consultorio piloto si algún odontólogo alterna dos sillones simultáneos con asistente o rige siempre exclusión 1:1
  - Tests: solapamiento por profesional (`409`), solapamiento por sillón entre profesionales distintos (`409`), concurrencia paralela sobre el mismo slot, colisión con `bloqueo_agenda`, máquina de estados completa, liberación al cancelar y auditoría
- **Dependencias**: `C-04, C-05`
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §`turnos`
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: Agenda, Prestaciones y Sillones (RN-AG), RN-OS-01 y RN-AU-05
  - `knowledge-base/06_funcionalidades.md` §US-003, US-004, US-005
  - `knowledge-base/07_flujos_principales.md` §Flujo 3
  - `knowledge-base/09_decisiones_y_supuestos.md` §SU-03

---

## FASE 3 — Reserva Online, WhatsApp Asistido y Google Calendar

> Completado `C-06`, pueden ejecutarse en paralelo `C-07`, `C-08`, `C-10` y `C-17` (con sus requisitos previos). `C-09` se conecta al bus de eventos de `C-06` y `C-07`.

### [C-07] `public-booking`
- **Estado**: `[ ]` pendiente
- **Scope**: Endpoints públicos de reserva online y autogestión por token de turno (`US-006`, `US-007`)
  - `GET /api/v1/public/{slug}/catalogo` — prestaciones activas con `visible_publico = true` y profesionales activos (sin datos internos de sillones ni pacientes)
  - `GET /api/v1/public/{slug}/disponibilidad` — slots libres dentro de `disponibilidades_profesional` donde exista al menos un sillón libre durante `prestacion.duracion_minutos` (`RN-AG-02`, `RN-AG-05`, sin sobrecarga)
  - `POST /api/v1/public/{slug}/reservas` — transacción que busca/crea paciente por `(consultorio_id, dni)`, guarda `opt_in_whatsapp`, auto-asigna sillón libre priorizando `sillon_preferido_id`, crea turno `reservado` (`origen = 'publico'`), genera token opaco (≥32 bytes) y retorna `/turno/{token}`; rate limiting por IP
  - `GET /api/v1/public/turnos/{token}` — vista acotada al turno propio (`RN-AU-04`)
  - `POST /api/v1/public/turnos/{token}/confirmar` — pasa a `confirmado` y registra auditoría
  - `POST /api/v1/public/turnos/{token}/cancelar` — valida `anticipacion_minima_cancelacion_hs` (`RN-AG-06`); si no cumple, responde `422` con el teléfono del consultorio
  - Emisión de los mismos eventos de dominio de turno (`TurnoCreado`, `TurnoEstadoCambiado`) vía `shared/events.py` al reservar, confirmar y cancelar para que `C-09` sincronice con Google Calendar
  - Tests: reserva concurrente (`409`), asignación de sillón preferido/libre, rechazo de cancelación tardía (`422`), token inválido/expirado (`404`/`410`), rate limiting y verificación de no exposición de datos de terceros
- **Dependencias**: `C-06`
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §Rutas públicas (sin autenticación de usuario)
  - `knowledge-base/05_reglas_de_negocio.md` §RN-AU-04 y Dominio: Agenda, Prestaciones y Sillones (RN-AG)
  - `knowledge-base/06_funcionalidades.md` §US-006, US-007
  - `knowledge-base/07_flujos_principales.md` §Flujo 1 y Flujo 2

---

### [C-08] `whatsapp-reminders`
- **Estado**: `[ ]` pendiente
- **Scope**: Adaptador de recordatorios asistidos por WhatsApp mediante link `wa.me` en 1 clic (`US-008`, `DD-02`)
  - Puerto + adaptador `infrastructure/integrations/whatsapp_links.py` (desacoplado para permitir Meta WhatsApp API en v1.1 sin alterar reglas de negocio)
  - `GET /api/v1/turnos/{id}/whatsapp-link` — valida `paciente.opt_in_whatsapp = true` (`RN-WA-01`), normaliza teléfono y arma URL `https://wa.me/{telefono}?text={mensaje_codificado}` con paciente, fecha/hora local, profesional y URL `${PUBLIC_BASE_URL}/turno/{token}` (`RN-WA-02`)
  - Respuesta explícita cuando `opt_in_whatsapp = false` impidiendo el envío directo
  - Tests: formato y URL-encoding del link `wa.me`, bloqueo/advertencia ante `opt_in_whatsapp = false`, normalización telefónica AR, RBAC (`recepcion`, `odontologo`, `dueno`)
- **Dependencias**: `C-06`
- **Governance**: BAJO
- **Leer antes**:
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: WhatsApp y Notificaciones (RN-WA)
  - `knowledge-base/06_funcionalidades.md` §US-008
  - `knowledge-base/07_flujos_principales.md` §Flujo 2
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-02

---

### [C-09] `google-calendar-sync`
- **Estado**: `[ ]` pendiente
- **Scope**: Integración OAuth 2.0 y sincronización unidireccional `Sistema → Google Calendar` para turnos internos y públicos (`US-009`, `DD-05`)
  - Modelos: `IntegracionGoogleCalendar`, `GoogleCalendarSyncEvent`
  - Migración `006_google_calendar_sync.py`: tablas `integraciones_google_calendar` y `google_calendar_sync_events` (`estado_sync`: `pendiente`, `sincronizado`, `error`, `eliminado`)
  - Cifrado simétrico en reposo (`Fernet` / AES-GCM con `ENCRYPTION_KEY`) para `access_token_enc` y `refresh_token_enc`
  - Endpoints OAuth (`odontologo`): `POST /api/v1/integraciones/google/connect`, `GET /api/v1/integraciones/google/callback` (validación estricta de `state` firmado), `DELETE /api/v1/integraciones/google/disconnect`, `GET /api/v1/integraciones/google/status`
  - Adaptador Google Calendar API v3 + suscriptor de eventos de dominio (`C-06` y `C-07`) + worker ligero de reintentos + `POST /api/v1/turnos/{id}/google-sync/reintentar` para crear, actualizar y eliminar eventos ante alta/confirmación/reprogramación/cancelación (`RN-GC-01`)
  - Resiliencia y privacidad: errores de Google no abortan la transacción de turnos (`RN-GC-02`); el evento externo no contiene diagnósticos ni historia clínica (`RN-GC-03`)
  - Riesgo / pendiente (`10_preguntas_abiertas.md`): definir cuenta de Google Cloud y verificación de la app OAuth en producción para evitar límite de usuarios/expiración de tokens en modo Testing
  - Tests: validación de `state` OAuth, cifrado de tokens, sync mockeado crear/actualizar/eliminar desde turnos internos y públicos, resiliencia ante fallo de API externa, verificación de privacidad del título del evento
- **Dependencias**: `C-06, C-07`
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §`integraciones_google_calendar` y `google_calendar_sync_events`
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: Integración Google Calendar (RN-GC)
  - `knowledge-base/06_funcionalidades.md` §US-009
  - `knowledge-base/08_arquitectura_propuesta.md` §Seguridad y Residencia de Datos en Argentina
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-05 y `knowledge-base/10_preguntas_abiertas.md` §Preguntas abiertas del proyecto

---

## FASE 4 — Clínica Odontológica, Presupuestos, Pagos y Exportaciones

### [C-10] `clinica-odontograma`
- **Estado**: `[ ]` pendiente
- **Scope**: Historia clínica, odontograma versionado por pieza/cara y planes de tratamiento exclusivos para `odontologo` (`US-011`, `US-012`)
  - Modelos: `HistoriaClinica`, `Odontograma`, `PlanTratamiento`
  - Migración `007_clinica_odontograma.py`: tablas `historias_clinicas`, `odontogramas` (`UNIQUE(paciente_id, version)`, `piezas_json` JSONB FDI `11..48`/`51..85` y caras `V/L/M/D/O`), `planes_tratamiento`
  - Endpoints protegidos obligatoriamente con `require_odontologo()` (`RN-AU-02`, `DD-06`):
    - `GET/POST /api/v1/pacientes/{id}/historia-clinica` (asociación opcional a `turno_id`, sin borrado físico `RN-AU-03`)
    - `GET/PUT /api/v1/pacientes/{id}/odontograma` y `GET /api/v1/pacientes/{id}/odontograma/historial` (cada actualización confirmada genera `version = N + 1` inmutable `RN-CL-01`)
    - `GET/POST/PATCH /api/v1/pacientes/{id}/planes-tratamiento`
  - Registro obligatorio en `auditoria_eventos` (`RN-AU-05`)
  - Riesgo / pendiente (`10_preguntas_abiertas.md`): confirmar con el odontólogo la lista cerrada de estados de pieza/cara en `piezas_json` (sano, caries, obturado, ausente, corona, endodoncia, implante, a realizar)
  - Tests: `403 Forbidden` para `dueno` sin rol `odontologo`, `recepcion` y `administracion`; acceso válido para `odontologo` y `dueno`+`odontologo`; inmutabilidad y versionado incremental del odontograma; auditoría
- **Dependencias**: `C-05, C-06`
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §Regla crítica de privacidad clínica
  - `knowledge-base/04_modelo_de_datos.md` §`historias_clinicas`, `odontogramas`, `planes_tratamiento`
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: Autenticación y Privacidad Clínica (RN-AU), RN-CL-01 y RN-AU-05
  - `knowledge-base/06_funcionalidades.md` §US-011, US-012
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-06 y `knowledge-base/10_preguntas_abiertas.md` §Preguntas abiertas del proyecto

---

### [C-11] `presupuestos-versionados`
- **Estado**: `[ ]` pendiente
- **Scope**: Presupuestos odontológicos en ARS con ítems por prestación/pieza y trazabilidad de versiones (`US-012`)
  - Modelos: `Presupuesto`, `PresupuestoItem`
  - Migración `008_presupuestos.py`: tablas `presupuestos` (`version`, `presupuesto_padre_id`, `estado` ENUM `borrador`/`emitido`/`aceptado`/`rechazado`/`reemplazado`, `total_ars`, `aceptado_por_paciente_at`) y `presupuesto_items` (`prestacion_id`, `pieza_dental`, `cantidad`, `precio_unitario_ars`, `subtotal_ars`)
  - Endpoints: `GET/POST /api/v1/presupuestos`, `GET /api/v1/presupuestos/{id}`, `PATCH /api/v1/presupuestos/{id}/estado`, `POST /api/v1/presupuestos/{id}/versiones` (al editar un presupuesto `emitido`/`aceptado`, marca el anterior `reemplazado` y crea versión `N + 1` vinculada por `presupuesto_padre_id` `RN-CL-01`)
  - RBAC: creación/emisión/re-versionado por `odontologo`; lectura de resumen económico para `dueno`, `administracion` y `recepcion`; registro en `auditoria_eventos` (`RN-AU-05`)
  - Tests: cálculo de subtotales/totales en ARS, re-versionado enlazado y estado `reemplazado`, RBAC por rol, auditoría
- **Dependencias**: `C-04, C-10`
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §RBAC — Matriz de permisos
  - `knowledge-base/04_modelo_de_datos.md` §`presupuestos` y `presupuesto_items`
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: Clínica, Presupuestos, Pagos y Obras Sociales (RN-CL / RN-PG)
  - `knowledge-base/06_funcionalidades.md` §US-012

---

### [C-12] `pagos-manuales`
- **Estado**: `[ ]` pendiente
- **Scope**: Registro manual de señas y pagos con inmutabilidad contable y anulación auditada (`US-013`, `DD-03`)
  - Modelo `Pago` (`tipo`: `sena`/`pago_parcial`/`pago_total`, `medio_pago`, `monto_ars > 0`, `fecha_pago`, `referencia_comprobante`, `estado`: `registrado`/`anulado`, `motivo_anulacion`, `registrado_por_usuario_id`)
  - Migración `009_pagos.py`: tabla `pagos` con `CHECK (monto_ars > 0)` y vínculos opcionales a `turnos` y `presupuestos`
  - Endpoints:
    - `POST /api/v1/pagos` — registro manual alineado a `03_actores_y_roles.md` §RBAC: `recepcion` registra señas (`tipo = 'sena'`) y `administracion` registra señas y pagos parciales/totales recalculando saldo pendiente (`RN-PG-01`)
    - `GET /api/v1/pagos` y `GET /api/v1/pacientes/{id}/cuenta-corriente` — resumen financiero y saldo pendiente (`dueno`, `administracion`, `recepcion`)
    - `PATCH /api/v1/pagos/{id}/anular` — exclusivo `administracion` o `dueno` (`RN-PG-02`, `US-013`) con `motivo_anulacion` obligatorio; sin `DELETE` ni edición de monto
  - Registro obligatorio en `auditoria_eventos` (`RN-AU-05`)
  - Tests: registro de seña por `recepcion` (rechaza `pago_total` por `recepcion` o `POST` por `dueno` sin rol operativo/admin), pago parcial/total sobre presupuesto y recálculo de saldo, prohibición de editar monto o borrar, anulación por `administracion`/`dueno` con motivo obligatorio, auditoría
- **Dependencias**: `C-06, C-11`
- **Governance**: CRITICO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §RBAC — Matriz de permisos
  - `knowledge-base/04_modelo_de_datos.md` §`pagos`
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: Clínica, Presupuestos, Pagos y Obras Sociales (RN-CL / RN-PG)
  - `knowledge-base/06_funcionalidades.md` §US-013
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-03

---

### [C-13] `exportaciones-reportes`
- **Estado**: `[ ]` pendiente
- **Scope**: Exportación CSV/PDF para facturación externa ARCA y obras sociales, reportes operativos básicos y visor de auditoría (`US-014`, `DD-07`)
  - Endpoints de exportación (`administracion` y `dueno`):
    - `GET /api/v1/exportaciones/pagos` y `GET /api/v1/exportaciones/turnos` (`formato=csv|pdf`), filtrables por rango de fechas, profesional y obra social (excluyendo todo dato clínico)
    - Sanitización anti-CSV-injection en celdas que comiencen con `=`, `+`, `-`, `@`
  - Endpoints operativos y de auditoría:
    - `GET /api/v1/reportes/ocupacion` — tasa de ocupación por profesional/sillón, cantidad de turnos atendidos, cancelados y ausentes, total cobrado en el período
    - `GET /api/v1/auditoria` — visor paginado de `auditoria_eventos` filtrable por entidad, usuario y fecha (`dueno`, y eventos financieros para `administracion`)
  - Riesgo / pendiente (`SU-02`, `10_preguntas_abiertas.md`): confirmar columnas exactas de CSV/PDF requeridas por administración/contador para carga en ARCA y liquidación de obras sociales
  - Tests: generación CSV sanitizada y PDF sin datos clínicos, cálculo correcto de métricas de ocupación/ausentismo/cobranzas, RBAC estricto por rol
- **Dependencias**: `C-12`
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §RBAC — Matriz de permisos
  - `knowledge-base/06_funcionalidades.md` §US-014
  - `knowledge-base/07_flujos_principales.md` §Flujo 5
  - `knowledge-base/08_arquitectura_propuesta.md` §Seguridad y Residencia de Datos en Argentina
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-07, SU-02 y `knowledge-base/10_preguntas_abiertas.md`

---

## FASE 5 — Frontend PWA (Shell, Reserva Pública, Agenda, Pacientes, Clínica y Caja)

> Las pantallas frontend consumen exclusivamente los endpoints de las fases 1–4 y respetan `DD-06` (ocultar y bloquear clínica sin rol `odontologo`).

### [C-14] `frontend-shell-config`
- **Estado**: `[ ]` pendiente
- **Scope**: Shell PWA responsive, contexto de autenticación/RBAC y pantallas de configuración del consultorio (`US-001`, `US-002`)
  - `src/app/`: router con guards de autenticación y rol, `AuthContext` (login, refresh transparente ante `401`, logout), layout responsive PWA (barra lateral en escritorio / navegación inferior en móvil)
  - `src/features/config/` (visible según rol `dueno`): configuración del consultorio (`anticipacion_minima_cancelacion_hs`, teléfono WhatsApp), gestión de usuarios y roles (incluyendo `dueno`+`odontologo`), ABM de sillones/boxes, ABM de prestaciones y duración, horarios semanales y bloqueos de agenda
  - Verificación: typecheck `tsc --noEmit`, `vite build`, tests de guards por rol y flujos de login/configuración
- **Dependencias**: `C-03, C-04`
- **Governance**: BAJO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §Actores del sistema y RBAC — Matriz de permisos
  - `knowledge-base/06_funcionalidades.md` §US-001, US-002
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios propuesta
  - `knowledge-base/09_decisiones_y_supuestos.md` §SU-01

---

### [C-15] `frontend-public-booking`
- **Estado**: `[ ]` pendiente
- **Scope**: Flujo público mobile-first de reserva online y confirmación/cancelación por token (`US-006`, `US-007`)
  - `src/features/public-booking/` (sin autenticación):
    - `/reservar/:slug`: selección de prestación pública, profesional (o cualquier disponible), fecha/slot disponible, formulario de datos (`nombre`, `apellido`, `dni`, `telefono_whatsapp`, checkbox `opt_in_whatsapp`), pantalla de confirmación con enlace `/turno/:token` y recarga automática de slots ante error `409`
    - `/turno/:token`: detalle del turno, botones **Confirmar asistencia** y **Cancelar turno** con manejo explícito del bloqueo `422` por anticipación mínima mostrando el teléfono del consultorio
  - Riesgo / seguimiento (`SU-04`): instrumentar claramente flujo mobile-first y enlace `/turno/:token` compartible por WhatsApp para validar adopción de pacientes en piloto
  - Verificación: tests de flujo de reserva, manejo de `409` y `422`, layout mobile-first y build sin errores
- **Dependencias**: `C-01, C-07`
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §Rutas públicas (sin autenticación de usuario)
  - `knowledge-base/06_funcionalidades.md` §US-006, US-007
  - `knowledge-base/07_flujos_principales.md` §Flujo 1 y Flujo 2
  - `knowledge-base/09_decisiones_y_supuestos.md` §SU-01, SU-04

---

### [C-16] `frontend-agenda`
- **Estado**: `[ ]` pendiente
- **Scope**: Grilla de agenda día/semana por profesional y sillón, recordatorios `wa.me` y conexión Google Calendar (`US-003`, `US-004`, `US-005`, `US-008`, `US-009`)
  - `src/features/agenda/`:
    - Vista diaria y semanal con colores por estado, alternable por columnas de **profesionales** o **sillones/boxes**, y vista móvil rápida para odontólogo
    - Modal de creación y reprogramación de turno: cálculo automático de duración por prestación (editable internamente), alerta informativa de obra social (`RN-OS-01`), mensajes claros de conflicto `409` (profesional vs sillón)
    - Acciones de cambio de estado, botón **Enviar recordatorio WhatsApp (`wa.me`)** en 1 clic con advertencia si `opt_in_whatsapp = false`
    - Panel en perfil profesional para conectar/desconectar Google Calendar (OAuth 2.0), ver estado de sincronización del turno y disparar reintento manual
  - Verificación: tests de componentes/flujos de agenda, alternancia profesional/sillón, manejo de `409` y validación visual de opt-in `wa.me`
- **Dependencias**: `C-06, C-08, C-09, C-14`
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-003, US-004, US-005, US-008, US-009
  - `knowledge-base/07_flujos_principales.md` §Flujo 2 y Flujo 3
  - `knowledge-base/08_arquitectura_propuesta.md` §Patrones aplicados y Estructura de directorios propuesta

---

### [C-17] `frontend-pacientes`
- **Estado**: `[ ]` pendiente
- **Scope**: Gestión administrativa de pacientes, catálogo de obras sociales e historial básico de turnos (`US-010`)
  - `src/features/pacientes/` (accesible para `recepcion`, `administracion`, `dueno` y `odontologo` según RBAC, sin exponer datos clínicos):
    - Buscador rápido por apellido, nombre, DNI o teléfono; alta y edición administrativa de ficha
    - Gestión de consentimiento `opt_in_whatsapp` y asignación de coberturas del paciente (obra social, plan, número de afiliado)
    - ABM de catálogo de `obras_sociales` (`codigo_rnos`, `cupo_mensual_referencia` informativo `RN-OS-01`)
    - Historial básico de turnos del paciente (consumiendo `GET /api/v1/turnos?paciente_id=...`) y slot extensible para resumen de cuenta corriente (integrado en `C-19`)
  - Verificación: tests de búsqueda multi-campo, carga de cobertura y opt-in, ABM de obras sociales y verificación de no exposición clínica
- **Dependencias**: `C-05, C-06, C-14`
- **Governance**: BAJO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §RBAC — Matriz de permisos
  - `knowledge-base/05_reglas_de_negocio.md` §RN-WA-01, RN-OS-01
  - `knowledge-base/06_funcionalidades.md` §US-010
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios propuesta

---

### [C-18] `frontend-clinica`
- **Estado**: `[ ]` pendiente
- **Scope**: Módulo clínico confidencial con historia clínica, odontograma FDI interactivo y planes de tratamiento exclusivo para `odontologo` (`US-011`, `US-012`)
  - `src/features/clinica/` (habilitado **exclusivamente** cuando el usuario posee rol `odontologo`; oculto y bloqueado para `dueno` sin rol clínico, `recepcion` y `administracion` `DD-06`):
    - Pestaña/vista clínica dentro de la ficha del paciente (`C-17`): lectura y alta de evoluciones en historia clínica asociadas opcionalmente al turno activo
    - **Odontograma simple interactivo** (piezas FDI permanentes `11..48` y temporarias `51..85`, caras `V/L/M/D/O`) con selector de estado clínico y visor de historial de versiones inmutables (`version = N + 1`)
    - Creación y seguimiento de planes de tratamiento (`borrador`, `propuesto`, `en_curso`, `finalizado`, `cancelado`)
  - Verificación: tests de ocultamiento/bloqueo clínico para `dueno` sin `odontologo` y `recepcion`, alta de evolución clínica y generación de nueva versión de odontograma
- **Dependencias**: `C-10, C-14, C-17`
- **Governance**: ALTO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §Regla crítica de privacidad clínica
  - `knowledge-base/06_funcionalidades.md` §US-011, US-012
  - `knowledge-base/07_flujos_principales.md` §Flujo 4
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-06 y `knowledge-base/10_preguntas_abiertas.md`

---

### [C-19] `frontend-pagos-reportes`
- **Estado**: `[ ]` pendiente
- **Scope**: UI de presupuestos versionados, caja/señas manuales, saldo pendiente en ficha del paciente, exportaciones ARCA/OS y tablero operativo (`US-010` CA-3, `US-012`, `US-013`, `US-014`)
  - `src/features/pagos/`:
    - Presupuestos en ARS con ítems por prestación/pieza, emisión/aceptación y creación de nueva versión (`reemplazado`)
    - Registro manual de señas (`recepcion`/`administracion`) y pagos (`administracion`), widget de cuenta corriente y saldo pendiente integrado en la ficha del paciente (`C-17`), y modal de anulación con motivo obligatorio (`administracion`/`dueno`)
    - Pantalla de **Exportaciones** (filtros por fecha, profesional y obra social + descarga CSV/PDF para ARCA y obras sociales)
  - `src/features/reportes/`: tablero operativo básico para `dueno`/`administracion` (ocupación por profesional/sillón, atendidos/cancelados/ausentes, total cobrado) y visor paginado de `auditoria_eventos`
  - Verificación: tests de emisión/re-versionado de presupuesto, carga y anulación de pago con motivo, descarga de exportaciones, visualización de saldo en ficha del paciente y build limpio
- **Dependencias**: `C-11, C-12, C-13, C-14, C-17`
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/03_actores_y_roles.md` §RBAC — Matriz de permisos
  - `knowledge-base/06_funcionalidades.md` §US-010, US-012, US-013, US-014
  - `knowledge-base/07_flujos_principales.md` §Flujo 4 y Flujo 5
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios propuesta
