# Arquitectura Propuesta

## Patrones aplicados

| Patrón | Dónde se usa | Por qué |
|---|---|---|
| **Monolito Modular (Clean / Hexagonal pragmática)** | `backend/app/modules/*` | Mantiene bajo costo de despliegue en v1 evitando microservicios, pero separa dominio clínico, agenda y adaptadores externos |
| **Ports & Adapters (Adaptadores de Integración)** | `infrastructure/integrations/` (Google Calendar, WhatsApp Link, Export CSV/PDF) | Permite cambiar `wa.me` por Meta WhatsApp API o agregar Mercado Pago en v1.1 sin tocar las reglas de negocio |
| **Transacciones ACID + Exclusion Constraints (`btree_gist`)** | Tabla `turnos` en PostgreSQL | Garantiza 0 solapamientos por profesional y por sillón/box incluso bajo reservas concurrentes |
| **RBAC basado en dependencias FastAPI** | `api/dependencies/auth.py` | Centraliza la verificación de `consultorio_id` y exige explícitamente rol `odontologo` en todo recurso clínico |
| **Append-Only Audit & Versioning** | `auditoria_eventos`, `odontogramas`, `presupuestos`, `pagos` | Prioriza mantenibilidad y trazabilidad clínica/financiera evitando borrados destructivos |
| **Feature-based Architecture** | `frontend/src/features/*` | Agrupa UI, hooks y tipos por módulo funcional (`agenda`, `public-booking`, `clinica`, `pagos`, `config`) |

---

## Estructura de directorios propuesta

```
turnos-odontologia/
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── alembic/
│   │   └── versions/
│   └── app/
│       ├── main.py
│       ├── core/                   # config, security (JWT/argon2), crypto (tokens OAuth), db
│       ├── shared/                 # audit_logger, pagination, exceptions
│       └── modules/
│           ├── auth/               # login, refresh, rbac dependencies
│           ├── consultorio/        # consultorio, sillones, prestaciones, horarios, obras_sociales
│           ├── agenda/             # turnos, disponibilidad, bloqueos, reserva pública
│           ├── pacientes/          # ficha administrativa, coberturas, opt-in WA
│           ├── clinica/            # historias_clinicas, odontogramas, planes_tratamiento (solo odontologo)
│           ├── pagos/              # presupuestos versionados, pagos manuales, exportaciones CSV/PDF
│           └── integraciones/      # google_calendar (OAuth + sync worker), whatsapp_links
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.ts              # configuración PWA responsive + proxy API
    └── src/
        ├── app/                    # router, auth context, layout protegido
        ├── shared/                 # api client, UI components, date/currency formatters (ARS)
        └── features/
            ├── agenda/             # grilla día/semana por profesional y sillón
            ├── public-booking/     # /reservar/:slug y /turno/:token
            ├── pacientes/          # listado, ficha administrativa, cobertura
            ├── clinica/            # evolución clínica, odontograma interactivo, planes
            ├── pagos/              # presupuestos, caja/señas, exportaciones CSV/PDF
            ├── reportes/           # ocupación, ausentismo, auditoría (dueño)
            └── config/             # usuarios/roles, sillones, prestaciones, Google Calendar
```

---

## Seguridad y Residencia de Datos en Argentina

- **Residencia de datos en Argentina (consideración operativa obligatoria)**:
  - La instancia de **PostgreSQL** (datos identificatorios de pacientes, historia clínica, odontograma y pagos), el almacenamiento de backups cifrados y el backend deben desplegarse en un **VPS o proveedor cloud con datacenter ubicado físicamente en Argentina** (ej. Buenos Aires — DonWeb Cloud, WNPower, Iplan, Telecom/Arsat u otro proveedor local evaluado por presupuesto).
  - La única salida de datos hacia infraestructura externa en v1 es **Google Calendar API**, donde por regla `RN-GC-03` **se prohíbe enviar diagnósticos, evoluciones ni datos clínicos** (solo horario, prestación y referencia mínima del turno).
  - Backups diarios automatizados (`pg_dump` cifrado con GPG/age) retenidos en almacenamiento ubicado también en Argentina.
- **Autenticación**: JWT de acceso de vida corta (15–30 min) + refresh token rotativo en cookie `HttpOnly`, `Secure`, `SameSite=Lax`. Contraseñas hasheadas con **Argon2id** (`passlib` / `argon2-cffi`).
- **Autorización**:
  - Middleware/dependencia que extrae `usuario_id`, `consultorio_id` y lista de `roles` del token validado contra BD (para reflejar bajas inmediatas).
  - Guard estricto `require_roles("odontologo")` en todo endpoint clínico (`historia-clinica`, `odontograma`, `planes-tratamiento`).
- **Validación de input y anti-abuso**: schemas estrictos con Pydantic v2, sanitización de outputs en exportaciones CSV (prevención de CSV injection en celdas que inicien con `=`, `+`, `-`, `@`), y rate limiting en `/login` y rutas públicas `/public/*`.
- **Secrets management**: tokens OAuth de Google Calendar (`access_token`, `refresh_token`) encriptados en reposo con `Fernet` / AES-GCM usando `ENCRYPTION_KEY` inyectada por variables de entorno del servidor (nunca versionadas en git).

---

## Variables de entorno

| Variable | Descripción | Ejemplo | Sensible (Y/N) |
|---|---|---|---|
| `APP_ENV` | Entorno de ejecución | `production` | N |
| `DATABASE_URL` | URI de conexión PostgreSQL | `postgresql+asyncpg://user:pass@db:5432/odontologia` | Y |
| `JWT_SECRET_KEY` | Clave de firma para tokens JWT | `change-me-64-chars-random` | Y |
| `ENCRYPTION_KEY` | Clave simétrica para cifrar tokens OAuth en BD | `base64-32-byte-fernet-key` | Y |
| `PUBLIC_BASE_URL` | URL pública del frontend para armar links `/turno/{token}` en `wa.me` | `https://turnos.miconsultorio.com.ar` | N |
| `CORS_ORIGINS` | Orígenes permitidos para la API | `https://turnos.miconsultorio.com.ar` | N |
| `GOOGLE_CLIENT_ID` | Client ID OAuth 2.0 de Google Cloud | `123456.apps.googleusercontent.com` | N |
| `GOOGLE_CLIENT_SECRET` | Client Secret OAuth 2.0 de Google Cloud | `GOCSPX-...` | Y |
| `GOOGLE_REDIRECT_URI` | Callback autorizado para OAuth de Google Calendar | `https://turnos.miconsultorio.com.ar/api/v1/integraciones/google/callback` | N |
| `DEFAULT_CANCEL_NOTICE_HS` | Valor por defecto de anticipación mínima de cancelación | `24` | N |
