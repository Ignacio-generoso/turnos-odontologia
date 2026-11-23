"""Tests automatizados por escenario para el change `crear-turno-sin-solapamientos`.

Todos los datos de pacientes, profesionales y teléfonos utilizados en este módulo
son 100 % ficticios en cumplimiento de la regla de dominio de AGENTS.md.
"""

from __future__ import annotations

from datetime import datetime, time, timedelta, timezone
from decimal import Decimal
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from src.api.app import create_app
from src.domain.models import (
    BloqueoAgenda,
    Consultorio,
    CrearTurnoInput,
    DisponibilidadProfesional,
    EstadoTurno,
    FueraDeDisponibilidadError,
    Paciente,
    PermisoDenegadoError,
    Prestacion,
    RecursoInactivoError,
    RecursoNoEncontradoError,
    RolUsuario,
    Sillon,
    SolapamientoProfesionalError,
    SolapamientoSillonError,
    Turno,
    Usuario,
)
from src.domain.services import AgendaTurnosService, RepositorioAgendaMemoria

TZ_AR = timezone(timedelta(hours=-3))


def ar_dt(year: int, month: int, day: int, hour: int, minute: int) -> datetime:
    """Construye una fecha timezone-aware en horario de Argentina (-03:00)."""
    return datetime(year, month, day, hour, minute, tzinfo=TZ_AR)


@pytest.fixture()
def entorno_consultorio() -> dict[str, object]:
    """Crea un consultorio piloto ficticio completo con dos odontólogos y dos sillones."""
    repo = RepositorioAgendaMemoria()

    consultorio = Consultorio(
        nombre="Consultorio Piloto Ficticio",
        slug="consultorio-piloto",
        zona_horaria="America/Argentina/Buenos_Aires",
    )
    otro_consultorio = Consultorio(
        nombre="Consultorio Externo Ficticio",
        slug="consultorio-externo",
        zona_horaria="America/Argentina/Buenos_Aires",
    )
    repo.consultorios[consultorio.id] = consultorio
    repo.consultorios[otro_consultorio.id] = otro_consultorio

    recepcion = Usuario(
        consultorio_id=consultorio.id,
        nombre_completo="Laura Recepción (Ficticio)",
        email="recepcion@ejemplo-ficticio.test",
        roles={RolUsuario.RECEPCION},
    )
    admin_solo = Usuario(
        consultorio_id=consultorio.id,
        nombre_completo="Carlos Administración (Ficticio)",
        email="admin@ejemplo-ficticio.test",
        roles={RolUsuario.ADMINISTRACION},
    )
    dra_garcia = Usuario(
        consultorio_id=consultorio.id,
        nombre_completo="Dra. Sofía García (Ficticio)",
        email="sgarcia@ejemplo-ficticio.test",
        roles={RolUsuario.ODONTOLOGO},
        matricula_profesional="MN-00001",
    )
    dr_perez = Usuario(
        consultorio_id=consultorio.id,
        nombre_completo="Dr. Martín Pérez (Ficticio)",
        email="mperez@ejemplo-ficticio.test",
        roles={RolUsuario.ODONTOLOGO},
        matricula_profesional="MN-00002",
    )
    usuario_inactivo = Usuario(
        consultorio_id=consultorio.id,
        nombre_completo="Usuario Baja (Ficticio)",
        email="baja@ejemplo-ficticio.test",
        roles={RolUsuario.ODONTOLOGO},
        activo=False,
    )
    for usr in (recepcion, admin_solo, dra_garcia, dr_perez, usuario_inactivo):
        repo.usuarios[usr.id] = usr

    sillon_1 = Sillon(consultorio_id=consultorio.id, nombre="Sillón 1")
    sillon_2 = Sillon(consultorio_id=consultorio.id, nombre="Sillón 2")
    sillon_otro_consultorio = Sillon(consultorio_id=otro_consultorio.id, nombre="Sillón Externo")
    for s in (sillon_1, sillon_2, sillon_otro_consultorio):
        repo.sillones[s.id] = s

    limpieza = Prestacion(
        consultorio_id=consultorio.id,
        nombre="Limpieza",
        duracion_minutos=40,
        precio_referencia_ars=Decimal("25000.00"),
    )
    consulta = Prestacion(
        consultorio_id=consultorio.id,
        nombre="Consulta",
        duracion_minutos=30,
        precio_referencia_ars=Decimal("18000.00"),
    )
    for p in (limpieza, consulta):
        repo.prestaciones[p.id] = p

    paciente_1 = Paciente(
        consultorio_id=consultorio.id,
        nombre="Paciente Prueba",
        apellido="Uno",
        dni="99000001",
        telefono_whatsapp="+5491100000001",
        opt_in_whatsapp=True,
    )
    paciente_2 = Paciente(
        consultorio_id=consultorio.id,
        nombre="Paciente Prueba",
        apellido="Dos",
        dni="99000002",
        telefono_whatsapp="+5491100000002",
        opt_in_whatsapp=False,
    )
    repo.pacientes[paciente_1.id] = paciente_1
    repo.pacientes[paciente_2.id] = paciente_2

    # Lunes (dia_semana = 0): 2026-11-23 es lunes
    repo.disponibilidades.extend(
        [
            DisponibilidadProfesional(
                consultorio_id=consultorio.id,
                profesional_id=dra_garcia.id,
                dia_semana=0,
                hora_inicio=time(9, 0),
                hora_fin=time(13, 0),
                sillon_preferido_id=sillon_1.id,
            ),
            DisponibilidadProfesional(
                consultorio_id=consultorio.id,
                profesional_id=dr_perez.id,
                dia_semana=0,
                hora_inicio=time(9, 0),
                hora_fin=time(13, 0),
                sillon_preferido_id=sillon_2.id,
            ),
        ]
    )

    app = create_app(repo)
    client = TestClient(app)

    return {
        "repo": repo,
        "service": AgendaTurnosService(repo),
        "client": client,
        "consultorio": consultorio,
        "recepcion": recepcion,
        "admin_solo": admin_solo,
        "dra_garcia": dra_garcia,
        "dr_perez": dr_perez,
        "usuario_inactivo": usuario_inactivo,
        "sillon_1": sillon_1,
        "sillon_2": sillon_2,
        "sillon_otro_consultorio": sillon_otro_consultorio,
        "limpieza": limpieza,
        "consulta": consulta,
        "paciente_1": paciente_1,
        "paciente_2": paciente_2,
    }


def test_escenario_1_creacion_exitosa_con_duracion_calculada_y_auditoria(
    entorno_consultorio: dict[str, object],
) -> None:
    """Escenario 1 (Camino feliz): crea turno, calcula fin=10:40, genera token y auditoría."""
    client: TestClient = entorno_consultorio["client"]  # type: ignore[assignment]
    repo: RepositorioAgendaMemoria = entorno_consultorio["repo"]  # type: ignore[assignment]
    recepcion: Usuario = entorno_consultorio["recepcion"]  # type: ignore[assignment]
    dra_garcia: Usuario = entorno_consultorio["dra_garcia"]  # type: ignore[assignment]
    sillon_1: Sillon = entorno_consultorio["sillon_1"]  # type: ignore[assignment]
    limpieza: Prestacion = entorno_consultorio["limpieza"]  # type: ignore[assignment]
    paciente_1: Paciente = entorno_consultorio["paciente_1"]  # type: ignore[assignment]

    health = client.get("/api/v1/health")
    assert health.status_code == 200
    assert health.json() == {"status": "ok"}

    resp = client.post(
        "/api/v1/turnos",
        headers={"X-Usuario-Id": str(recepcion.id)},
        json={
            "paciente_id": str(paciente_1.id),
            "profesional_id": str(dra_garcia.id),
            "sillon_id": str(sillon_1.id),
            "prestacion_id": str(limpieza.id),
            "inicio": ar_dt(2026, 11, 23, 10, 0).isoformat(),
            "observaciones_agenda": "Control semestral ficticio",
        },
    )

    assert resp.status_code == 201
    data = resp.json()
    assert data["estado"] == "reservado"
    assert data["origen"] == "interno"
    assert data["duracion_minutos"] == 40
    assert datetime.fromisoformat(data["fin"]) == ar_dt(2026, 11, 23, 10, 40)
    assert len(data["token_publico_hash"]) == 64

    assert len(repo.turnos) == 1
    assert len(repo.auditoria) == 1
    assert repo.auditoria[0].accion == "crear"
    assert repo.auditoria[0].entidad == "turno"
    assert len(repo.eventos_emitidos) == 1


def test_escenario_2_rechazo_solapamiento_mismo_profesional_distinto_sillon(
    entorno_consultorio: dict[str, object],
) -> None:
    """Escenario 2 (Error RN-AG-03): mismo profesional no puede atender en dos sillones a la vez."""
    client: TestClient = entorno_consultorio["client"]  # type: ignore[assignment]
    repo: RepositorioAgendaMemoria = entorno_consultorio["repo"]  # type: ignore[assignment]
    recepcion: Usuario = entorno_consultorio["recepcion"]  # type: ignore[assignment]
    dra_garcia: Usuario = entorno_consultorio["dra_garcia"]  # type: ignore[assignment]
    sillon_1: Sillon = entorno_consultorio["sillon_1"]  # type: ignore[assignment]
    sillon_2: Sillon = entorno_consultorio["sillon_2"]  # type: ignore[assignment]
    limpieza: Prestacion = entorno_consultorio["limpieza"]  # type: ignore[assignment]
    consulta: Prestacion = entorno_consultorio["consulta"]  # type: ignore[assignment]
    paciente_1: Paciente = entorno_consultorio["paciente_1"]  # type: ignore[assignment]
    paciente_2: Paciente = entorno_consultorio["paciente_2"]  # type: ignore[assignment]

    primer_resp = client.post(
        "/api/v1/turnos",
        headers={"X-Usuario-Id": str(recepcion.id)},
        json={
            "paciente_id": str(paciente_1.id),
            "profesional_id": str(dra_garcia.id),
            "sillon_id": str(sillon_1.id),
            "prestacion_id": str(limpieza.id),
            "inicio": ar_dt(2026, 11, 23, 10, 0).isoformat(),
        },
    )
    assert primer_resp.status_code == 201

    conflicto_resp = client.post(
        "/api/v1/turnos",
        headers={"X-Usuario-Id": str(recepcion.id)},
        json={
            "paciente_id": str(paciente_2.id),
            "profesional_id": str(dra_garcia.id),
            "sillon_id": str(sillon_2.id),
            "prestacion_id": str(consulta.id),
            "inicio": ar_dt(2026, 11, 23, 10, 15).isoformat(),
        },
    )
    assert conflicto_resp.status_code == 409
    assert conflicto_resp.json()["detail"]["codigo"] == "solapamiento_profesional"
    assert len(repo.turnos) == 1
    assert len(repo.auditoria) == 1


def test_escenario_3_rechazo_solapamiento_mismo_sillon_distinto_profesional(
    entorno_consultorio: dict[str, object],
) -> None:
    """Escenario 3 (Error RN-AG-04): dos profesionales distintos no pueden usar el mismo sillón."""
    client: TestClient = entorno_consultorio["client"]  # type: ignore[assignment]
    repo: RepositorioAgendaMemoria = entorno_consultorio["repo"]  # type: ignore[assignment]
    recepcion: Usuario = entorno_consultorio["recepcion"]  # type: ignore[assignment]
    dra_garcia: Usuario = entorno_consultorio["dra_garcia"]  # type: ignore[assignment]
    dr_perez: Usuario = entorno_consultorio["dr_perez"]  # type: ignore[assignment]
    sillon_1: Sillon = entorno_consultorio["sillon_1"]  # type: ignore[assignment]
    limpieza: Prestacion = entorno_consultorio["limpieza"]  # type: ignore[assignment]
    consulta: Prestacion = entorno_consultorio["consulta"]  # type: ignore[assignment]
    paciente_1: Paciente = entorno_consultorio["paciente_1"]  # type: ignore[assignment]
    paciente_2: Paciente = entorno_consultorio["paciente_2"]  # type: ignore[assignment]

    service: AgendaTurnosService = entorno_consultorio["service"]  # type: ignore[assignment]
    turno_base = service.crear_turno(
        recepcion,
        CrearTurnoInput(
            paciente_id=paciente_1.id,
            profesional_id=dra_garcia.id,
            sillon_id=sillon_1.id,
            prestacion_id=limpieza.id,
            inicio=ar_dt(2026, 11, 23, 10, 0),
        ),
    )
    turno_base.estado = EstadoTurno.CONFIRMADO

    conflicto_resp = client.post(
        "/api/v1/turnos",
        headers={"X-Usuario-Id": str(recepcion.id)},
        json={
            "paciente_id": str(paciente_2.id),
            "profesional_id": str(dr_perez.id),
            "sillon_id": str(sillon_1.id),
            "prestacion_id": str(consulta.id),
            "inicio": ar_dt(2026, 11, 23, 10, 20).isoformat(),
        },
    )
    assert conflicto_resp.status_code == 409
    assert conflicto_resp.json()["detail"]["codigo"] == "solapamiento_sillon"
    assert len(repo.turnos) == 1


def test_escenario_4_borde_turno_contiguo_exacto_semiabierto(
    entorno_consultorio: dict[str, object],
) -> None:
    """Escenario 4 (Borde [inicio, fin)): turno de 10:40 a 11:10 tras 10:00 a 10:40 es válido."""
    client: TestClient = entorno_consultorio["client"]  # type: ignore[assignment]
    recepcion: Usuario = entorno_consultorio["recepcion"]  # type: ignore[assignment]
    dra_garcia: Usuario = entorno_consultorio["dra_garcia"]  # type: ignore[assignment]
    sillon_1: Sillon = entorno_consultorio["sillon_1"]  # type: ignore[assignment]
    limpieza: Prestacion = entorno_consultorio["limpieza"]  # type: ignore[assignment]
    consulta: Prestacion = entorno_consultorio["consulta"]  # type: ignore[assignment]
    paciente_1: Paciente = entorno_consultorio["paciente_1"]  # type: ignore[assignment]
    paciente_2: Paciente = entorno_consultorio["paciente_2"]  # type: ignore[assignment]

    r1 = client.post(
        "/api/v1/turnos",
        headers={"X-Usuario-Id": str(recepcion.id)},
        json={
            "paciente_id": str(paciente_1.id),
            "profesional_id": str(dra_garcia.id),
            "sillon_id": str(sillon_1.id),
            "prestacion_id": str(limpieza.id),
            "inicio": ar_dt(2026, 11, 23, 10, 0).isoformat(),
        },
    )
    assert r1.status_code == 201

    r2 = client.post(
        "/api/v1/turnos",
        headers={"X-Usuario-Id": str(recepcion.id)},
        json={
            "paciente_id": str(paciente_2.id),
            "profesional_id": str(dra_garcia.id),
            "sillon_id": str(sillon_1.id),
            "prestacion_id": str(consulta.id),
            "inicio": ar_dt(2026, 11, 23, 10, 40).isoformat(),
        },
    )
    assert r2.status_code == 201
    assert datetime.fromisoformat(r2.json()["fin"]) == ar_dt(2026, 11, 23, 11, 10)


def test_escenario_5_borde_horario_liberado_por_turno_cancelado(
    entorno_consultorio: dict[str, object],
) -> None:
    """Escenario 5 (Borde cancelación): un turno cancelado no bloquea profesional ni sillón."""
    repo: RepositorioAgendaMemoria = entorno_consultorio["repo"]  # type: ignore[assignment]
    client: TestClient = entorno_consultorio["client"]  # type: ignore[assignment]
    consultorio: Consultorio = entorno_consultorio["consultorio"]  # type: ignore[assignment]
    recepcion: Usuario = entorno_consultorio["recepcion"]  # type: ignore[assignment]
    dra_garcia: Usuario = entorno_consultorio["dra_garcia"]  # type: ignore[assignment]
    sillon_1: Sillon = entorno_consultorio["sillon_1"]  # type: ignore[assignment]
    limpieza: Prestacion = entorno_consultorio["limpieza"]  # type: ignore[assignment]
    paciente_1: Paciente = entorno_consultorio["paciente_1"]  # type: ignore[assignment]
    paciente_2: Paciente = entorno_consultorio["paciente_2"]  # type: ignore[assignment]

    repo.turnos.append(
        Turno(
            consultorio_id=consultorio.id,
            paciente_id=paciente_1.id,
            profesional_id=dra_garcia.id,
            sillon_id=sillon_1.id,
            prestacion_id=limpieza.id,
            inicio=ar_dt(2026, 11, 23, 10, 0),
            fin=ar_dt(2026, 11, 23, 10, 40),
            duracion_minutos=40,
            estado=EstadoTurno.CANCELADO,
            token_publico_hash="hash-cancelado-previo",
        )
    )

    resp = client.post(
        "/api/v1/turnos",
        headers={"X-Usuario-Id": str(recepcion.id)},
        json={
            "paciente_id": str(paciente_2.id),
            "profesional_id": str(dra_garcia.id),
            "sillon_id": str(sillon_1.id),
            "prestacion_id": str(limpieza.id),
            "inicio": ar_dt(2026, 11, 23, 10, 0).isoformat(),
        },
    )
    assert resp.status_code == 201
    assert resp.json()["estado"] == "reservado"


def test_escenario_6_bloqueo_agenda_disponibilidad_y_sobrecarga_autorizada(
    entorno_consultorio: dict[str, object],
) -> None:
    """Escenario 6: bloqueo de agenda (409), fuera de franja (422) y sobrecarga permitida a recepción."""
    repo: RepositorioAgendaMemoria = entorno_consultorio["repo"]  # type: ignore[assignment]
    client: TestClient = entorno_consultorio["client"]  # type: ignore[assignment]
    consultorio: Consultorio = entorno_consultorio["consultorio"]  # type: ignore[assignment]
    recepcion: Usuario = entorno_consultorio["recepcion"]  # type: ignore[assignment]
    dra_garcia: Usuario = entorno_consultorio["dra_garcia"]  # type: ignore[assignment]
    sillon_1: Sillon = entorno_consultorio["sillon_1"]  # type: ignore[assignment]
    consulta: Prestacion = entorno_consultorio["consulta"]  # type: ignore[assignment]
    paciente_1: Paciente = entorno_consultorio["paciente_1"]  # type: ignore[assignment]

    repo.bloqueos.append(
        BloqueoAgenda(
            consultorio_id=consultorio.id,
            sillon_id=sillon_1.id,
            inicio=ar_dt(2026, 11, 23, 12, 0),
            fin=ar_dt(2026, 11, 23, 13, 0),
            motivo="Mantenimiento preventivo de compresor",
        )
    )

    resp_bloqueo = client.post(
        "/api/v1/turnos",
        headers={"X-Usuario-Id": str(recepcion.id)},
        json={
            "paciente_id": str(paciente_1.id),
            "profesional_id": str(dra_garcia.id),
            "sillon_id": str(sillon_1.id),
            "prestacion_id": str(consulta.id),
            "inicio": ar_dt(2026, 11, 23, 12, 15).isoformat(),
        },
    )
    assert resp_bloqueo.status_code == 409
    assert resp_bloqueo.json()["detail"]["codigo"] == "conflicto_bloqueo_agenda"

    resp_fuera_franja = client.post(
        "/api/v1/turnos",
        headers={"X-Usuario-Id": str(recepcion.id)},
        json={
            "paciente_id": str(paciente_1.id),
            "profesional_id": str(dra_garcia.id),
            "sillon_id": str(sillon_1.id),
            "prestacion_id": str(consulta.id),
            "inicio": ar_dt(2026, 11, 23, 13, 30).isoformat(),
            "sobrecarga": False,
        },
    )
    assert resp_fuera_franja.status_code == 422
    assert resp_fuera_franja.json()["detail"]["codigo"] == "fuera_de_disponibilidad"

    # Con sobrecarga=True autorizado a recepción y duración ajustada manualmente a 45 min
    resp_sobrecarga = client.post(
        "/api/v1/turnos",
        headers={"X-Usuario-Id": str(recepcion.id)},
        json={
            "paciente_id": str(paciente_1.id),
            "profesional_id": str(dra_garcia.id),
            "sillon_id": str(sillon_1.id),
            "prestacion_id": str(consulta.id),
            "inicio": ar_dt(2026, 11, 23, 13, 30).isoformat(),
            "duracion_minutos": 45,
            "sobrecarga": True,
        },
    )
    assert resp_sobrecarga.status_code == 201
    assert resp_sobrecarga.json()["duracion_minutos"] == 45
    assert datetime.fromisoformat(resp_sobrecarga.json()["fin"]) == ar_dt(2026, 11, 23, 14, 15)


def test_escenario_7_aislamiento_consultorio_rbac_y_timezone_obligatorio(
    entorno_consultorio: dict[str, object],
) -> None:
    """Escenario 7: aislamiento RN-AU-01 (403), rol inválido (403) y rechazo de datetime naive (422)."""
    client: TestClient = entorno_consultorio["client"]  # type: ignore[assignment]
    recepcion: Usuario = entorno_consultorio["recepcion"]  # type: ignore[assignment]
    admin_solo: Usuario = entorno_consultorio["admin_solo"]  # type: ignore[assignment]
    dra_garcia: Usuario = entorno_consultorio["dra_garcia"]  # type: ignore[assignment]
    sillon_1: Sillon = entorno_consultorio["sillon_1"]  # type: ignore[assignment]
    sillon_otro: Sillon = entorno_consultorio["sillon_otro_consultorio"]  # type: ignore[assignment]
    limpieza: Prestacion = entorno_consultorio["limpieza"]  # type: ignore[assignment]
    paciente_1: Paciente = entorno_consultorio["paciente_1"]  # type: ignore[assignment]

    # Cruce de consultorio -> 403 Forbidden
    resp_tenant = client.post(
        "/api/v1/turnos",
        headers={"X-Usuario-Id": str(recepcion.id)},
        json={
            "paciente_id": str(paciente_1.id),
            "profesional_id": str(dra_garcia.id),
            "sillon_id": str(sillon_otro.id),
            "prestacion_id": str(limpieza.id),
            "inicio": ar_dt(2026, 11, 23, 10, 0).isoformat(),
        },
    )
    assert resp_tenant.status_code == 403
    assert resp_tenant.json()["detail"]["codigo"] == "aislamiento_consultorio"

    # Rol administracion no crea turnos -> 403 Forbidden
    resp_rol = client.post(
        "/api/v1/turnos",
        headers={"X-Usuario-Id": str(admin_solo.id)},
        json={
            "paciente_id": str(paciente_1.id),
            "profesional_id": str(dra_garcia.id),
            "sillon_id": str(sillon_1.id),
            "prestacion_id": str(limpieza.id),
            "inicio": ar_dt(2026, 11, 23, 10, 0).isoformat(),
        },
    )
    assert resp_rol.status_code == 403
    assert resp_rol.json()["detail"]["codigo"] == "permiso_denegado"

    # Sobrecarga intentada por odontólogo (solo recepcion/dueno) -> 403 Forbidden
    resp_sobrecarga_odontologo = client.post(
        "/api/v1/turnos",
        headers={"X-Usuario-Id": str(dra_garcia.id)},
        json={
            "paciente_id": str(paciente_1.id),
            "profesional_id": str(dra_garcia.id),
            "sillon_id": str(sillon_1.id),
            "prestacion_id": str(limpieza.id),
            "inicio": ar_dt(2026, 11, 23, 13, 30).isoformat(),
            "sobrecarga": True,
        },
    )
    assert resp_sobrecarga_odontologo.status_code == 403

    # Timestamp naive sin zona horaria -> 422 Unprocessable Entity
    resp_naive = client.post(
        "/api/v1/turnos",
        headers={"X-Usuario-Id": str(recepcion.id)},
        json={
            "paciente_id": str(paciente_1.id),
            "profesional_id": str(dra_garcia.id),
            "sillon_id": str(sillon_1.id),
            "prestacion_id": str(limpieza.id),
            "inicio": "2026-11-23T10:00:00",
        },
    )
    assert resp_naive.status_code == 422


def test_validaciones_adicionales_auth_y_recursos_inactivos(
    entorno_consultorio: dict[str, object],
) -> None:
    """Cobertura adicional: cabeceras faltantes/inválidas, recurso inactivo y no encontrado."""
    client: TestClient = entorno_consultorio["client"]  # type: ignore[assignment]
    recepcion: Usuario = entorno_consultorio["recepcion"]  # type: ignore[assignment]
    usuario_inactivo: Usuario = entorno_consultorio["usuario_inactivo"]  # type: ignore[assignment]
    dra_garcia: Usuario = entorno_consultorio["dra_garcia"]  # type: ignore[assignment]
    sillon_1: Sillon = entorno_consultorio["sillon_1"]  # type: ignore[assignment]
    limpieza: Prestacion = entorno_consultorio["limpieza"]  # type: ignore[assignment]
    paciente_1: Paciente = entorno_consultorio["paciente_1"]  # type: ignore[assignment]

    assert (
        client.post(
            "/api/v1/turnos",
            json={
                "paciente_id": str(paciente_1.id),
                "profesional_id": str(dra_garcia.id),
                "sillon_id": str(sillon_1.id),
                "prestacion_id": str(limpieza.id),
                "inicio": ar_dt(2026, 11, 23, 10, 0).isoformat(),
            },
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/api/v1/turnos",
            headers={"X-Usuario-Id": "no-es-uuid"},
            json={
                "paciente_id": str(paciente_1.id),
                "profesional_id": str(dra_garcia.id),
                "sillon_id": str(sillon_1.id),
                "prestacion_id": str(limpieza.id),
                "inicio": ar_dt(2026, 11, 23, 10, 0).isoformat(),
            },
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/api/v1/turnos",
            headers={"X-Usuario-Id": str(usuario_inactivo.id)},
            json={
                "paciente_id": str(paciente_1.id),
                "profesional_id": str(dra_garcia.id),
                "sillon_id": str(sillon_1.id),
                "prestacion_id": str(limpieza.id),
                "inicio": ar_dt(2026, 11, 23, 10, 0).isoformat(),
            },
        ).status_code
        == 403
    )

    # Profesional sin rol odontólogo -> 422
    assert (
        client.post(
            "/api/v1/turnos",
            headers={"X-Usuario-Id": str(recepcion.id)},
            json={
                "paciente_id": str(paciente_1.id),
                "profesional_id": str(recepcion.id),
                "sillon_id": str(sillon_1.id),
                "prestacion_id": str(limpieza.id),
                "inicio": ar_dt(2026, 11, 23, 10, 0).isoformat(),
            },
        ).status_code
        == 422
    )

    # Recurso inexistente -> 404
    assert (
        client.post(
            "/api/v1/turnos",
            headers={"X-Usuario-Id": str(recepcion.id)},
            json={
                "paciente_id": str(paciente_1.id),
                "profesional_id": str(dra_garcia.id),
                "sillon_id": str(uuid4()),
                "prestacion_id": str(limpieza.id),
                "inicio": ar_dt(2026, 11, 23, 10, 0).isoformat(),
            },
        ).status_code
        == 404
    )

    # Excepciones directas de servicio verificables en capa dominio
    service: AgendaTurnosService = entorno_consultorio["service"]  # type: ignore[assignment]
    service.crear_turno(
        recepcion,
        CrearTurnoInput(
            paciente_id=paciente_1.id,
            profesional_id=dra_garcia.id,
            sillon_id=sillon_1.id,
            prestacion_id=limpieza.id,
            inicio=ar_dt(2026, 11, 23, 9, 0),
        ),
    )
    with pytest.raises(SolapamientoProfesionalError):
        service.crear_turno(
            recepcion,
            CrearTurnoInput(
                paciente_id=paciente_1.id,
                profesional_id=dra_garcia.id,
                sillon_id=entorno_consultorio["sillon_2"].id,  # type: ignore[attr-defined]
                prestacion_id=limpieza.id,
                inicio=ar_dt(2026, 11, 23, 9, 10),
            ),
        )
    with pytest.raises(SolapamientoSillonError):
        service.crear_turno(
            recepcion,
            CrearTurnoInput(
                paciente_id=paciente_1.id,
                profesional_id=entorno_consultorio["dr_perez"].id,  # type: ignore[attr-defined]
                sillon_id=sillon_1.id,
                prestacion_id=limpieza.id,
                inicio=ar_dt(2026, 11, 23, 9, 10),
            ),
        )


def test_cobertura_ramas_borde_y_recursos_inactivos(
    entorno_consultorio: dict[str, object],
) -> None:
    """Cubre validaciones adicionales de servicio para alcanzar 100 % de cobertura en dominio."""
    repo: RepositorioAgendaMemoria = entorno_consultorio["repo"]  # type: ignore[assignment]
    service: AgendaTurnosService = entorno_consultorio["service"]  # type: ignore[assignment]
    consultorio: Consultorio = entorno_consultorio["consultorio"]  # type: ignore[assignment]
    recepcion: Usuario = entorno_consultorio["recepcion"]  # type: ignore[assignment]
    usuario_inactivo: Usuario = entorno_consultorio["usuario_inactivo"]  # type: ignore[assignment]
    dra_garcia: Usuario = entorno_consultorio["dra_garcia"]  # type: ignore[assignment]
    dr_perez: Usuario = entorno_consultorio["dr_perez"]  # type: ignore[assignment]
    sillon_1: Sillon = entorno_consultorio["sillon_1"]  # type: ignore[assignment]
    sillon_2: Sillon = entorno_consultorio["sillon_2"]  # type: ignore[assignment]
    limpieza: Prestacion = entorno_consultorio["limpieza"]  # type: ignore[assignment]
    paciente_1: Paciente = entorno_consultorio["paciente_1"]  # type: ignore[assignment]

    # Operador inactivo directo en servicio
    with pytest.raises(PermisoDenegadoError):
        service.crear_turno(
            usuario_inactivo,
            CrearTurnoInput(
                paciente_id=paciente_1.id,
                profesional_id=dra_garcia.id,
                sillon_id=sillon_1.id,
                prestacion_id=limpieza.id,
                inicio=ar_dt(2026, 11, 23, 10, 0),
            ),
        )

    # Turno que cruza medianoche fuera de jornada del día
    with pytest.raises(FueraDeDisponibilidadError):
        service.crear_turno(
            recepcion,
            CrearTurnoInput(
                paciente_id=paciente_1.id,
                profesional_id=dra_garcia.id,
                sillon_id=sillon_1.id,
                prestacion_id=limpieza.id,
                inicio=ar_dt(2026, 11, 23, 23, 45),
            ),
        )

    # Bloqueo y turno existente de otro consultorio o recurso distinto no interfieren
    otro_consultorio_id = next(cid for cid in repo.consultorios if cid != consultorio.id)
    repo.bloqueos.append(
        BloqueoAgenda(
            consultorio_id=otro_consultorio_id,
            sillon_id=sillon_1.id,
            inicio=ar_dt(2026, 11, 23, 9, 0),
            fin=ar_dt(2026, 11, 23, 12, 0),
            motivo="Bloqueo externo",
        )
    )
    repo.bloqueos.append(
        BloqueoAgenda(
            consultorio_id=consultorio.id,
            profesional_id=dr_perez.id,
            sillon_id=sillon_2.id,
            inicio=ar_dt(2026, 11, 23, 9, 0),
            fin=ar_dt(2026, 11, 23, 12, 0),
            motivo="Bloqueo otro profesional y sillón",
        )
    )
    repo.turnos.append(
        Turno(
            consultorio_id=otro_consultorio_id,
            paciente_id=paciente_1.id,
            profesional_id=dra_garcia.id,
            sillon_id=sillon_1.id,
            prestacion_id=limpieza.id,
            inicio=ar_dt(2026, 11, 23, 10, 0),
            fin=ar_dt(2026, 11, 23, 10, 40),
            duracion_minutos=40,
            token_publico_hash="hash-otro-consultorio",
        )
    )
    creado = service.crear_turno(
        recepcion,
        CrearTurnoInput(
            paciente_id=paciente_1.id,
            profesional_id=dra_garcia.id,
            sillon_id=sillon_1.id,
            prestacion_id=limpieza.id,
            inicio=ar_dt(2026, 11, 23, 10, 0),
        ),
    )
    assert creado.estado == EstadoTurno.RESERVADO

    # Sillón inactivo
    sillon_2.activo = False
    with pytest.raises(RecursoInactivoError):
        service.crear_turno(
            recepcion,
            CrearTurnoInput(
                paciente_id=paciente_1.id,
                profesional_id=dra_garcia.id,
                sillon_id=sillon_2.id,
                prestacion_id=limpieza.id,
                inicio=ar_dt(2026, 11, 23, 11, 0),
            ),
        )
    sillon_2.activo = True

    # Consultorio inactivo y consultorio inexistente
    consultorio.activo = False
    with pytest.raises(RecursoInactivoError):
        service.crear_turno(
            recepcion,
            CrearTurnoInput(
                paciente_id=paciente_1.id,
                profesional_id=dra_garcia.id,
                sillon_id=sillon_1.id,
                prestacion_id=limpieza.id,
                inicio=ar_dt(2026, 11, 23, 11, 0),
            ),
        )
    consultorio.activo = True

    operador_huerfano = Usuario(
        consultorio_id=uuid4(),
        nombre_completo="Operador Huérfano (Ficticio)",
        email="huerfano@ejemplo-ficticio.test",
        roles={RolUsuario.RECEPCION},
    )
    with pytest.raises(RecursoNoEncontradoError):
        service.crear_turno(
            operador_huerfano,
            CrearTurnoInput(
                paciente_id=paciente_1.id,
                profesional_id=dra_garcia.id,
                sillon_id=sillon_1.id,
                prestacion_id=limpieza.id,
                inicio=ar_dt(2026, 11, 23, 11, 0),
            ),
        )
