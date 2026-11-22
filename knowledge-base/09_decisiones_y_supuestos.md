# Decisiones y Supuestos

## Decisiones documentadas

### DD-01 — Aplicación web responsive / PWA para consultorio piloto con modelado `consultorio_id`
**Decisión**: Construir una aplicación web responsive (PWA) orientada en v1 a un consultorio piloto (2–5 profesionales), incluyendo `consultorio_id` en todas las entidades de negocio y consultas.
**Contexto**: Se requiere validar el producto rápido en un consultorio chico sin complejizar onboarding ni billing SaaS, pero evitando una reescritura si luego escala a múltiples consultorios.
**Alternativas consideradas**: (a) Sistema single-tenant sin `consultorio_id`; (b) SaaS multi-tenant comercial completo desde el día 1.
**Justificación**: El costo de incluir `consultorio_id` desde el esquema inicial es bajo y habilita futura expansión multi-consultorio mientras multi-sede y onboarding SaaS quedan diferidos post-MVP (alineado con [docs/discovery/market-research.md](../docs/discovery/market-research.md) §D.3).
**Trade-offs aceptados**: En v1 no habrá panel super-admin de alta de clínicas ni facturación de suscripciones SaaS.

---

### DD-02 — Ajuste respecto a D.3: Recordatorios WhatsApp asistidos (`wa.me` 1 clic) en v1, API Meta en v1.1
**Decisión**: Reemplazar los recordatorios automáticos vía WhatsApp Business API (sugeridos en la Sección D.3 de `market-research.md`) por envío asistido mediante enlaces `wa.me` en 1 clic con texto prearmado y control de opt-in en v1, posponiendo la API oficial de Meta / BSP para **v1.1**.
**Contexto**: La restricción de **presupuesto acotado** del proyecto y la evidencia competitiva (DentalSoft cobra 0,026 USD por mensaje de Meta, mientras Dentatools resuelve v1 con envío manual en 1 clic) muestran que el costo por mensaje y la aprobación de plantillas Meta pueden encarecer o frenar la v1.
**Alternativas consideradas**: Integrar Meta WhatsApp Cloud API o un BSP desde el día 1.
**Justificación**: Elimina costos variables por mensaje y complejidad de webhooks/plantillas en el piloto, manteniendo una arquitectura con puerto/adaptador para enchufar Meta API en v1.1.
**Trade-offs aceptados**: El envío del recordatorio no es desatendido; requiere que recepción haga clic por cada turno (aliviado por el mensaje prearmado con link `/turno/{token}`).

---

### DD-03 — Ajuste respecto a D.3: Registro manual de señas y pagos en v1, Mercado Pago en v1.1
**Decisión**: Postergar la integración online con Mercado Pago (mencionada en §D.3 de `market-research.md`) para **v1.1**, implementando en v1 el registro manual completo de señas, transferencias y pagos con inmutabilidad contable y anulación auditada.
**Contexto**: El presupuesto acotado prioriza entregar agenda, clínica y trazabilidad básica antes que integrar checkout, webhooks de pago, conciliación y comisiones de pasarela.
**Alternativas consideradas**: Integrar Mercado Pago Checkout Pro / QR desde v1.
**Justificación**: Permite al consultorio seguir cobrando señas por transferencia/efectivo como hoy lo hace, pero ordenando los saldos dentro del sistema desde el primer día y dejando lista la relación `pagos ↔ turnos/presupuestos` para automatizar en v1.1.
**Trade-offs aceptados**: El paciente no paga la seña dentro del flujo público `/reservar/{slug}` en v1; la confirmación de seña depende de carga manual de recepción/administración.

---

### DD-04 — Stack tecnológico: FastAPI + PostgreSQL + React/TypeScript en Docker (Argentina)
**Decisión**: Adoptar Python (FastAPI) + PostgreSQL en el backend y React + TypeScript (PWA) en el frontend, contenerizados con Docker y alojados en servidor/VPS en Argentina.
**Contexto**: Se necesita mantener costos predecibles, alta mantenibilidad, integridad transaccional para no-solapamiento de turnos y cumplimiento de residencia de datos de pacientes en Argentina.
**Alternativas consideradas**: Stack full-stack Node/Next.js o servicios PaaS gestionados en EE. UU./Brasil.
**Justificación**: PostgreSQL aporta `btree_gist` exclusion constraints nativos para evitar dobles reservas en profesional y sillón; FastAPI ofrece tipado claro y velocidad de desarrollo; Docker facilita migrar entre proveedores de VPS en Argentina.
**Trade-offs aceptados**: Mayor responsabilidad operativa sobre backups y mantenimiento de VPS comparado con un PaaS extranjero gestionado (mitigado documentando backups cifrados y scripts en `08_arquitectura_propuesta.md`).

---

### DD-05 — Sincronización unidireccional con Google Calendar en v1
**Decisión**: Sincronizar únicamente en sentido `Sistema → Google Calendar` del profesional en v1; la sincronización bidireccional queda diferida post-MVP.
**Contexto**: Google Calendar es integración obligatoria en v1, pero manejar webhooks `watch`, conflictos de edición externa y eventos personales del odontólogo duplica la complejidad.
**Alternativas consideradas**: Sincronización bidireccional desde v1.
**Justificación**: Cubre la necesidad real del odontólogo (ver sus turnos del consultorio en el calendario de su celular) con riesgo acotado y sin comprometer la fuente de verdad de la agenda (`PostgreSQL`).
**Trade-offs aceptados**: Si el odontólogo bloquea un horario personal en su Google Calendar, debe cargarlo también como bloqueo en el sistema para que no se ofrezca en la reserva online.

---

### DD-06 — Aislamiento estricto de Historia Clínica y Odontograma solo para Odontólogo/a
**Decisión**: Restringir lectura y escritura de `historias_clinicas`, `odontogramas` y `planes_tratamiento` exclusivamente al rol `odontologo` (bloqueado para `recepcion`, `administracion` y `dueno` sin rol clínico).
**Contexto**: Protección de privacidad clínica y trazabilidad médico-legal de datos sensibles de pacientes.
**Alternativas consideradas**: Permitir lectura al Dueño/a por defecto.
**Justificación**: Un dueño no odontólogo no debe acceder a evoluciones clínicas; si el dueño además atiende pacientes, se le asignan ambos roles explícitamente (`dueno` + `odontologo`).
**Trade-offs aceptados**: Recepción solo ve observaciones operativas de agenda y estado económico de presupuestos/pagos, no el detalle clínico.

---

### DD-07 — Obras sociales informativas y exportación manual para ARCA en v1
**Decisión**: Registrar obra social/plan del paciente y un cupo mensual de referencia de carácter meramente informativo, sin bloqueo automático de turnos ni integración online con ARCA/obras sociales; cubrir el cumplimiento mediante exportación CSV/PDF.
**Contexto**: Las integraciones fiscales (ARCA) y con padrones de obras sociales varían por convenio y exceden el presupuesto de v1.
**Alternativas consideradas**: Bloqueo duro de turnos por cupo de obra social o integración directa con webservices ARCA.
**Justificación**: Evita falsos rechazos de turnos por datos cargados manualmente y entrega valor inmediato a administración para facturar y liquidar externamente.
**Trade-offs aceptados**: El control de topes de obra social sigue bajo criterio administrativo en v1.

---

## Supuestos inferidos y confirmados

### SU-01 — Aplicación web responsive sin app móvil nativa en v1
**Supuesto**: El sistema opera como web responsive / PWA desde navegador de escritorio (recepción/administración) y celular (odontólogo/paciente), sin app nativa iOS/Android.
**Origen**: Confirmado por el usuario (sobre `docs/discovery/market-research.md` §D.3).
**Riesgo si es falso**: Si un profesional exige notificaciones push nativas offline en iOS, la PWA tiene limitaciones en Safari.
**Cómo validar**: Probar usabilidad móvil en Android/iOS con los odontólogos del consultorio piloto durante la primera semana de uso.

### SU-02 — Facturación ante ARCA fuera del sistema en v1
**Supuesto**: La facturación electrónica oficial ante ARCA se realiza externamente usando los datos exportados en CSV/PDF desde el sistema.
**Origen**: Confirmado por el usuario y `docs/discovery/discovery.md` §8.
**Riesgo si es falso**: Si el consultorio exige emitir Factura C/B automática dentro de la misma pantalla desde el día 1, habrá fricción en administración.
**Cómo validar**: Verificar con administración del consultorio piloto los campos exactos que requiere su contador/facturador ARCA para el CSV.

### SU-03 — Cada turno vincula profesional, sillón/box y duración por prestación
**Supuesto**: Todo turno requiere un profesional, un sillón/box físico y una duración determinada por el tipo de prestación (ajustable internamente), impidiendo solapamientos en ambos recursos.
**Origen**: Confirmado por el usuario.
**Riesgo si es falso**: Si el consultorio realiza prácticas simultáneas con asistentes en más de un sillón bajo un solo odontólogo, la restricción 1:1 del profesional podría resultar estricta.
**Cómo validar**: Confirmar en el consultorio piloto si un odontólogo atiende exclusivamente un sillón a la vez o si usa sillones paralelos con asistente.

### SU-04 — Adopción de reserva online por parte de pacientes habituales
**Supuesto**: Una porción significativa de pacientes adoptará el link público `/reservar/{slug}` y `/turno/{token}` cuando recepción lo envíe por WhatsApp.
**Origen**: `docs/discovery/discovery.md` §10 (riesgo identificado) y `market-research.md` §D.4.
**Riesgo si es falso**: Recepción seguirá cargando casi el 100% de los turnos manualmente, aunque igualmente conservará el beneficio de agenda sin solapamientos y confirmaciones rápidas.
**Cómo validar**: Medir porcentaje de turnos con `origen = 'publico'` y confirmaciones vía `/turno/{token}` en los primeros 30 días del piloto.

### SU-05 — Disponibilidad de proveedor VPS en Argentina dentro del presupuesto
**Supuesto**: Existen proveedores VPS/cloud en Argentina con PostgreSQL/Docker estable dentro del presupuesto mensual del consultorio piloto.
**Origen**: Restricción de residencia de datos en Argentina + presupuesto acotado (`discovery.md` §9).
**Riesgo si es falso**: Costos inesperados o menor disponibilidad de hardware local respecto a clouds globales.
**Cómo validar**: Cotizar 2–3 proveedores locales con datacenter en Argentina antes de pasar a infraestructura de producción.
