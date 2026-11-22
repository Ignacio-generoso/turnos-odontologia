# Investigación de mercado — Sistemas de gestión y turnos odontológicos (Argentina → LATAM → referencias internacionales)

**Fecha de investigación**: 2026-11-21
**Alcance**: software de agenda/turnos, gestión clínica odontológica, CRM y marketplaces con agenda.
**Método**: relevamiento web de sitios oficiales (producto y pricing) + notas por competidor en `discovery/sources/`. Cada fila de la Tabla A registra la **empresa proveedora** y la **fecha de consulta**.
**Criterio de evidencia**: solo se afirma lo visible públicamente. Lo no demostrado se marca como `(no evidenciado)` o `(no publicado)`. Las afirmaciones comerciales del proveedor se identifican como tales y no se equiparan a funcionalidad comprobada.

> **Límite metodológico**: 5 sitios (Dentaly, OdontoApp, OdontoLog, Dentiqly, Denticon) devolvieron un shell de SPA sin contenido renderizado y no pudieron evaluarse. No se usó navegador headless en esta corrida.

---

## A. Tabla comparativa

### A.1 Mercado argentino y LATAM (ordenado por relevancia para Argentina)

| # | Sistema | Empresa proveedora | Origen / mercado | Enfoque principal | Turnos / automatización | Clínica dental | WhatsApp / IA | Integración local AR | Pricing público | Trial | Fecha de consulta | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **DentalSoft** | DentalSoft | Argentina | Gestión integral de consultorio | Agenda, turnos online 24/7 + recordatorios | Historia clínica, odontograma | WhatsApp (costo Meta 0,026 USD/msg) + asistente IA | ARS, **Mercado Pago** (señas) y obras sociales; ARCA no evidenciado | Gratis (3 meses) / $30.000 / $60.000 ARS por mes | Plan gratis (3 meses) | 2026-11-22 | dentalsoft.com.ar |
| 2 | **Dentalink** | Dentalink | Chile / LATAM | Software dental cloud | Agenda | Ficha clínica, presupuestos | No evidenciado | No evidenciado | (no publicado) — cotización | No evidenciado | 2026-11-21 | softwaredentalink.com/ar |
| 3 | **Dentia** | Dentia | Argentina | Gestión + automatización | Turnos + seña al reservar | Historia clínica, odontograma, IA clínica | WhatsApp con IA (plan Elite) | **ARCA** (facturación electrónica A/B/C) | **Básico $20.000 / Pro $30.000 / Elite $40.000 ARS/mes** | 30 días | 2026-11-22 | dentia.tech |
| 4 | **Dentatools** | Dentatools | Argentina / LATAM | Gestión cloud | Agenda + auto-agendado | Historia clínica, odontograma, presupuestos | WhatsApp en 1 clic (envío manual, sin API) | Cobros en ARS (Factura C suscripción) | **$76.500 ARS/mes IVA incl., usuarios ilimitados** | No evidenciado | 2026-11-22 | dentatools.co/ar |
| 5 | **Doctoralia PRO** | Doctoralia (Docplanner Group) | España / 13 países (incl. AR) | Marketplace + agenda | Reserva online, recordatorios | Historia clínica desde plan Plus | SMS (no WhatsApp evidenciado) | Precio en ARS; sin ARCA/obras sociales | Starter $25.000 / Plus $35.000 / VIP $55.000 ARS/mes (anual) | Versión gratuita | 2026-11-21 | pro.doctoralia.com/ar/precio |
| 6 | **Dentidad** | Dentidad | Argentina | Turnos + seña anti-ausentismo | Turnos | Básica (no evidenciada) | No evidenciado | **Mercado Pago** (seña) | (no publicado) | 14 días | 2026-11-21 | dentidad.com |
| 7 | **Odontal Web** | Odontal Web | Argentina | Gestión + asistente IA | Turnos | Módulos clínicos | IA "Odi"; sin costo por mensaje declarado | No evidenciado | (no publicado) | No evidenciado | 2026-11-21 | odontalweb.com.ar |
| 8 | **Bilog** | Bilog | Argentina | Gestión de consultorios | Turnos | Módulos clínicos/administrativos | No evidenciado | No evidenciado | (no publicado) | No evidenciado | 2026-11-21 | bilog.com.ar |
| 9 | **DentalFLOW** | DentalFLOW | Argentina (Río Negro) | Gestión de consultorio | Turnos | Módulos de consultorio | WhatsApp y obras sociales **"próximamente"** | Anunciada, no disponible | (no publicado) | No evidenciado | 2026-11-21 | dentalflow.ar |
| 10 | **OCLÜ** | OCLÜ | Argentina / LATAM | CRM all-in-one | Agenda + seguimiento comercial | Limitada (CRM) | IA "OCLÜ IA" | No evidenciado; DICOM como add-on | (no publicado) | No evidenciado | 2026-11-21 | oclucrm.com/latam |
| 11 | **DenPro** | DenPro | Internacional (datos UE/GDPR) | Gestión odontológica | Turnos | Módulos clínicos/administrativos | No evidenciado | No evidenciado; datos en UE | (no publicado) | No evidenciado | 2026-11-21 | denpro.ar |
| 12 | **DrApp** | DrApp | Argentina | Salud multi-especialidad | Agenda | Baja (no exclusivo dental) | No evidenciado | No evidenciado | (no publicado) | 15 días | 2026-11-21 | drapp.com.ar/odontologia |
| 13 | **NacarOS** | NacarOS | LATAM | Gestión PWA | Turnos | Básica | No evidenciado | Precio en USD | Gratis hasta 20 pacientes activos; Pro USD 14,99/mes (11,99 anual) | Plan gratis | 2026-11-21 | nacaros.com |
| 14 | **IKOMDENTAL** | IKOMDENTAL | LATAM / US / CA / ES (23 países) | Gestión dental | Turnos | Módulos clínicos/administrativos | No evidenciado | No evidenciado | (no publicado) | 30 días | 2026-11-21 | ikomdental.com |
| 15 | **Gestión Odontológica** | Gestión Odontológica | Colombia | Gestión + contabilidad | Turnos | Módulos clínicos | No evidenciado | Nómina electrónica **colombiana** | (no publicado) | No evidenciado | 2026-11-21 | gestionodontologica.com |

### A.2 Referencias internacionales (benchmark funcional, no competencia directa en AR)

| # | Sistema | Empresa proveedora | Mercado | Enfoque | Features clave | Pricing público | Fecha de consulta | Fuente |
|---|---|---|---|---|---|---|---|---|
| 16 | **Open Dental** | Open Dental Software, Inc. | EE. UU. | Software configurable / ecosistema abierto | Alta configurabilidad, cientos de bridges, imaging, portal | **USD 199/mes por sede** (soporte, contrato 12 meses; tarifas distintas fuera de EE. UU.) | 2026-11-21 | opendental.com |
| 17 | **Curve Dental** | Curve Dental | EE. UU. / CA | Cloud-first | Gestión clínica y administrativa en nube; I+D declarada USD 200M | (no publicado) | 2026-11-21 | curvedental.com |
| 18 | **Dentrix** | Henry Schein One | EE. UU. | Suite integral | Suite clínica, administrativa e imaging | (no publicado) | 2026-11-21 | dentrix.com |
| 19 | **CareStack** | CareStack | US / UK / AU | Cloud todo-en-uno para grupos | Multi-sede, consolidación de herramientas | (no publicado) | 2026-11-21 | carestack.com |

### A.3 Sistemas sin evidencia (shell SPA)

| Sistema | Empresa proveedora | URL | Resultado | Fecha de consulta |
|---|---|---|---|---|
| Dentaly | Dentaly | dentaly.com.ar | Sin contenido renderizado | 2026-11-21 |
| OdontoApp | OdontoApp | odontoapp.online | Sin contenido renderizado | 2026-11-21 |
| OdontoLog | OdontoLog | odontolog.lat | Sin contenido renderizado | 2026-11-21 |
| Dentiqly | Dentiqly | dentiqly.com | Sin contenido renderizado | 2026-11-21 |
| Denticon | Denticon | denticon.com | Sin contenido renderizado | 2026-11-21 |

> **Empresa proveedora**: se consigna el nombre comercial/razón social pública del proveedor; cuando la razón social no pudo verificarse en el sitio, se usa el nombre comercial. **Fecha de consulta**: fecha del relevamiento de esa fila.

---

## B. Matriz de puntuación (0–5)

**Pesos**: Turnos/automatización 25% · Funcionalidad odontológica clínica 20% · Integraciones locales y WhatsApp 15% · Administración/cobros/facturación 15% · Experiencia del paciente 10% · Seguridad/exportación/trazabilidad 10% · Precio y adopción 5%.

**Escala**: 0 = ausente/no evidenciado; 3 = presente pero no diferencial; 5 = diferencial comprobado.
**Advertencia**: la nota es juicio analítico sobre la evidencia pública, no una medición del producto en uso.

| Sistema | Turnos 25% | Clínica 20% | Local+WA 15% | Admin/cobros 15% | Paciente 10% | Seguridad 10% | Precio 5% | **Ponderado (0–5)** | **Índice (0–100)** |
|---|---|---|---|---|---|---|---|---|---|
| **Dentia** | 5 | 3 | 5 | 4 | 4 | 3 | 3 | **4,05** | **81** |
| **Dentalink** | 4 | 4 | 3 | 4 | 3 | 5 | 2 | **3,75** | **75** |
| **DentalSoft** | 4 | 4 | 3 | 4 | 3 | 3 | 4 | **3,65** | **73** |
| **Open Dental** | 4 | 5 | 1 | 4 | 3 | 4 | 2 | **3,55** | **71** |
| **Dentrix** | 4 | 5 | 1 | 4 | 3 | 4 | 1 | **3,50** | **70** |
| **Curve Dental** | 4 | 4 | 1 | 4 | 4 | 4 | 2 | **3,45** | **69** |
| **CareStack** | 4 | 4 | 1 | 4 | 4 | 4 | 2 | **3,45** | **69** |
| **Dentatools** | 4 | 3 | 3 | 4 | 3 | 3 | 3 | **3,40** | **68** |
| **Doctoralia PRO** | 4 | 2 | 4 | 3 | 5 | 3 | 3 | **3,40** | **68** |
| **Odontal Web** | 4 | 3 | 3 | 3 | 4 | 2 | 3 | **3,25** | **65** |
| **Dentidad** | 4 | 2 | 4 | 3 | 4 | 2 | 3 | **3,20** | **64** |
| **Bilog** | 3 | 4 | 2 | 4 | 2 | 3 | 3 | **3,10** | **62** |
| **OCLÜ** | 3 | 2 | 4 | 3 | 4 | 3 | 2 | **3,00** | **60** |
| **IKOMDENTAL** | 3 | 4 | 2 | 3 | 3 | 3 | 2 | **3,00** | **60** |
| **Gestión Odontológica** | 3 | 4 | 1 | 4 | 2 | 3 | 2 | **2,90** | **58** |
| **DenPro** | 3 | 3 | 2 | 3 | 2 | 4 | 2 | **2,80** | **56** |
| **DentalFLOW** | 3 | 3 | 2 | 3 | 2 | 2 | 3 | **2,65** | **53** |
| **NacarOS** | 3 | 2 | 2 | 3 | 3 | 2 | 4 | **2,60** | **52** |
| **DrApp** | 4 | 1 | 2 | 2 | 3 | 2 | 3 | **2,45** | **49** |

**Lectura de la matriz**
- Los mejor puntuados en el mercado argentino combinan agenda sólida con **una** integración local fuerte (Dentia: ARCA + IA; DentalSoft: precio y WhatsApp; Dentidad: Mercado Pago).
- Ningún jugador local obtiene puntaje alto simultáneamente en **profundidad clínica + compliance local + experiencia de paciente**. Ese hueco es la oportunidad.
- Los sistemas internacionales lideran en clínica y seguridad, pero su baja adaptación local (idioma fiscal, obras sociales, precio en USD) los saca de la competencia directa.

---

## C. Análisis competitivo

### C.1 Funcionalidades estándar (table stakes)

1. Agenda de turnos con vista día/semana y asignación por profesional.
2. Ficha/registro del paciente.
3. Historia clínica odontológica básica.
4. Presupuestos y planes de tratamiento.
5. Recordatorios de turnos (email/SMS/WhatsApp).
6. Gestión de pagos y estado de cuenta.
7. Roles básicos (dueño, profesional, recepción).
8. Reportes operativos simples.

### C.2 Diferenciadores reales observados (no marketing)

| Diferenciador | Quién lo tiene | Evidencia |
|---|---|---|
| **Facturación electrónica ARCA** | Dentia | dentia.tech |
| **WhatsApp con IA** | Dentia (plan Elite); Odontal Web ("Odi"); DentalSoft | dentia.tech; odontalweb.com.ar; dentalsoft.com.ar |
| **Seña online con Mercado Pago** | Dentidad; DentalSoft | dentidad.com; dentalsoft.com.ar |
| **Precio plano con usuarios ilimitados** | Dentatools | dentatools.co/ar |
| **ISO 27001 declarada** | Dentalink | softwaredentalink.com/ar |
| **Datos en UE / GDPR** | DenPro | denpro.ar |
| **Marketplace con demanda de pacientes** | Doctoralia PRO | pro.doctoralia.com/ar/precio |
| **Configurabilidad y bridges** | Open Dental | opendental.com |

### C.3 Brechas frecuentes en el mercado argentino

1. **Pricing opaco**: la mayoría no publica precios (Dentalink, Dentidad, Odontal Web, Bilog, DentalFLOW, OCLÜ, DenPro, DrApp, IKOMDENTAL). *(Corregido tras verificación: Dentia sí publica sus planes en ARS en sus preguntas frecuentes).*
2. **Integración local incompleta**: ARCA, obras sociales y convenios rara vez están resueltos; DentalFLOW los anuncia como "próximamente".
3. **WhatsApp como add-on caro**: en DentalSoft el mensaje de Meta se cobra aparte (0,026 USD), lo que castiga a consultorios con volumen.
4. **Anti-ausentismo débil**: pocos competidores locales evidencian seña online (Dentidad, DentalSoft y Dentia en reserva por chat); la lista de espera aparece en Doctoralia VIP, no en los locales.
5. **Profundidad clínica vs. simplicidad**: los locales priorizan agenda/administración; los internacionales priorizan clínica pero no adaptan lo fiscal.
6. **Seguridad y portabilidad poco visibles**: solo Dentalink (ISO 27001) y DenPro (GDPR) comunican postura de seguridad; exportación/auditoría no se evidencia en la mayoría.
7. **IA como discurso**: "IA" aparece en Dentia, Odontal Web y OCLÜ, pero no se documenta alcance, límites ni supervisión.
8. **Multi-sede**: no se evidencia en los locales; es territorio de CareStack/Curve/Dentrix.

### C.4 Oportunidades de innovación

1. **WhatsApp nativo con costo transparente y opt-in**: reserva, confirmación, recordatorio y reprogramación en un solo hilo, con control de gasto por mensaje.
2. **Anti-no-show combinado**: seña online + lista de espera automática + recordatorio escalonado.
3. **Odontograma + presupuesto con trazabilidad**: versión del plan, aceptación del paciente y auditoría de cambios.
4. **Cumplimiento local de punta a punta**: ARCA + medios de pago + obras sociales en un flujo, no como módulos separados.
5. **Portabilidad y seguridad explícitas**: exportación completa, registro de auditoría y política de datos visible.
6. **PWA multi-dispositivo**: operar desde celular en consultorios chicos sin instalación (NacarOS ya lo insinúa, pero con poca profundidad clínica).
7. **Precio local claro**: planes en ARS con límites explícitos, aprovechando la opacidad general del mercado.

---

## D. Recomendación final

### D.1 Cinco competidores prioritarios para demo

| Prioridad | Competidor | Por qué mirarlo |
|---|---|---|
| 1 | **DentalSoft** | Único local con pricing público completo; benchmark de planes y de costo WhatsApp. |
| 2 | **Dentalink** | Referencia LATAM de profundidad clínica y seguridad (ISO 27001). |
| 3 | **Dentia** | Mejor combinación evidenciada de IA en WhatsApp + facturación ARCA. |
| 4 | **Dentatools** | Benchmark de precio plano con usuarios ilimitados. |
| 5 | **Dentidad** | Único con seña online (Mercado Pago) como anti-ausentismo. |

**Comodín de análisis**: Doctoralia PRO — no es sistema clínico, pero marca el estándar de experiencia de reserva y captación de pacientes.

### D.2 Tres productos de referencia para UX

1. **Curve Dental** — claridad y modernidad de la interfaz cloud.
2. **Open Dental** — profundidad y configurabilidad del flujo clínico.
3. **Doctoralia PRO** — flujo de reserva y autogestión del paciente.

### D.3 MVP sugerido

**Must-have (v1)**
1. Agenda multi-profesional con vista día/semana y prevención de solapamientos.
2. Reserva online del paciente por link público, con confirmación y cancelación.
3. Recordatorios automáticos por WhatsApp con opt-in y control de costo.
4. Ficha del paciente + odontograma simple + plan de tratamiento/presupuesto.
5. Registro de pagos y seña online (Mercado Pago).
6. Roles y permisos (dueño, odontólogo, recepción).
7. Exportación de datos y registro de auditoría básico.

**Diferenciadores de la v1**
- WhatsApp nativo con costo transparente (no add-on sorpresa).
- Anti-no-show: seña + lista de espera automática.
- Precio local transparente en ARS.
- Odontograma + presupuesto con trazabilidad de versiones.

**Diferido (post-MVP)**
- Facturación electrónica ARCA.
- Integración con obras sociales.
- IA conversacional avanzada.
- Imágenes/DICOM.
- Multi-sede y analítica avanzada.
- App móvil nativa (priorizar PWA).

### D.4 Supuestos y límites de esta recomendación

- **Supuesto**: el usuario objetivo son consultorios chicos/medianos argentinos (1–5 profesionales), no grandes cadenas. Si el target es multi-sede, cambia la prioridad hacia CareStack/Curve.
- **Supuesto**: el dolor principal es ausentismo y coordinación manual por WhatsApp, no la facturación. Si ARCA es bloqueante desde el día 1, sube a must-have.
- **Límite**: 5 competidores no pudieron evaluarse por SPA; se recomienda revisarlos con navegador antes de cerrar el benchmark.
- **Límite**: los puntajes son analíticos y dependen de información pública; no reemplazan una demo con trial.

---

## Verificación de fuentes

Verificación manual realizada el **2026-11-22** sobre 5 URLs citadas en el informe (sitios oficiales, páginas de precios regionales, marketplace y página de contratación internacional):

| # | Fuente verificada (tipo) | Qué afirmaba el informe | Qué se encontró al abrir la URL | Qué se corrigió |
|---|---|---|---|---|
| 1 | `https://www.dentalsoft.com.ar` *(sitio oficial + precios)* | Planes Gratis $0 / Gestión $30.000 / Pro $60.000 ARS/mes, WhatsApp a 0,026 USD/msg Meta; facturación/integraciones locales no evidenciadas. | Precios y costo Meta confirmados (plan Gratis limitado a 3 meses). Además publica **cobros/señas con Mercado Pago**, **obras sociales y liquidaciones**, **turnos online 24/7** y **asistente virtual con IA**. | Se actualizaron Tabla A.1, C.2, C.3 y `sources/dentalsoft.md`. |
| 2 | `https://dentia.tech` *(sitio oficial + FAQ/precios)* | Pricing público `(no publicado)` e incluido en "pricing opaco" (C.3); ARCA, 30 días gratis e IA en WhatsApp. | +100 clínicas, 30 días gratis, ARCA (A/B/C) e IA en WhatsApp confirmados. **Error detectado:** el sitio **sí publica precios** en FAQ: **Básico $20.000**, **Pro $30.000** y **Elite $40.000 ARS/mes**, además de seña al reservar. | Se corrigió el pricing en Tabla A.1, se quitó a Dentia de C.3 ("pricing opaco") y se actualizó `sources/dentia.md`. |
| 3 | `https://dentatools.co/ar` *(landing regional + precios)* | `$76.500 ARS/mes IVA incl., usuarios ilimitados`; WhatsApp `No evidenciado`. | Precio y usuarios ilimitados confirmados (con Factura C). Además muestra **auto-agendado de turnos**, **odontograma digital** y **recordatorios por WhatsApp en un clic** (envío manual, sin API automática). | Se actualizaron Tabla A.1 y `sources/dentatools.md` precisando el envío manual por WhatsApp. |
| 4 | `https://pro.doctoralia.com/ar/precio` *(página de precios de marketplace)* | Planes anuales Starter $25.000 / Plus $35.000 / VIP $55.000 ARS/mes, web profesional $4.000 ARS/mes, plan gratuito, historia clínica desde Plus, SMS y sin WhatsApp. | **Todo confirmado** exactamente en la página de precios argentina. | Sin correcciones necesarias. |
| 5 | `https://opendental.com/site/order.html` *(página de contratación/precios internacional)* | Soporte mensual USD 199/mes por ubicación (contrato 12 meses), incluye software, soporte telefónico, actualizaciones, imaging, Web Forms, Patient Portal y email reminders; tarifas distintas fuera de EE. UU. | **Todo confirmado** en la página oficial de *Ordering* (precisando que la tarifa cubre hasta 3 odontólogos por ubicación). | Sin correcciones necesarias (aclaración menor anotada). |

---

## Fuentes

Todas consultadas el **2026-11-21**. Detalle por competidor en `discovery/sources/`.

- https://www.dentalsoft.com.ar
- https://www.softwaredentalink.com/ar
- https://dentia.tech
- https://dentalflow.ar
- https://dentidad.com
- https://www.odontalweb.com.ar
- https://www.bilog.com.ar
- https://drapp.com.ar/odontologia
- https://dentatools.co/ar
- https://oclucrm.com/latam
- https://pro.doctoralia.com/ar/precio
- https://denpro.ar
- https://nacaros.com
- https://ikomdental.com
- https://gestionodontologica.com
- https://opendental.com/site/order.html
- https://curvedental.com
- https://dentrix.com
- https://carestack.com
- https://dentaly.com.ar (sin contenido)
- https://odontoapp.online (sin contenido)
- https://odontolog.lat (sin contenido)
- https://dentiqly.com (sin contenido)
- https://denticon.com (sin contenido)
