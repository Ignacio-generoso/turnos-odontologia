# Descripción General

## Stack tecnológico

| Capa | Tecnología | Versión mínima recomendada | Justificación |
|---|---|---|---|
| **Frontend** | React + TypeScript + Vite (PWA responsive) | React 18+, TS 5+ | Interfaz ágil en escritorio (recepción) y móvil (odontólogo/paciente) sin costo de app nativa |
| **Backend / API** | Python + FastAPI + Pydantic v2 | Python 3.11+, FastAPI 0.110+ | Desarrollo rápido, tipado fuerte, validación declarativa y ecosistema maduro para integraciones REST |
| **ORM / Migraciones** | SQLAlchemy 2.0 + Alembic | SQLAlchemy 2.0+, Alembic 1.13+ | Control explícito de transacciones, constraints de no-solapamiento y migraciones versionadas |
| **Base de datos** | PostgreSQL | PostgreSQL 15+ | Integridad referencial, constraints de exclusión/bloqueo transaccional y JSONB para odontograma/auditoría |
| **Background / Jobs** | Worker ligero Python (APScheduler / tareas async) | — | Reintentos de sincronización con Google Calendar sin requerir broker complejo en v1 |
| **Contenerización** | Docker + Docker Compose | Docker 24+ | Despliegue reproducible en VPS/cloud ubicado en Argentina |
| **Proxy / TLS** | Nginx o Caddy | — | Terminación HTTPS, headers de seguridad y servicio de assets estáticos del frontend |

---

## Arquitectura general

Aplicación web modular con arquitectura cliente-servidor desacoplada (SPA/PWA en React + API REST en FastAPI + PostgreSQL), empaquetada en contenedores Docker y alojada en infraestructura dentro de Argentina.

```
+-------------------------------------------------------------------+
|                        Clientes (HTTPS)                           |
|  - Recepción / Dueño / Admin / Odontólogo (App interna PWA)       |
|  - Paciente (Link público de reserva / confirmación / cancelación)|
+---------------------------------+---------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                   Reverse Proxy (Caddy / Nginx)                   |
+---------------------------------+---------------------------------+
                                  |
          +-----------------------+-----------------------+
          v                                               v
+------------------------+                     +--------------------+
| Frontend React + TS    |                     | Backend FastAPI    |
| (Static / PWA)         | ---- REST/JSON ---> | (Modular Monolith) |
+------------------------+                     +---------+----------+
                                                         |
                 +-------------------+-------------------+-------------------+
                 v                   v                   v                   v
      +------------------+  +------------------+  +--------------+  +------------------+
      | PostgreSQL (AR)  |  | Google Calendar  |  | WhatsApp     |  | Exportador       |
      | Datos clínicos,  |  | API v3           |  | wa.me links  |  | CSV / PDF        |
      | agenda y audit   |  | (1-way sync)     |  | (asistido)   |  | (ARCA / OS)      |
      +------------------+  +------------------+  +--------------+  +------------------+
```

### Decisiones estructurales de alto nivel

1. **Monolito modular en FastAPI**: evita sobrecarga operativa de microservicios manteniendo separación clara por dominios (`agenda`, `clinica`, `pacientes`, `pagos`, `auditoria`, `integraciones`).
2. **Aislamiento lógico por `consultorio_id`**: aunque la v1 opera para un consultorio piloto, todas las tablas de dominio portan `consultorio_id` para habilitar multi-tenancy futuro sin migraciones disruptivas.
3. **Residencia de datos en Argentina**: la base de datos PostgreSQL y los backups cifrados corren dentro de servidores/datacenters ubicados físicamente en Argentina.

---

## Integraciones externas

| Servicio / Canal | Propósito en v1 | Tipo de integración | Dirección / Estado |
|---|---|---|---|
| **Google Calendar API v3** | Reflejar altas, reprogramaciones y cancelaciones de turnos en el calendario de cada odontólogo | OAuth 2.0 + REST API (con cola de reintentos) | **Unidireccional** (`Sistema → Google`) en v1; bidireccional diferido |
| **WhatsApp (`wa.me`)** | Enviar confirmaciones y recordatorios asistidos con texto prearmado en 1 clic | Deep link `https://wa.me/...` generado por frontend/backend | **Manual asistido** en v1; Meta Business API en v1.1 |
| **Señas / Pagos** | Registrar señas, transferencias y pagos parciales o totales vinculados al turno/presupuesto | Carga manual en el sistema (sin pasarela online en v1) | **Interno** en v1; Mercado Pago en v1.1 |
| **ARCA y Obras Sociales** | Mantener datos fiscales/cobertura del paciente y generar reportes listos para facturar/liquidar | Exportación de archivos **CSV / PDF** | **Manual + exportación** en v1; integración directa diferida |

---

## API REST (resumen por recurso)

Todos los endpoints privados usan prefijo `/api/v1` y token JWT con contexto de `usuario_id`, `rol` y `consultorio_id`. Los endpoints públicos usan `/api/v1/public/{consultorio_slug}/...`.

| Recurso | Endpoints principales | Acceso |
|---|---|---|
| **Auth** | `POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout`, `GET /auth/me` | Público (login) / Autenticado |
| **Configuración y Recursos** | `GET/PUT /consultorio`, `CRUD /sillones`, `CRUD /prestaciones`, `CRUD /profesionales/horarios`, `CRUD /obras-sociales` | Dueño / Recepción (lectura) |
| **Agenda y Turnos** | `GET /turnos`, `POST /turnos`, `PATCH /turnos/{id}/reprogramar`, `PATCH /turnos/{id}/estado`, `GET /disponibilidad` | Equipo interno (según rol) |
| **Reserva Pública** | `GET /public/{slug}/catalogo`, `GET /public/{slug}/disponibilidad`, `POST /public/{slug}/reservas`, `GET/POST /public/turnos/{token}` | Público (sin login, con token firmado por turno) |
| **Pacientes** | `GET/POST /pacientes`, `GET/PATCH /pacientes/{id}`, `PATCH /pacientes/{id}/opt-in-whatsapp` | Equipo interno |
| **Clínica (restringido)** | `GET/POST /pacientes/{id}/historia-clinica`, `GET/PUT /pacientes/{id}/odontograma`, `CRUD /pacientes/{id}/planes-tratamiento` | **Solo Odontólogo/a** |
| **Presupuestos y Pagos** | `CRUD /presupuestos`, `POST /presupuestos/{id}/versiones`, `POST /pagos`, `GET /pagos`, `PATCH /pagos/{id}/anular` | Odontólogo (presupuestos), Admin/Recepción/Dueño |
| **Integraciones y Export** | `POST /integraciones/google/connect`, `GET /integraciones/google/callback`, `GET /turnos/{id}/whatsapp-link`, `GET /exportaciones/pagos`, `GET /exportaciones/turnos` | Equipo interno según rol |
| **Auditoría y Reportes** | `GET /auditoria`, `GET /reportes/ocupacion` | Dueño / Administración (reportes) |
