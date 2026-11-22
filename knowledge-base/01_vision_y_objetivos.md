# Visión y Objetivos

## Propósito del sistema

Reducir el ausentismo, las dobles reservas y la carga operativa de los consultorios odontológicos chicos de Argentina (2 a 5 profesionales) mediante una aplicación web responsive (PWA) que centraliza la agenda multi-profesional y por sillón/box, la reserva online con sincronización a Google Calendar, la ficha clínica con odontograma simple y trazabilidad de presupuestos/pagos.

El sistema nace optimizado para un consultorio piloto en Argentina con presupuesto acotado, modelado desde el día 1 con identificador de consultorio (`consultorio_id`) para permitir escalar a múltiples consultorios en versiones futuras sin reescribir la base de datos.

---

## Contexto competitivo y brechas del mercado argentino

A partir del relevamiento de 24 sistemas en [docs/discovery/market-research.md](../docs/discovery/market-research.md) (19 con evidencia pública y 5 SPA pendientes de inspección), el mercado local presenta una fragmentación clara:

- **Competidores locales relevantes**:
  - **Dentia** (AR): destaca por facturación ARCA (A/B/C), seña al reservar e IA en WhatsApp (planes públicos $20.000–$40.000 ARS/mes).
  - **DentalSoft** (AR): ofrece turnos online 24/7, odontograma, Mercado Pago y obras sociales, pero cobra mensajes de WhatsApp Meta aparte (0,026 USD/msg).
  - **Dentatools** (AR/LATAM): precio plano con usuarios ilimitados ($76.500 ARS/mes) y envío manual de WhatsApp en 1 clic, sin API automática.
  - **Dentidad** (AR): foco en seña online con Mercado Pago como herramienta anti-ausentismo, con profundidad clínica básica no evidenciada.
  - **Doctoralia PRO** (marketplace): estándar de experiencia de reserva online para el paciente, sin adaptación fiscal ni obras sociales argentinas.
  - **Dentalink** (LATAM) y **Open Dental / Curve Dental / Dentrix / CareStack** (internacionales): referentes en profundidad clínica, UX moderna y postura de seguridad (ISO 27001 / GDPR), pero sin adaptación fiscal argentina o con pricing en USD.

- **Brechas que este sistema busca cubrir**:
  1. Ningún jugador local combina simultáneamente **experiencia simple para el paciente + trazabilidad clínica básica + adaptación operativa argentina** a costo predecible.
  2. El costo variable de WhatsApp API castiga a consultorios chicos en volumen; en v1 se resuelve con envío asistido en 1 clic (`wa.me`) sin costo por mensaje.
  3. Escasa visibilidad de **auditoría de cambios y portabilidad/exportación** de datos en sistemas locales.
  4. Necesidad de **residencia de datos en Argentina** frente a soluciones alojadas en EE. UU. o UE.

---

## Objetivos por actor

| Actor | Objetivo principal | Objetivos secundarios |
|---|---|---|
| **Dueño/a del consultorio** | Tener visibilidad operativa del consultorio (ocupación, ausentismo y cobranzas) y controlar configuración y permisos | Preparar el consultorio para crecer sin cambiar de herramienta; auditar cambios críticos |
| **Odontólogo/a** | Acceder rápido a su agenda del día y registrar historia clínica, odontograma y plan de tratamiento ordenado | Sincronizar sus turnos automáticamente en Google Calendar; consultar presupuestos aceptados |
| **Recepción / secretaría** | Gestionar turnos multi-profesional y por sillón/box sin superposiciones ni doble carga | Enviar confirmaciones/recordatorios por WhatsApp en 1 clic; registrar señas y gestionar cancelaciones |
| **Administración / facturación** | Registrar pagos, señas y cobertura de obra social, y exportar datos para facturar externamente | Conciliar transferencias/pagos por turno o presupuesto; generar listados para ARCA y obras sociales |
| **Paciente** | Reservar, confirmar o cancelar turnos online desde un link público sin depender de ida y vuelta por chat | Consultar disponibilidad real por profesional/prestación y recibir recordatorio claro |

---

## Alcance v1 (MVP ajustado a presupuesto acotado)

Basado en la Sección D.3 de [docs/discovery/market-research.md](../docs/discovery/market-research.md) y ajustado para minimizar costos recurrentes en v1:

- **Agenda multi-profesional y por sillón/box**: vistas día/semana, duración variable según tipo de prestación y prevención estricta de solapamientos (por profesional y por sillón/box).
- **Reserva online por link público**: selección de prestación, profesional y horario disponible; confirmación y cancelación online respetando anticipación mínima configurable.
- **Sincronización unidireccional con Google Calendar**: alta, reprogramación y cancelación de turnos reflejadas automáticamente en el calendario del profesional (`sistema → Google Calendar`).
- **Recordatorios asistidos por WhatsApp**: generación de mensajes prearmados y disparo por link `wa.me` en 1 clic desde recepción, respetando opt-in del paciente.
- **Ficha del paciente + Historia clínica + Odontograma simple**: evolución clínica y odontograma básico con acceso estrictamente restringido al rol clínico (`Odontólogo/a`), más trazabilidad de versiones en planes de tratamiento y presupuestos.
- **Presupuestos y registro manual de pagos/señas**: registro de señas en efectivo/transferencia/otros medios, saldos y estado de cobro.
- **Coberturas / Obras sociales (informativo) y exportación básica**: carga manual de obra social/plan del paciente y exportación CSV/PDF de turnos, pagos y prestaciones para facturación externa (ARCA y liquidación de obras sociales).
- **Roles, permisos y auditoría básica**: RBAC estricto para 5 actores y registro de auditoría sobre eventos críticos (turnos, pagos, presupuestos e historia clínica).
- **Modelo preparado para crecer**: todas las entidades de negocio incluyen `consultorio_id` aunque la v1 opere sobre un único consultorio piloto.

---

## Fuera de alcance (Post-MVP)

- **v1.1 (siguiente incremento priorizado)**:
  - Cobro online automático de señas con **Mercado Pago** (checkout y webhook).
  - Recordatorios automáticos y bidireccionales vía **WhatsApp Business API (Meta)** o BSP.
  - Lista de espera automática ante cancelaciones de último momento.
- **Post-MVP / Diferido**:
  - Sincronización **bidireccional** desde Google Calendar hacia el sistema.
  - Facturación electrónica directa integrada con webservices de **ARCA**.
  - Integración automática o validación en línea de **obras sociales** y bloqueo automático de cupos.
  - Gestión de imágenes radiográficas / **DICOM**.
  - **IA conversacional** avanzada en WhatsApp o asistente clínico.
  - Operación **multi-sede** / multi-consultorio comercial (onboarding y billing SaaS) y analítica avanzada.
  - **App móvil nativa** (iOS/Android) — se prioriza web responsive / PWA.
  - Portal completo de autogestión clínica del paciente (historial de documentos, descargas clínicas).

---

## Métricas de éxito

| Métrica | Línea base esperada (manual) | Meta v1 (consultorio piloto) | Cómo se mide |
|---|---|---|---|
| **Tasa de ausentismo (no-show)** | Alta por olvido o falta de confirmación | Reducción ≥ 30% respecto al primer mes | Turnos `ausente` / total de turnos confirmados |
| **Conflictos por doble reserva** | Frecuentes por coordinación manual | **0** solapamientos por profesional o sillón/box | Validación transaccional en agenda |
| **Adopción de reserva/confirmación online** | 0% (100% WhatsApp manual) | ≥ 25% de turnos reservados o confirmados vía link público | Campo `origen` del turno (`publico` vs `interno`) |
| **Tiempo operativo de confirmación diaria** | Carga manual mensaje por mensaje | Reducción ≥ 50% usando vista diaria + `wa.me` 1 clic | Feedback del equipo de recepción |
| **Trazabilidad de presupuestos y señas** | Planillas sueltas / cuaderno | 100% de señas y presupuestos versionados registrados | Cobertura de registros en sistema + auditoría |
