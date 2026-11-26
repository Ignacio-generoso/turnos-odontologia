# Informe de Discovery — Sistema de Gestión de Turnos y Agenda Odontológica

**UNIVERSIDAD TECNOLÓGICA NACIONAL · UTN**  
*Investigación de mercado, matriz comparativa, análisis competitivo y definición de MVP para consultorios odontológicos en Argentina*

- **Proyecto:** Turnos Odontología (`turnos-odontologia`)
- **Materia:** Desarrollo de Software — Comisión 3K10
- **Integrantes:** Vega Agustina · Moreno Andrés · Generoso Ignacio · Basabe Tomás · Chirino Daniel
- **Fecha:** 22 de noviembre de 2026

---

## Resumen Ejecutivo

### Qué se investigó

Se realizó una investigación de mercado exhaustiva sobre **24 sistemas de gestión y turnos odontológicos** con foco prioritario en **Argentina**, ampliado a **Latinoamérica** y a **referencias internacionales** (EE. UU./Europa) para benchmark funcional y de experiencia de usuario. De los 24 sistemas relevados, **19 presentaron evidencia pública verificable** en sitios oficiales, páginas de precios y documentación (15 en Argentina/LATAM y 4 internacionales), mientras que **5 sitios** devolvieron únicamente un shell SPA sin contenido renderizado y quedaron consignados explícitamente sin evidencia. En todo el relevamiento se distinguió entre **funcionalidad comprobada** y **afirmación comercial del proveedor**, marcando todo dato sin respaldo público como `No evidenciado` o `(no publicado)`.

### Principales hallazgos

- **Mercado fragmentado sin ganador integral en Argentina:** los sistemas mejor puntuados en el mercado local resuelven la agenda combinada con **una fortaleza aislada** —**Dentia** (4,05/5) destaca en facturación electrónica ARCA e IA en WhatsApp; **Dentalink** (3,75/5) en profundidad clínica e ISO 27001 declarada; **DentalSoft** (3,65/5) en transparencia de precios en ARS y cobros con Mercado Pago; y **Dentidad** en seña anti-ausentismo—, pero **ningún competidor local reúne simultáneamente profundidad clínica, cumplimiento fiscal/operativo argentino y excelente experiencia de paciente**.
- **Brechas críticas detectadas:** (1) alta opacidad de precios en la mayoría de los proveedores; (2) integración local incompleta con ARCA y obras sociales; (3) WhatsApp ofrecido como add-on con costo por mensaje de Meta (ej. USD 0,026/msg en DentalSoft) o anunciado como *"próximamente"*; (4) escasa transparencia sobre seguridad, trazabilidad y exportación de datos; y (5) uso comercial de "IA" sin documentar alcance ni supervisión.
- **Hallazgo clave en verificación de fuentes:** al auditar personalmente 5 fuentes oficiales el 2026-11-22, se detectó que **Dentia** sí publicaba sus precios en ARS en su sección de preguntas frecuentes (Básico \$20.000 / Pro \$30.000 / Elite \$40.000 ARS/mes), que **DentalSoft** también evidenciaba Mercado Pago y obras sociales, y que **Dentatools** resolvía WhatsApp mediante envío manual en 1 clic sin API paga.

### MVP recomendado

Se recomienda construir un producto orientado a **consultorios odontológicos chicos de Argentina (2 a 5 profesionales)** que sufren ausentismo, dobles reservas y sobrecarga administrativa en la coordinación por WhatsApp:

- **Imprescindibles (v1):** agenda multi-profesional (día/semana) sin solapamientos por profesional ni por sillón/box; reserva online 24/7 por link público con confirmación/cancelación; recordatorios por WhatsApp con opt-in y control de costos; ficha clínica con odontograma simple y plan de tratamiento/presupuesto; registro de pagos/señas; roles y permisos (dueño, odontólogo, recepción); y exportación/auditoría básica.
- **Diferenciadores:** WhatsApp transparente sin costos sorpresa, estrategia anti-ausentismo (seña + lista de espera), precios claros en ARS y trazabilidad de versiones en odontograma y presupuestos.
- **Etapas posteriores (post-MVP):** facturación electrónica directa con ARCA, integración online con padrones de obras sociales, IA conversacional avanzada, imágenes DICOM, multi-sede y app móvil nativa (priorizando PWA en v1).

---

## A. Tabla Comparativa de Sistemas

**Criterio de evidencia:** solo se afirma lo visible públicamente en sitios oficiales, páginas de precios o documentación pública. Todo atributo sin respaldo público se consigna como `No evidenciado` o `(no publicado)`. Las afirmaciones comerciales del proveedor se distinguen explícitamente de la funcionalidad comprobada.

**Límite metodológico:** 5 sitios (Dentaly, OdontoApp, OdontoLog, Dentiqly, Denticon) devolvieron un shell SPA sin contenido renderizado y no pudieron evaluarse sin navegador headless.

### A.1 Mercado argentino y LATAM (ordenado por relevancia para Argentina)

| # | Sistema (Proveedor) | País / Segmento | Enfoque principal | Turnos / Automatización | Clínica dental | WhatsApp / IA | Integración local AR | Pricing público | Trial | Fuente y fecha |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **DentalSoft** (DentalSoft) | Argentina · Consultorios y clínicas | Gestión integral de consultorio | Comprobado: agenda, turnos online 24/7 + recordatorios | Historia clínica, odontograma | WhatsApp (costo Meta 0,026 USD/msg) + asistente IA (afirmación comercial) | ARS, Mercado Pago (señas) y obras sociales; ARCA: No evidenciado | Gratis (3 meses) / $30.000 / $60.000 ARS/mes | Plan gratis (3 meses) | https://www.dentalsoft.com.ar · 2026-11-22 |
| 2 | **Dentalink** (Dentalink) | Chile / LATAM · Clínicas y consultorios | Software dental cloud | Agenda | Ficha clínica, presupuestos | No evidenciado | No evidenciado | (no publicado) — cotización | No evidenciado | https://www.softwaredentalink.com/ar · 2026-11-21 |
| 3 | **Dentia** (Dentia) | Argentina · Consultorios y clínicas | Gestión + automatización | Comprobado: turnos + seña al reservar | Historia clínica, odontograma, IA clínica (afirmación comercial) | WhatsApp con IA (plan Elite) | Comprobado: ARCA (facturación electrónica A/B/C) | Básico $20.000 / Pro $30.000 / Elite $40.000 ARS/mes | 30 días | https://dentia.tech · 2026-11-22 |
| 4 | **Dentatools** (Dentatools) | Argentina / LATAM · Consultorios | Gestión cloud | Comprobado: agenda + auto-agendado | Comprobado: historia clínica, odontograma, presupuestos | Comprobado: WhatsApp en 1 clic (envío manual, sin API) | Cobros en ARS (Factura C suscripción) | $76.500 ARS/mes IVA incl., usuarios ilimitados | No evidenciado | https://dentatools.co/ar · 2026-11-22 |
| 5 | **Doctoralia PRO** (Doctoralia / Docplanner Group) | España / 13 países (incl. AR) · Profesionales y clínicas | Marketplace + agenda | Comprobado: reserva online, recordatorios | Historia clínica desde plan Plus | SMS; WhatsApp: No evidenciado | Precio en ARS; ARCA/obras sociales: No evidenciado | Starter $25.000 / Plus $35.000 / VIP $55.000 ARS/mes (anual) | Versión gratuita | https://pro.doctoralia.com/ar/precio · 2026-11-21 |
| 6 | **Dentidad** (Dentidad) | Argentina · Consultorios | Turnos + seña anti-ausentismo | Turnos | Básica (No evidenciado alcance completo) | No evidenciado | Mercado Pago (seña) | (no publicado) | 14 días | https://dentidad.com · 2026-11-21 |
| 7 | **Odontal Web** (Odontal Web) | Argentina · Consultorios | Gestión + asistente IA | Turnos | Módulos clínicos | IA "Odi" (afirmación comercial); sin costo por mensaje declarado | No evidenciado | (no publicado) | No evidenciado | https://www.odontalweb.com.ar · 2026-11-21 |
| 8 | **Bilog** (Bilog) | Argentina · Consultorios | Gestión de consultorios | Turnos | Módulos clínicos/administrativos | No evidenciado | No evidenciado | (no publicado) | No evidenciado | https://www.bilog.com.ar · 2026-11-21 |
| 9 | **DentalFLOW** (DentalFLOW) | Argentina (Río Negro) · Consultorios | Gestión de consultorio | Turnos | Módulos de consultorio | WhatsApp y obras sociales anunciados "próximamente" | Anunciada, no disponible | (no publicado) | No evidenciado | https://dentalflow.ar · 2026-11-21 |
| 10 | **OCLÜ** (OCLÜ) | Argentina / LATAM · Clínicas | CRM all-in-one | Agenda + seguimiento comercial | Limitada (enfoque CRM) | IA "OCLÜ IA" (afirmación comercial) | No evidenciado; DICOM como add-on | (no publicado) | No evidenciado | https://oclucrm.com/latam · 2026-11-21 |
| 11 | **DenPro** (DenPro) | Internacional (datos UE/GDPR) · Consultorios | Gestión odontológica | Turnos | Módulos clínicos/administrativos | No evidenciado | No evidenciado; datos alojados en UE | (no publicado) | No evidenciado | https://denpro.ar · 2026-11-21 |
| 12 | **DrApp** (DrApp) | Argentina · Multi-especialidad | Salud multi-especialidad | Agenda | Baja (no exclusivo dental) | No evidenciado | No evidenciado | (no publicado) | 15 días | https://drapp.com.ar/odontologia · 2026-11-21 |
| 13 | **NacarOS** (NacarOS) | LATAM · Consultorios chicos | Gestión PWA | Turnos | Básica | No evidenciado | Precio en USD | Gratis hasta 20 pacientes activos; Pro USD 14,99/mes (11,99 anual) | Plan gratis | https://nacaros.com · 2026-11-21 |
| 14 | **IKOMDENTAL** (IKOMDENTAL) | LATAM / US / CA / ES (23 países) · Clínicas | Gestión dental | Turnos | Módulos clínicos/administrativos | No evidenciado | No evidenciado | (no publicado) | 30 días | https://ikomdental.com · 2026-11-21 |
| 15 | **Gestión Odontológica** (Gestión Odontológica) | Colombia · Consultorios | Gestión + contabilidad | Turnos | Módulos clínicos | No evidenciado | Nómina electrónica colombiana (sin AR) | (no publicado) | No evidenciado | https://gestionodontologica.com · 2026-11-21 |

### A.2 Referencias internacionales (benchmark funcional, sin competencia directa en Argentina)

| # | Sistema (Proveedor) | Mercado | Enfoque | Funcionalidades comprobadas clave | Pricing público | Fuente y fecha |
|---|---|---|---|---|---|---|
| 16 | **Open Dental** (Open Dental Software, Inc.) | EE. UU. | Software configurable / ecosistema abierto | Comprobado: alta configurabilidad, cientos de bridges, imaging, Web Forms, Patient Portal, email reminders | USD 199/mes por sede (contrato 12 meses; hasta 3 odontólogos por ubicación) | https://opendental.com/site/order.html · 2026-11-21 |
| 17 | **Curve Dental** (Curve Dental) | EE. UU. / CA | Cloud-first | Gestión clínica y administrativa en nube; I+D declarada USD 200M (afirmación comercial) | (no publicado) | https://curvedental.com · 2026-11-21 |
| 18 | **Dentrix** (Henry Schein One) | EE. UU. | Suite integral | Suite clínica, administrativa e imaging | (no publicado) | https://dentrix.com · 2026-11-21 |
| 19 | **CareStack** (CareStack) | US / UK / AU | Cloud todo-en-uno para grupos | Multi-sede, consolidación de herramientas | (no publicado) | https://carestack.com · 2026-11-21 |

### A.3 Sistemas sin evidencia pública evaluable (shell SPA)

| Sistema | Empresa proveedora | URL oficial | Resultado de consulta | Fecha de consulta |
|---|---|---|---|---|
| Dentaly | Dentaly | https://dentaly.com.ar | Sin contenido renderizado (`No evidenciado`) | 2026-11-21 |
| OdontoApp | OdontoApp | https://odontoapp.online | Sin contenido renderizado (`No evidenciado`) | 2026-11-21 |
| OdontoLog | OdontoLog | https://odontolog.lat | Sin contenido renderizado (`No evidenciado`) | 2026-11-21 |
| Dentiqly | Dentiqly | https://dentiqly.com | Sin contenido renderizado (`No evidenciado`) | 2026-11-21 |
| Denticon | Denticon | https://denticon.com | Sin contenido renderizado (`No evidenciado`) | 2026-11-21 |

---

## B. Matriz de Puntuación (0 a 5)

### Nota metodológica

- **Pesos aplicados:** Gestión de turnos y automatización **25 %** · Funcionalidad odontológica clínica **20 %** · Integraciones locales y WhatsApp **15 %** · Administración, cobros y facturación **15 %** · Experiencia del paciente **10 %** · Seguridad, exportación y trazabilidad **10 %** · Precio y facilidad de adopción **5 %**.
- **Significado de las notas:** `0` = ausente o `No evidenciado`; `1–2` = cobertura mínima o sin integración local; `3` = presente pero no diferencial; `4` = cobertura sólida comprobada; `5` = diferencial comprobado en su categoría.
- **Tratamiento de datos "No evidenciado":** cuando un atributo no pudo comprobarse públicamente, no se asumió su existencia; se puntuó de forma conservadora (0 a 2 según lo estrictamente verificable en el sitio) para no inflar puntajes por deducción. La nota representa un juicio analítico sobre evidencia pública y no una prueba en demo.

| Sistema | Turnos (25%) | Clínica (20%) | Local+WA (15%) | Admin/Cobros (15%) | Paciente (10%) | Seguridad (10%) | Precio (5%) | **Total Ponderado (0–5)** | **Índice (0–100)** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
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

**Lectura de la matriz:** los mejor puntuados en Argentina combinan agenda sólida con **una** integración local fuerte (Dentia con ARCA + IA; DentalSoft con pricing + Mercado Pago; Dentidad con seña online), pero ninguno alcanza excelencia simultánea en clínica, compliance local y experiencia de paciente.

---

## C. Análisis Competitivo

### C.1 Funcionalidades que ya son estándar de mercado (table stakes)

1. Agenda de turnos con vista diaria/semanal y asignación por profesional.
2. Ficha y registro administrativo del paciente.
3. Historia clínica odontológica básica.
4. Presupuestos y planes de tratamiento.
5. Recordatorios de turnos (email, SMS o WhatsApp).
6. Gestión de cobros y estado de cuenta.
7. Roles básicos (dueño, odontólogo, recepción).
8. Reportes operativos simples.

### C.2 Diferenciadores reales observados (no marketing)

| Diferenciador | Proveedor que lo evidencia | Fuente |
|---|---|---|
| **Facturación electrónica ARCA (A/B/C)** | Dentia | https://dentia.tech |
| **WhatsApp con IA** | Dentia (plan Elite), Odontal Web ("Odi"), DentalSoft | https://dentia.tech · https://www.odontalweb.com.ar · https://www.dentalsoft.com.ar |
| **Seña online con Mercado Pago** | Dentidad, DentalSoft | https://dentidad.com · https://www.dentalsoft.com.ar |
| **Precio plano con usuarios ilimitados** | Dentatools | https://dentatools.co/ar |
| **Certificación ISO 27001 declarada** | Dentalink | https://www.softwaredentalink.com/ar |
| **Alojamiento en UE / cumplimiento GDPR** | DenPro | https://denpro.ar |
| **Marketplace con demanda de pacientes** | Doctoralia PRO | https://pro.doctoralia.com/ar/precio |
| **Alta configurabilidad y bridges externos** | Open Dental | https://opendental.com/site/order.html |

### C.3 Vacíos frecuentes del mercado argentino

1. **Pricing opaco:** la mayoría no publica precios abiertos (Dentalink, Dentidad, Odontal Web, Bilog, DentalFLOW, OCLÜ, DenPro, DrApp, IKOMDENTAL). *(Corregido tras verificación: Dentia sí publica sus planes en ARS en sus FAQ).*
2. **Integración local incompleta:** ARCA, obras sociales y convenios rara vez están resueltos de punta a punta (DentalFLOW los anuncia como "próximamente").
3. **WhatsApp como add-on costoso:** DentalSoft traslada el costo por mensaje de Meta (USD 0,026/msg), penalizando a consultorios con alto volumen.
4. **Anti-ausentismo débil:** pocos competidores locales combinan seña online con lista de espera automática (Doctoralia la restringe al plan VIP).
5. **Tensión entre profundidad clínica y simplicidad:** los sistemas locales priorizan agenda/administración y los internacionales priorizan clínica sin adaptación fiscal local.
6. **Seguridad y portabilidad poco visibles:** salvo Dentalink (ISO 27001) y DenPro (GDPR), no se comunica postura de seguridad, auditoría ni exportación de datos.
7. **IA como discurso comercial:** Dentia, Odontal Web y OCLÜ mencionan "IA" sin documentar alcance, límites ni supervisión clínica/humana.
8. **Soporte multi-sede:** poco evidenciado en los productos argentinos; dominado por jugadores internacionales (CareStack, Curve, Dentrix).

### C.4 Oportunidades de innovación para un nuevo sistema

1. **WhatsApp con costo transparente y opt-in:** flujo unificado de confirmación y recordatorio, evitando sorpresas por mensaje (ej. envío asistido en v1 y API Meta opcional en v1.1).
2. **Anti-no-show combinado:** seña + lista de espera automática + recordatorio escalonado.
3. **Odontograma + presupuesto con trazabilidad:** versionado explícito del plan, aceptación y registro de auditoría.
4. **Cumplimiento local integrado:** ARCA, medios de pago y obras sociales articulados en un mismo flujo operativo.
5. **Portabilidad y seguridad explícitas:** exportación completa (CSV/PDF), auditoría de acciones y residencia de datos en Argentina.
6. **PWA multi-dispositivo:** operación fluida en escritorio para recepción y celular para odontólogos sin costo de app nativa.
7. **Precio local claro en ARS:** planes públicos y previsibles frente a la opacidad predominante.

---

## D. Recomendación Final

### D.1 Cinco competidores prioritarios para analizar mediante demo

| Prioridad | Competidor | Motivo de selección |
|---|---|---|
| 1 | **DentalSoft** | Único competidor local con pricing público completo, Mercado Pago y obras sociales; benchmark de costo WhatsApp. |
| 2 | **Dentalink** | Referencia LATAM en profundidad clínica y comunicación de seguridad (ISO 27001). |
| 3 | **Dentia** | Mejor combinación evidenciada en Argentina de IA en WhatsApp + facturación electrónica ARCA. |
| 4 | **Dentatools** | Benchmark de precio plano en ARS con usuarios ilimitados y WhatsApp manual en 1 clic. |
| 5 | **Dentidad** | Foco específico en seña online con Mercado Pago como mecanismo anti-ausentismo. |

*Comodín de análisis:* **Doctoralia PRO** — aunque no es un sistema clínico integral, marca el estándar de experiencia de reserva online y autogestión del paciente.

### D.2 Tres productos de referencia para experiencia de usuario (UX)

1. **Curve Dental:** claridad visual y modernidad de la interfaz cloud-first.
2. **Open Dental:** profundidad y configurabilidad del flujo clínico odontológico.
3. **Doctoralia PRO:** fricción mínima en reserva online, recordatorios y autogestión del paciente.

### D.3 MVP sugerido

| Categoría | Funcionalidades |
|---|---|
| **Imprescindible (v1)** | 1. Agenda multi-profesional (día/semana) sin solapamientos por profesional ni por sillón/box.<br>2. Reserva online por link público, con confirmación y cancelación controlada.<br>3. Recordatorios por WhatsApp con opt-in y control de costo.<br>4. Ficha del paciente + odontograma simple + plan de tratamiento/presupuesto.<br>5. Registro de señas y pagos (manual en v1; pasarela Mercado Pago en v1.1).<br>6. Roles y permisos estrictos (dueño, odontólogo, recepción, administración).<br>7. Exportación de datos (CSV/PDF) y auditoría básica. |
| **Diferenciador** | • WhatsApp transparente sin costos ocultos por mensaje.<br>• Estrategia anti-ausentismo (seña + lista de espera).<br>• Precio local transparente en ARS.<br>• Odontograma y presupuestos con trazabilidad de versiones. |
| **Etapas posteriores (post-MVP)** | • Facturación electrónica directa con ARCA.<br>• Integración online con padrones de obras sociales.<br>• IA conversacional avanzada.<br>• Gestión de imágenes/DICOM.<br>• Multi-sede y analítica avanzada.<br>• App móvil nativa (priorizando PWA en v1). |

### D.4 Supuestos y límites

- **Target inicial:** consultorios chicos/medianos argentinos (2–5 profesionales), no grandes cadenas.
- **Dolor principal:** ausentismo y coordinación manual por WhatsApp/teléfono, más que facturación electrónica automatizada en el día 1.
- **Límites del relevamiento:** 5 sitios SPA no pudieron evaluarse sin navegador headless y los puntajes reflejan únicamente evidencia pública previa a demos.

---

## Verificación de Fuentes

El **2026-11-22** se abrieron y comprobaron personalmente **5 fuentes** de distinto tipo (sitio oficial, FAQ/precios, landing regional, marketplace y página de contratación internacional):

| # | URL verificada (tipo) | Qué afirmaba el informe inicial | Qué se encontró al abrir la URL | Qué se corrigió |
|---|---|---|---|---|
| 1 | `https://www.dentalsoft.com.ar` *(sitio oficial + precios)* | Planes Gratis $0 / Gestión $30.000 / Pro $60.000 ARS/mes, WhatsApp a 0,026 USD/msg Meta; integraciones locales no evidenciadas. | Precios y costo Meta confirmados (plan Gratis limitado a 3 meses). Además publica **cobros/señas con Mercado Pago, obras sociales y liquidaciones, turnos online 24/7 y asistente virtual con IA**. | Se actualizaron Tabla A.1, C.2, C.3 y `sources/dentalsoft.md`. |
| 2 | `https://dentia.tech` *(sitio oficial + FAQ/precios)* | Pricing público `(no publicado)` e incluido en "pricing opaco" (C.3); ARCA, 30 días gratis e IA en WhatsApp. | +100 clínicas, 30 días gratis, ARCA (A/B/C) e IA en WhatsApp confirmados. **Error detectado: el sitio sí publica precios en su FAQ (Básico $20.000, Pro $30.000, Elite $40.000 ARS/mes)** y seña al reservar. | Se corrigió el pricing en Tabla A.1, se quitó a Dentia de "pricing opaco" (C.3) y se actualizó `sources/dentia.md`. |
| 3 | `https://dentatools.co/ar` *(landing regional + precios)* | `$76.500 ARS/mes IVA incl., usuarios ilimitados`; WhatsApp `No evidenciado`. | Precio y usuarios ilimitados confirmados (con Factura C). Además evidencia **auto-agendado de turnos, odontograma digital y recordatorios por WhatsApp en un clic** (envío manual, sin API). | Se actualizaron Tabla A.1 y `sources/dentatools.md` precisando el envío manual por WhatsApp. |
| 4 | `https://pro.doctoralia.com/ar/precio` *(página de precios de marketplace)* | Planes anuales Starter $25.000 / Plus $35.000 / VIP $55.000 ARS/mes, web profesional $4.000 ARS/mes, plan gratuito, historia clínica desde Plus, SMS y sin WhatsApp. | **Todo confirmado** exactamente en la página de precios argentina. | Sin correcciones necesarias. |
| 5 | `https://opendental.com/site/order.html` *(página de contratación internacional)* | Soporte mensual USD 199/mes por ubicación (contrato 12 meses), software, soporte telefónico, actualizaciones, imaging, Web Forms, Patient Portal y email reminders. | **Todo confirmado** en la página oficial de *Ordering* (precisando que la tarifa cubre hasta 3 odontólogos por ubicación). | Sin correcciones necesarias (aclaración menor incorporada). |

---

## Referencias Completas

Todas las fuentes fueron relevadas el **2026-11-21** (con re-verificación de las 5 fuentes auditadas el **2026-11-22**). Las fichas individuales por competidor se encuentran en `docs/discovery/sources/`.

1. DentalSoft — https://www.dentalsoft.com.ar (consultada 2026-11-22)
2. Dentalink — https://www.softwaredentalink.com/ar (consultada 2026-11-21)
3. Dentia — https://dentia.tech (consultada 2026-11-22)
4. Dentatools — https://dentatools.co/ar (consultada 2026-11-22)
5. Doctoralia PRO — https://pro.doctoralia.com/ar/precio (consultada 2026-11-21)
6. Dentidad — https://dentidad.com (consultada 2026-11-21)
7. Odontal Web — https://www.odontalweb.com.ar (consultada 2026-11-21)
8. Bilog — https://www.bilog.com.ar (consultada 2026-11-21)
9. DentalFLOW — https://dentalflow.ar (consultada 2026-11-21)
10. OCLÜ — https://oclucrm.com/latam (consultada 2026-11-21)
11. DenPro — https://denpro.ar (consultada 2026-11-21)
12. DrApp — https://drapp.com.ar/odontologia (consultada 2026-11-21)
13. NacarOS — https://nacaros.com (consultada 2026-11-21)
14. IKOMDENTAL — https://ikomdental.com (consultada 2026-11-21)
15. Gestión Odontológica — https://gestionodontologica.com (consultada 2026-11-21)
16. Open Dental — https://opendental.com/site/order.html (consultada 2026-11-22)
17. Curve Dental — https://curvedental.com (consultada 2026-11-21)
18. Dentrix — https://dentrix.com (consultada 2026-11-21)
19. CareStack — https://carestack.com (consultada 2026-11-21)
20. Dentaly — https://dentaly.com.ar (consultada 2026-11-21, sin contenido renderizado)
21. OdontoApp — https://odontoapp.online (consultada 2026-11-21, sin contenido renderizado)
22. OdontoLog — https://odontolog.lat (consultada 2026-11-21, sin contenido renderizado)
23. Dentiqly — https://dentiqly.com (consultada 2026-11-21, sin contenido renderizado)
24. Denticon — https://denticon.com (consultada 2026-11-21, sin contenido renderizado)
