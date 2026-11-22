# Actores y Roles

## Actores del sistema

| Actor | Tipo | Descripción | Cómo interactúa con el sistema |
|---|---|---|---|
| **Dueño/a del consultorio** | Interno (autenticado) | Responsable del negocio, configuración general, tarifas, sillones y control operativo | App web interna: configura consultorio, usuarios, prestaciones, horarios; ve métricas de ocupación, pagos y auditoría |
| **Odontólogo/a** | Interno clínico (autenticado) | Profesional que atiende pacientes y es único responsable del registro clínico | App web / móvil (PWA): ve su agenda, atiende turnos, carga historia clínica, odontograma, planes de tratamiento y presupuestos; conecta su Google Calendar |
| **Recepción / secretaría** | Interno operativo (autenticado) | Coordina la agenda diaria del consultorio y el contacto con pacientes | App web interna: crea/reprograma/cancela turnos, asigna sillón/box, dispara recordatorios por `wa.me`, registra señas iniciales y da de alta datos administrativos del paciente |
| **Administración / facturación** | Interno administrativo (autenticado) | Controla ingresos, señas, saldos, coberturas y preparación de datos fiscales | App web interna: registra y concilia pagos, gestiona presupuestos aprobados a nivel financiero, carga obras sociales y exporta CSV/PDF para ARCA y liquidaciones |
| **Paciente** | Externo (sin cuenta en v1) | Persona que solicita o gestiona un turno odontológico | Links públicos web: reserva turno online por link del consultorio y confirma/cancela mediante token único de turno |

> **Nota sobre rol dual**: si el/la Dueño/a del consultorio también atiende pacientes como profesional, su usuario puede tener asignados ambos roles (`dueno` + `odontologo`) de forma explícita. Un usuario con rol únicamente `dueno` **no** tiene acceso a la historia clínica ni al odontograma.

---

## RBAC — Matriz de permisos

Convención: **C** (Crear), **R** (Leer), **U** (Actualizar), **D** (Anular/Desactivar lógico — no se permite borrado físico de registros clínicos ni financieros). `—` = Acceso denegado (HTTP `403 Forbidden`).

| Recurso / Módulo | Dueño/a *(solo gestión)* | Odontólogo/a | Recepción / secretaría | Administración / facturación | Paciente *(link/token público)* |
|---|---|---|---|---|---|
| **Configuración consultorio, sillones, prestaciones y horarios** | C R U D | R | R | R | R *(solo catálogo público habilitado)* |
| **Gestión de usuarios y roles** | C R U D | — | — | — | — |
| **Agenda y Turnos** | R *(todos)* | R / U *(estado propio)* | C R U D *(todos)* | R *(todos)* | C *(reservar)* / R U *(solo su turno vía token)* |
| **Ficha administrativa del paciente** *(nombre, DNI, teléfono, opt-in WA, obra social)* | R | R | C R U | R U *(cobertura/datos fiscales)* | C *(datos propios al reservar)* |
| **Historia clínica (evoluciones, antecedentes)** | **—** *(bloqueado)* | **C R U** | **—** *(bloqueado)* | **—** *(bloqueado)* | **—** |
| **Odontograma** | **—** *(bloqueado)* | **C R U** | **—** *(bloqueado)* | **—** *(bloqueado)* | **—** |
| **Planes de tratamiento** | **—** *(bloqueado)* | **C R U** | **—** *(bloqueado)* | **—** *(bloqueado)* | **—** |
| **Presupuestos** *(ítems económicos y estado de aceptación)* | R | C R U | R *(resumen de saldo)* | R U *(estado de cobro)* | — |
| **Pagos y Señas manuales** | R | R *(solo consulta básica)* | C R *(registrar seña / ver saldo)* | C R U D *(anulación con motivo)* | — |
| **Recordatorios WhatsApp (`wa.me`)** | R | R *(su agenda)* | C R *(generar/abrir link)* | — | — |
| **Conexión Google Calendar** | R *(estado)* | C R U D *(su cuenta)* | — | — | — |
| **Exportaciones CSV/PDF (ARCA / Obras sociales / Pagos)** | R | — | — | C R *(exportar)* | — |
| **Reportes de ocupación y ausentismo** | R | R *(propios)* | R *(operativo del día)* | R | — |
| **Registro de auditoría (`audit_logs`)** | R | — | — | R *(eventos financieros)* | — |

### Regla crítica de privacidad clínica

- Los endpoints bajo `/api/v1/pacientes/{id}/historia-clinica`, `/odontograma` y `/planes-tratamiento` exigen explícitamente el rol `odontologo` en el guard de autorización del backend (no basta con ocultar botones en el frontend).
- Si un usuario posee `dueno` pero **no** `odontologo`, recibe `403 Forbidden` al intentar acceder a información clínica.

---

## Rutas públicas (sin autenticación de usuario)

| Ruta frontend / API | Propósito | Mecanismo de seguridad |
|---|---|---|
| `/reservar/{consultorio_slug}` | Flujo público para que el paciente elija prestación, profesional y horario disponible y reserve su turno | Rate limiting por IP, validación estricta de schema, sin exponer datos de otros pacientes ni sillones internos |
| `/turno/{token}` | Vista pública del turno del paciente para **confirmar asistencia** o **cancelar** respetando anticipación mínima | Token opaco criptográfico (mín. 32 bytes / UUIDv4+HMAC) de un solo turno, con expiración ligada a la fecha del turno |
| `/login` | Pantalla de inicio de sesión para el equipo interno | Protección contra fuerza bruta / bloqueo temporal por intentos fallidos |
| `/api/v1/integraciones/google/callback` | Callback OAuth 2.0 de Google Calendar | Parámetro `state` firmado y validado contra la sesión del profesional |
