# Preguntas Abiertas

## Inconsistencias y tensiones resueltas/detectadas

### IN-01 — Alcance D.3 de `market-research.md` vs. Presupuesto acotado en v1
**Documento A (`docs/discovery/market-research.md` §D.3)** sugiere incluir en v1: recordatorios automáticos por WhatsApp y cobro de seña online con Mercado Pago.
**Restricción real (`docs/discovery/discovery.md` §9)** establece presupuesto acotado y proveedor de WhatsApp/pagos sin definir.
**Resolución aplicada en KB**: En v1 se implementa WhatsApp asistido (`wa.me` 1 clic) y registro manual de señas/pagos, difiriendo Meta WhatsApp API y Mercado Pago a **v1.1** (`DD-02`, `DD-03`).

### IN-02 — Regla de límite por obra social (`discovery.md` §7) vs. Integración diferida (`market-research.md` §D.3)
**Documento A (`discovery.md` §7)** menciona "Límite de turnos por obra social/cobertura" como regla de negocio.
**Documento B (`market-research.md` §D.3)** difiere la integración con obras sociales por alto riesgo de error sin padrón conectado.
**Resolución aplicada en KB**: En v1 se modela el cupo mensual de referencia de manera **solo informativa** (`RN-OS-01`), sin bloqueo automático de agenda.

### IN-03 — Rutas de discovery en `.active-orchestrator-state.json`
**Nota**: Las rutas originales apuntaban a `discovery/...` pero los archivos reales viven en `docs/discovery/...` (ya corregido en `.active-orchestrator-state.json`). En los encabezados internos de `docs/discovery/discovery.md` y `docs/discovery/market-research.md` aún figura texto `discovery/sources/` como referencia relativa.

---

## Puntos "No evidenciado" / "(no publicado)" heredados del benchmark (`docs/discovery/market-research.md`)

Esta sección consolida **todos** los vacíos de evidencia pública detectados en el relevamiento de competidores para no basar decisiones de producto en supuestos no verificados:

### 1. Los 5 sistemas SPA sin contenido renderizado (requieren revisión con navegador headless / manual)
| Sistema | URL | Estado en benchmark | Qué falta relevar |
|---|---|---|---|
| **Dentaly** | `dentaly.com.ar` | Sin contenido renderizado (shell SPA) | Enfoque, turnos/WhatsApp, clínica dental, integración AR, pricing y trial |
| **OdontoApp** | `odontoapp.online` | Sin contenido renderizado (shell SPA) | Enfoque, turnos/WhatsApp, clínica dental, integración AR, pricing y trial |
| **OdontoLog** | `odontolog.lat` | Sin contenido renderizado (shell SPA) | Enfoque, turnos/WhatsApp, clínica dental, integración AR, pricing y trial |
| **Dentiqly** | `dentiqly.com` | Sin contenido renderizado (shell SPA) | Enfoque, turnos/WhatsApp, clínica dental, integración AR, pricing y trial |
| **Denticon** | `denticon.com` | Sin contenido renderizado (shell SPA) | Enfoque, turnos/WhatsApp, clínica dental, integración global, pricing y trial |

### 2. Brechas "No evidenciado" / "(no publicado)" en los 19 sistemas evaluados
- **Pricing opaco (`no publicado`)**: Dentalink, Dentidad, Odontal Web, Bilog, DentalFLOW, OCLÜ, DenPro, DrApp, IKOMDENTAL, Gestión Odontológica, Dentrix, Curve Dental y CareStack no publican precios abiertos (solo por cotización/contacto).
- **WhatsApp / IA (`No evidenciado`)**: Dentalink, Dentidad, Bilog, DenPro, DrApp, NacarOS, IKOMDENTAL y Gestión Odontológica no evidencian canal WhatsApp en sus sitios públicos; DentalFLOW lo anuncia como *"próximamente"*. Además, en **Dentia**, **Odontal Web ("Odi")** y **OCLÜ** la "IA" se comunica comercialmente sin documentar alcance, límites ni supervisión.
- **Integración local Argentina (`No evidenciado`)**: Dentalink, Odontal Web, Bilog, DrApp e IKOMDENTAL no evidencian integraciones locales AR (ARCA, Mercado Pago u obras sociales); OCLÜ no evidencia integración local AR (y ofrece DICOM como add-on); DenPro declara datos en UE sin integración AR; DentalFLOW anuncia integración local como no disponible aún.
- **Trial gratuito (`No evidenciado`)**: Dentalink, Dentatools, Odontal Web, Bilog, DentalFLOW, OCLÜ, DenPro y Gestión Odontológica no publican si ofrecen prueba gratuita sin cargo.
- **Profundidad clínica de Dentidad (`Básica, no evidenciada`)**: no hay evidencia pública suficiente sobre alcance de historia clínica/odontograma en Dentidad más allá del foco en turnos y seña con Mercado Pago.
- **Seguridad, portabilidad y multi-sede (`No evidenciado`)**: la mayoría de competidores locales no publica postura de seguridad, exportación/auditoría ni soporte multi-sede (solo Dentalink declara ISO 27001 y DenPro declara GDPR/datos en UE).

---

## Preguntas abiertas del proyecto (priorizadas)

| Prioridad | Pregunta | Impacto / Qué bloquea | Decisor |
|---|---|---|---|
| **Alta** | ¿Cuál será el proveedor concreto de VPS/hosting con datacenter en Argentina dentro del presupuesto del piloto? | Provisión de entorno staging/producción, backups y verificación de latencia (`DD-04`, `SU-05`) | Dueño / Tech Lead |
| **Alta** | ¿Qué campos exactos necesita administración en el archivo CSV/PDF para cargar facturas en ARCA y liquidar las obras sociales prioritarias del consultorio piloto? | Diseño final del exportador en `pagos/exportaciones` (`SU-02`) | Administración / Contador |
| **Alta** | ¿Qué cuenta de Google Cloud se usará para OAuth 2.0 de Google Calendar y se verificará la app para evitar límite de 100 usuarios/expiración de tokens en modo Testing? | Operación continua de `integraciones/google_calendar` en producción | Tech Lead / Dueño |
| **Media** | ¿Un odontólogo atiende siempre un único sillón por franja horaria o en algún procedimiento alterna entre dos sillones con asistente? | Confirmación de regla `RN-AG-03` vs flexibilidad excepcional en agenda interna (`SU-03`) | Odontólogo / Dueño |
| **Media** | ¿Qué nomenclatura y estados exactos se requieren en el "odontograma simple" (piezas permanentes + temporarias FDI, estados: sano, caries, obturado, ausente, corona, endodoncia, implante, a realizar)? | Schema JSONB de `odontogramas.piezas_json` y UI clínica (`US-011`) | Odontólogo/a |
| **Media** | ¿Qué obras sociales atiende el consultorio piloto hoy y cuál es el valor de referencia de cupo mensual (si aplica)? | Seed inicial de `obras_sociales` (`RN-OS-01`) | Administración |
| **Media** | ¿El valor por defecto de `anticipacion_minima_cancelacion_hs = 24` hs se ajusta a la política real del consultorio? | Configuración inicial de reserva pública (`RN-AG-06`) | Dueño / Recepción |
| **Baja** | ¿Se revisarán con navegador headless los 5 sitios SPA (`Dentaly`, `OdontoApp`, `OdontoLog`, `Dentiqly`, `Denticon`) antes de definir la estrategia comercial y el pricing en ARS para una futura etapa SaaS? | Cierre completo del benchmark de mercado (`discovery.md` §11) | Producto / Dueño |
| **Baja** | ¿Cuál será el modelo de pricing en ARS (plan único, por profesional o por sillón) si el proyecto avanza luego a multi-consultorio? | Roadmap post-MVP / comercialización (`discovery.md` §11) | Dueño / Producto |
