# Turnos Odontología — Base de Conocimiento

Base de conocimiento canónica del proyecto **Turnos Odontología**, generada a partir del relevamiento de mercado en [docs/discovery/](../docs/discovery/discovery.md) y las decisiones de alcance, arquitectura y producto definidas para la v1.

## Índice de Archivos

| Archivo | Contenido |
|---|---|
| [01_vision_y_objetivos.md](01_vision_y_objetivos.md) | Propósito, contexto competitivo en AR, objetivos por actor, alcance v1, diferido post-MVP y métricas |
| [02_descripcion_general.md](02_descripcion_general.md) | Stack tecnológico (FastAPI + PostgreSQL + React/TS), arquitectura general, integraciones y API REST |
| [03_actores_y_roles.md](03_actores_y_roles.md) | Los 5 actores, matriz RBAC (incluyendo bloqueo clínico estricto) y rutas públicas |
| [04_modelo_de_datos.md](04_modelo_de_datos.md) | Dominios, ERD, entidades con `consultorio_id`, constraints `btree_gist` y seed data |
| [05_reglas_de_negocio.md](05_reglas_de_negocio.md) | Reglas `RN-XX-NN`: duración variable, sillones/boxes, anti-solapamiento, RBAC clínico y auditoría |
| [06_funcionalidades.md](06_funcionalidades.md) | 6 épicas y 14 historias de usuario (`US-001` a `US-014`) con criterios de aceptación |
| [07_flujos_principales.md](07_flujos_principales.md) | 5 flujos end-to-end (reserva pública, `wa.me` + confirmación, agenda interna, clínica, caja/exportación) |
| [08_arquitectura_propuesta.md](08_arquitectura_propuesta.md) | Patrones, estructura de directorios, seguridad, residencia de datos en Argentina y variables de entorno |
| [09_decisiones_y_supuestos.md](09_decisiones_y_supuestos.md) | Decisiones (`DD-01`..`DD-07`, incluyendo ajustes vs. D.3) y supuestos (`SU-01`..`SU-05`) |
| [10_preguntas_abiertas.md](10_preguntas_abiertas.md) | Inconsistencias, puntos "No evidenciado" / 5 SPAs del benchmark y preguntas abiertas priorizadas |

## Quick Start para Desarrolladores

1. Entender el dominio y los permisos → [01_vision_y_objetivos.md](01_vision_y_objetivos.md), [03_actores_y_roles.md](03_actores_y_roles.md)
2. Entender los datos y constraints → [04_modelo_de_datos.md](04_modelo_de_datos.md)
3. Entender las reglas obligatorias → [05_reglas_de_negocio.md](05_reglas_de_negocio.md)
4. Entender la arquitectura y el despliegue en AR → [02_descripcion_general.md](02_descripcion_general.md), [08_arquitectura_propuesta.md](08_arquitectura_propuesta.md)
5. Implementar historias y flujos → [07_flujos_principales.md](07_flujos_principales.md), [06_funcionalidades.md](06_funcionalidades.md)
6. Revisar decisiones y pendientes antes de codificar → [09_decisiones_y_supuestos.md](09_decisiones_y_supuestos.md), [10_preguntas_abiertas.md](10_preguntas_abiertas.md)

## Resumen Ejecutivo

Sistema web responsive / PWA para consultorios odontológicos chicos de Argentina (2–5 profesionales), pensado para un piloto inicial pero modelado desde el arranque con `consultorio_id` para escalar a multi-consultorio. Combina agenda sin solapamientos por profesional y por sillón/box, reserva online por link público, sincronización unidireccional con Google Calendar, recordatorios asistidos por `wa.me`, historia clínica/odontograma de acceso exclusivo para odontólogos, presupuestos versionados y registro manual de señas/pagos con exportación CSV/PDF, desplegado con Docker en infraestructura alojada en Argentina.
