# Modelo de Datos

## Dominios

1. **Identidad y Consultorio**: organización piloto (`consultorios`), usuarios internos, roles, sillones/boxes y catálogo de prestaciones con duración base.
2. **Agenda y Turnos**: disponibilidad por profesional, turnos asignados a profesional y sillón/box, tokens públicos y cola de sincronización con Google Calendar.
3. **Pacientes y Coberturas**: datos personales, opt-in de WhatsApp y cobertura de obra social (informativa en v1).
4. **Clínica Odontológica**: historia clínica, odontograma versionado por pieza/cara y planes de tratamiento (acceso exclusivo de Odontólogo/a).
5. **Presupuestos y Pagos**: presupuestos versionados, ítems económicos y pagos/señas manuales.
6. **Auditoría**: registro append-only de cambios relevantes de negocio y accesos clínicos.

> **Convención transversal**: todas las tablas de negocio incluyen `consultorio_id` (FK a `consultorios.id`), `created_at` y `updated_at` en UTC (`TIMESTAMPTZ`), y usan borrado lógico (`deleted_at` o `activo`) para preservar trazabilidad clínica y contable.

---

## ERD (Entity Relationship Diagram)

```
CONSULTORIOS (1) ──< USUARIOS (N) ──< USUARIO_ROLES (N)
      │                    │
      │                    ├──< DISPONIBILIDADES_PROFESIONAL (N)
      │                    └──< INTEGRACIONES_GOOGLE_CALENDAR (0..1)
      │
      ├──< SILLONES (N)
      ├──< PRESTACIONES (N)
      ├──< OBRAS_SOCIALES (N)
      │
      ├──< PACIENTES (N) ──< PACIENTE_COBERTURAS (N) >── OBRAS_SOCIALES
      │        │
      │        ├──< HISTORIAS_CLINICAS (1..N evoluciones)
      │        ├──< ODONTOGRAMAS (1..N snapshots/versiones)
      │        ├──< PLANES_TRATAMIENTO (N)
      │        └──< PRESUPUESTOS (N) ──< PRESUPUESTO_ITEMS (N)
      │                 │
      │                 └──< PAGOS (N) >── TURNOS
      │
      └──< TURNOS (N) >── USUARIOS (profesional), SILLONES, PRESTACIONES, PACIENTES
               │
               └──< GOOGLE_CALENDAR_SYNC_EVENTS (0..1)

AUDITORIA_EVENTOS (append-only por consultorio_id y usuario_id)
```

---

## Entidades

### `consultorios`
- `id` (UUID, PK), `nombre` (VARCHAR 150), `slug` (VARCHAR 80, UNIQUE), `cuit` (VARCHAR 15, nullable), `direccion` (TEXT, nullable), `telefono_whatsapp` (VARCHAR 30), `anticipacion_minima_cancelacion_hs` (INT, default 24), `zona_horaria` (VARCHAR 50, default `'America/Argentina/Buenos_Aires'`), `activo` (BOOLEAN, default true).
- **Constraints**: `slug` único global.

### `usuarios` y `usuario_roles`
- `usuarios`: `id` (UUID, PK), `consultorio_id` (UUID, FK), `nombre_completo` (VARCHAR 150), `email` (VARCHAR 255), `password_hash` (TEXT), `matricula_profesional` (VARCHAR 50, nullable), `activo` (BOOLEAN, default true).
- `usuario_roles`: `id` (UUID, PK), `usuario_id` (UUID, FK), `rol` (ENUM: `'dueno'`, `'odontologo'`, `'recepcion'`, `'administracion'`).
- **Constraints**: `UNIQUE(consultorio_id, email)`, `UNIQUE(usuario_id, rol)`.

### `sillones` (boxes / consultorios físicos internos)
- `id` (UUID, PK), `consultorio_id` (UUID, FK), `nombre` (VARCHAR 80, ej. "Sillón 1"), `ubicacion` (VARCHAR 100, nullable), `activo` (BOOLEAN, default true).
- **Constraints**: `UNIQUE(consultorio_id, nombre)`.

### `prestaciones` (tipos de atención / servicios)
- `id` (UUID, PK), `consultorio_id` (UUID, FK), `nombre` (VARCHAR 120), `duracion_minutos` (INT, check `> 0` y múltiplo de 5 o 10), `precio_referencia_ars` (NUMERIC(12,2)), `requiere_sena` (BOOLEAN, default false), `monto_sena_sugerido_ars` (NUMERIC(12,2), nullable), `visible_publico` (BOOLEAN, default true), `activo` (BOOLEAN, default true).

### `disponibilidades_profesional` y `bloqueos_agenda`
- `disponibilidades_profesional`: `id` (UUID, PK), `consultorio_id` (UUID, FK), `profesional_id` (UUID, FK → `usuarios`), `dia_semana` (SMALLINT 0..6), `hora_inicio` (TIME), `hora_fin` (TIME), `sillon_preferido_id` (UUID, FK nullable → `sillones`), `activo` (BOOLEAN).
- `bloqueos_agenda`: `id` (UUID, PK), `consultorio_id` (UUID, FK), `profesional_id` (UUID, FK nullable), `sillon_id` (UUID, FK nullable), `inicio` (TIMESTAMPTZ), `fin` (TIMESTAMPTZ), `motivo` (VARCHAR 200).
- **Constraints**: `hora_fin > hora_inicio`, `fin > inicio`, al menos uno de `profesional_id` o `sillon_id` presente en `bloqueos_agenda`.

### `pacientes`, `obras_sociales` y `paciente_coberturas`
- `pacientes`: `id` (UUID, PK), `consultorio_id` (UUID, FK), `nombre` (VARCHAR 100), `apellido` (VARCHAR 100), `dni` (VARCHAR 20), `telefono_whatsapp` (VARCHAR 30), `email` (VARCHAR 255, nullable), `fecha_nacimiento` (DATE, nullable), `opt_in_whatsapp` (BOOLEAN, default false), `opt_in_whatsapp_at` (TIMESTAMPTZ, nullable), `notas_administrativas` (TEXT, nullable), `activo` (BOOLEAN, default true).
- `obras_sociales`: `id` (UUID, PK), `consultorio_id` (UUID, FK), `nombre` (VARCHAR 120), `codigo_rnos` (VARCHAR 30, nullable), `cupo_mensual_referencia` (INT, nullable — solo informativo en v1), `activo` (BOOLEAN).
- `paciente_coberturas`: `id` (UUID, PK), `consultorio_id` (UUID, FK), `paciente_id` (UUID, FK), `obra_social_id` (UUID, FK), `plan` (VARCHAR 80, nullable), `numero_afiliado` (VARCHAR 60), `es_principal` (BOOLEAN, default true).
- **Constraints**: `UNIQUE(consultorio_id, dni)` (cuando `dni` no es nulo), índice por `(consultorio_id, apellido, nombre)` y `(consultorio_id, telefono_whatsapp)`.

### `turnos`
- `id` (UUID, PK), `consultorio_id` (UUID, FK), `paciente_id` (UUID, FK), `profesional_id` (UUID, FK → `usuarios`), `sillon_id` (UUID, FK → `sillones`), `prestacion_id` (UUID, FK → `prestaciones`), `inicio` (TIMESTAMPTZ), `fin` (TIMESTAMPTZ), `duracion_minutos` (INT), `estado` (ENUM: `'reservado'`, `'confirmado'`, `'en_atencion'`, `'atendido'`, `'ausente'`, `'cancelado'`), `origen` (ENUM: `'interno'`, `'publico'`), `token_publico_hash` (VARCHAR 128, UNIQUE), `motivo_cancelacion` (TEXT, nullable), `cancelado_por` (VARCHAR 30, nullable), `observaciones_agenda` (TEXT, nullable), `creado_por_usuario_id` (UUID, FK nullable).
- **Constraints e Índices críticos**:
  - `CHECK (fin > inicio)` y `CHECK (duracion_minutos > 0)`.
  - **Exclusión de solapamientos (PostgreSQL `btree_gist`)**: para turnos con `estado != 'cancelado'`:
    - `EXCLUDE USING gist (consultorio_id WITH =, profesional_id WITH =, tstzrange(inicio, fin, '[)') WITH &&)`
    - `EXCLUDE USING gist (consultorio_id WITH =, sillon_id WITH =, tstzrange(inicio, fin, '[)') WITH &&)`
  - Índice por `(consultorio_id, inicio, estado)`.

### `historias_clinicas` y `odontogramas` *(acceso exclusivo Odontólogo/a)*
- `historias_clinicas`: `id` (UUID, PK), `consultorio_id` (UUID, FK), `paciente_id` (UUID, FK), `turno_id` (UUID, FK nullable), `odontologo_id` (UUID, FK → `usuarios`), `fecha_atencion` (TIMESTAMPTZ), `motivo_consulta` (TEXT), `anamnesis_antecedentes` (TEXT, nullable), `diagnostico` (TEXT, nullable), `evolucion` (TEXT), `version` (INT, default 1).
- `odontogramas`: `id` (UUID, PK), `consultorio_id` (UUID, FK), `paciente_id` (UUID, FK), `odontologo_id` (UUID, FK → `usuarios`), `version` (INT), `piezas_json` (JSONB — mapa por pieza FDI 11..48 / 51..85 y caras V/L/M/D/O con estado clínico), `notas_generales` (TEXT, nullable).
- **Constraints**: `UNIQUE(paciente_id, version)` en `odontogramas`. No se borran versiones anteriores (trazabilidad clínica).

### `planes_tratamiento`, `presupuestos` y `presupuesto_items`
- `planes_tratamiento`: `id` (UUID, PK), `consultorio_id` (UUID, FK), `paciente_id` (UUID, FK), `odontologo_id` (UUID, FK), `titulo` (VARCHAR 150), `estado` (ENUM: `'borrador'`, `'propuesto'`, `'en_curso'`, `'finalizado'`, `'cancelado'`).
- `presupuestos`: `id` (UUID, PK), `consultorio_id` (UUID, FK), `paciente_id` (UUID, FK), `plan_tratamiento_id` (UUID, FK nullable), `odontologo_id` (UUID, FK), `version` (INT, default 1), `presupuesto_padre_id` (UUID, FK nullable — trazabilidad de re-versionado), `estado` (ENUM: `'borrador'`, `'emitido'`, `'aceptado'`, `'rechazado'`, `'reemplazado'`), `total_ars` (NUMERIC(12,2)), `aceptado_por_paciente_at` (TIMESTAMPTZ, nullable), `observaciones` (TEXT, nullable).
- `presupuesto_items`: `id` (UUID, PK), `presupuesto_id` (UUID, FK), `prestacion_id` (UUID, FK), `pieza_dental` (VARCHAR 10, nullable), `cantidad` (INT, default 1), `precio_unitario_ars` (NUMERIC(12,2)), `subtotal_ars` (NUMERIC(12,2)).

### `pagos` (señas y pagos manuales en v1)
- `id` (UUID, PK), `consultorio_id` (UUID, FK), `paciente_id` (UUID, FK), `turno_id` (UUID, FK nullable), `presupuesto_id` (UUID, FK nullable), `tipo` (ENUM: `'sena'`, `'pago_parcial'`, `'pago_total'`), `medio_pago` (ENUM: `'efectivo'`, `'transferencia'`, `'tarjeta_debito'`, `'tarjeta_credito'`, `'otro'`), `monto_ars` (NUMERIC(12,2), `> 0`), `fecha_pago` (TIMESTAMPTZ), `referencia_comprobante` (VARCHAR 100, nullable), `estado` (ENUM: `'registrado'`, `'anulado'`), `motivo_anulacion` (TEXT, nullable), `registrado_por_usuario_id` (UUID, FK).

### `integraciones_google_calendar` y `google_calendar_sync_events`
- `integraciones_google_calendar`: `id` (UUID, PK), `consultorio_id` (UUID, FK), `usuario_id` (UUID, FK UNIQUE — odontólogo), `calendar_id` (VARCHAR 255, default `'primary'`), `access_token_enc` (TEXT), `refresh_token_enc` (TEXT), `token_expira_at` (TIMESTAMPTZ), `activa` (BOOLEAN, default true).
- `google_calendar_sync_events`: `id` (UUID, PK), `consultorio_id` (UUID, FK), `turno_id` (UUID, FK UNIQUE), `google_event_id` (VARCHAR 255), `estado_sync` (ENUM: `'pendiente'`, `'sincronizado'`, `'error'`, `'eliminado'`), `ultimo_intento_at` (TIMESTAMPTZ), `reintentos` (INT, default 0), `ultimo_error` (TEXT, nullable).

### `auditoria_eventos`
- `id` (UUID, PK), `consultorio_id` (UUID, FK), `usuario_id` (UUID, FK nullable), `rol_activo` (VARCHAR 40, nullable), `entidad` (VARCHAR 60), `entidad_id` (UUID), `accion` (VARCHAR 40, ej. `crear`, `reprogramar`, `cancelar`, `anular_pago`, `actualizar_odontograma`), `detalle_json` (JSONB), `ip_origen` (VARCHAR 45, nullable), `created_at` (TIMESTAMPTZ).

---

## Seed data inicial

Al inicializar el consultorio piloto en la base de datos:
1. **1 consultorio piloto** (`slug: "consultorio-piloto"`, `zona_horaria: "America/Argentina/Buenos_Aires"`, `anticipacion_minima_cancelacion_hs: 24`).
2. **1 usuario inicial** con rol `dueno` (y opción de añadir `odontologo` si atiende) para completar la configuración inicial.
3. **2 sillones base** (`Sillón 1`, `Sillón 2`) editables por el dueño.
4. **Catálogo base de prestaciones odontológicas** con duración estándar:
   - Consulta / Diagnóstico inicial (30 min)
   - Limpieza / Profilaxis (40 min)
   - Obturación / Arreglo simple (45 min)
   - Endodoncia / Conducto (60 min)
   - Extracción simple (45 min)
   - Control post-operatorio (20 min)
5. **1 obra social genérica** (`Particular / Sin cobertura`) para agilizar altas rápidas.
