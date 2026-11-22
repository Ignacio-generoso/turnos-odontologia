# Discovery — Turnos Odontología

**Fecha**: 2026-11-21
**Fuentes investigadas**: 19 sistemas con evidencia + 5 sin evidencia (SPA). Ver `discovery/sources/` e informe completo en `discovery/market-research.md`.

## 1. Problema que resuelve

Los consultorios odontológicos chicos de Argentina (2–5 profesionales) pierden turnos y tiempo porque la agenda se coordina manualmente por WhatsApp y teléfono, lo que produce ausentismo, dobles reservas y horas administrativas dedicadas a confirmar y reprogramar.

## 2. Usuarios / roles

- **Dueño/a**: configura el consultorio, precios y permisos; mira ocupación y ausentismo.
- **Odontólogo/a**: atiende, carga odontograma, historia clínica y plan de tratamiento.
- **Recepción / secretaría**: gestiona la agenda, confirma y reprograma turnos.
- **Administración / facturación**: registra pagos y coberturas, exporta datos para facturar.
- **Paciente**: reserva, confirma, cancela y paga señas.

## 3. Casos de uso

1. Como paciente, quiero reservar online y recibir un recordatorio por WhatsApp para no olvidarme del turno.
2. Como recepción, quiero ver la agenda del día y reprogramar sin superponer turnos.
3. Como odontólogo, quiero cargar odontograma y plan de tratamiento para tener la historia clínica ordenada.
4. Como administración, quiero registrar pagos, señas y coberturas, y exportar datos para facturar fuera del sistema.
5. Como dueño, quiero ver ocupación y ausentismo para tomar decisiones.

## 4. Competidores / soluciones existentes

| Competidor | Problema que resuelve | Pricing | Diferenciadores |
|---|---|---|---|
| DentalSoft | Gestión integral del consultorio | Gratis / $30.000 / $60.000 ARS por mes | Pricing público local; WhatsApp con costo por mensaje |
| Dentalink | Software dental cloud LATAM | (no publicado) | ISO 27001 declarada; profundidad clínica |
| Dentia | Gestión + automatización | (no publicado) | IA en WhatsApp + facturación ARCA |
| Dentatools | Gestión cloud | $76.500 ARS/mes IVA incl. | Usuarios ilimitados |
| Dentidad | Turnos + seña anti-ausentismo | (no publicado) | Seña online con Mercado Pago |
| Doctoralia PRO | Marketplace + agenda | $25.000 / $35.000 / $55.000 ARS/mes | Demanda de pacientes y reputación pública |
| Open Dental | Software dental configurable | USD 199/mes por sede | Configurabilidad y bridges |
| Curve Dental | Cloud dental | (no publicado) | UX moderna cloud-first |

**Notas**: el mercado local combina agenda con una integración fuerte aislada (ARCA, WhatsApp o Mercado Pago), pero ningún jugador reúne profundidad clínica + compliance local + experiencia de paciente. Los internacionales lideran en clínica y seguridad, sin adaptación fiscal argentina.

## 5. Funcionalidades necesarias

- Agenda multi-profesional con vista día/semana y prevención de solapamientos.
- Reserva online del paciente por link público, con confirmación y cancelación.
- Recordatorios automáticos por WhatsApp con opt-in.
- Odontograma, historia clínica y plan de tratamiento.
- Presupuestos y registro de pagos/seña.
- Registro manual y exportación de datos para ARCA y obras sociales.
- Roles y permisos (dueño, odontólogo, recepción, administración).
- Sincronización con Google Calendar.

## 6. Funcionalidades opcionales

- Analítica avanzada (ocupación, ausentismo, rentabilidad).
- Portal del paciente para autogestión.

## 7. Reglas de negocio

- Anticipación mínima configurable para cancelar un turno.
- Un profesional no puede tener dos turnos superpuestos.
- Límite de turnos por obra social/cobertura.

## 8. Integraciones

- **Google Calendar**: obligatoria en v1.
- **WhatsApp**: canal de recordatorios (proveedor y costo a definir).
- **ARCA y obras sociales**: registro manual + exportación en v1, sin integración automática.
- **Seña/pagos**: se registra en el sistema; proveedor de cobro sin definir.

## 9. Restricciones

- Los datos de pacientes deben alojarse en Argentina.
- Presupuesto acotado.

## 10. Riesgos

- **Supuesto sin probar**: que los pacientes adopten la reserva online cuando hoy usan WhatsApp por costumbre.
- **Costo variable**: el precio por mensaje de WhatsApp (Meta) puede erosionar el presupuesto del consultorio.
- **Modelado de coberturas**: el límite de turnos por obra social sin integración depende de carga manual y es propenso a error.
- **Infraestructura**: la residencia de datos en Argentina restringe proveedores cloud y puede encarecer el MVP.
- **Alcance**: presupuesto acotado frente a un MVP amplio (clínica + agenda + pagos + coberturas).

## 11. Preguntas abiertas

- ¿Qué proveedor de seña/pagos se usa (Mercado Pago u otro)?
- ¿WhatsApp API oficial de Meta o un intermediario? ¿Quién absorbe el costo por mensaje?
- ¿Qué obras sociales se priorizan y cómo se define su límite de turnos?
- ¿Google Calendar sincroniza en un solo sentido o bidireccional?
- ¿Cuál es el modelo de precio del producto en ARS?
- ¿Se revisan los 5 sitios SPA (Dentaly, OdontoApp, OdontoLog, Dentiqly, Denticon) antes de cerrar el benchmark?
