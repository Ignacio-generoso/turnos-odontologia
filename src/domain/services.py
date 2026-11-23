"""Repositorio en memoria y servicio de dominio para crear turnos sin solapamientos."""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from threading import Lock
from uuid import UUID
from zoneinfo import ZoneInfo

from src.domain.models import (
    AislamientoConsultorioError,
    AuditoriaEvento,
    BloqueoAgenda,
    BloqueoAgendaConflictError,
    Consultorio,
    CrearTurnoInput,
    DisponibilidadProfesional,
    EstadoTurno,
    FueraDeDisponibilidadError,
    OrigenTurno,
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
    TurnoCreado,
    Usuario,
)

ROLES_CREACION_TURNO = {RolUsuario.RECEPCION, RolUsuario.ODONTOLOGO, RolUsuario.DUENO}
ROLES_SOBRECARGA = {RolUsuario.RECEPCION, RolUsuario.DUENO}


def hay_solapamiento_semiabierto(
    inicio_a: datetime,
    fin_a: datetime,
    inicio_b: datetime,
    fin_b: datetime,
) -> bool:
    """Evalúa si dos intervalos semiabiertos [inicio, fin) se superponen.

    Un turno que comienza exactamente cuando termina el anterior (inicio_b == fin_a)
    NO genera solapamiento, replicando el operador `&&` sobre `tstzrange(inicio, fin, '[)')`.
    """
    return inicio_a < fin_b and inicio_b < fin_a


class RepositorioAgendaMemoria:
    """Almacenamiento en memoria thread-safe para pruebas de dominio y API."""

    def __init__(self) -> None:
        self.consultorios: dict[UUID, Consultorio] = {}
        self.usuarios: dict[UUID, Usuario] = {}
        self.sillones: dict[UUID, Sillon] = {}
        self.prestaciones: dict[UUID, Prestacion] = {}
        self.pacientes: dict[UUID, Paciente] = {}
        self.disponibilidades: list[DisponibilidadProfesional] = []
        self.bloqueos: list[BloqueoAgenda] = []
        self.turnos: list[Turno] = []
        self.auditoria: list[AuditoriaEvento] = []
        self.eventos_emitidos: list[TurnoCreado] = []
        self._lock = Lock()


class AgendaTurnosService:
    """Servicio de aplicación para la creación transaccional de turnos sin solapamientos."""

    def __init__(self, repo: RepositorioAgendaMemoria) -> None:
        self._repo = repo

    def crear_turno(self, operador: Usuario, payload: CrearTurnoInput) -> Turno:
        """Crea un turno interno garantizando todas las reglas RN-AG-01..05, RN-AU-01 y RN-AU-05."""
        self._validar_permiso_operador(operador, payload.sobrecarga)

        consultorio = self._obtener_consultorio(operador.consultorio_id)
        profesional = self._obtener_y_validar_recurso(
            self._repo.usuarios.get(payload.profesional_id),
            operador.consultorio_id,
            "profesional",
        )
        if RolUsuario.ODONTOLOGO not in profesional.roles:
            raise RecursoInactivoError("El profesional seleccionado no posee el rol odontologo activo.")

        sillon = self._obtener_y_validar_recurso(
            self._repo.sillones.get(payload.sillon_id),
            operador.consultorio_id,
            "sillon",
        )
        prestacion = self._obtener_y_validar_recurso(
            self._repo.prestaciones.get(payload.prestacion_id),
            operador.consultorio_id,
            "prestacion",
        )
        paciente = self._obtener_y_validar_recurso(
            self._repo.pacientes.get(payload.paciente_id),
            operador.consultorio_id,
            "paciente",
        )

        duracion_minutos = (
            payload.duracion_minutos if payload.duracion_minutos is not None else prestacion.duracion_minutos
        )
        inicio = payload.inicio
        fin = inicio + timedelta(minutes=duracion_minutos)

        if not payload.sobrecarga:
            self._validar_disponibilidad_horaria(
                consultorio=consultorio,
                profesional_id=profesional.id,
                inicio=inicio,
                fin=fin,
            )

        with self._repo._lock:
            self._validar_bloqueos(
                consultorio_id=consultorio.id,
                profesional_id=profesional.id,
                sillon_id=sillon.id,
                inicio=inicio,
                fin=fin,
            )
            self._validar_solapamientos_activos(
                consultorio_id=consultorio.id,
                profesional=profesional,
                sillon=sillon,
                inicio=inicio,
                fin=fin,
            )

            token_opaco = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(token_opaco.encode("utf-8")).hexdigest()

            turno = Turno(
                consultorio_id=consultorio.id,
                paciente_id=paciente.id,
                profesional_id=profesional.id,
                sillon_id=sillon.id,
                prestacion_id=prestacion.id,
                inicio=inicio,
                fin=fin,
                duracion_minutos=duracion_minutos,
                estado=EstadoTurno.RESERVADO,
                origen=OrigenTurno.INTERNO,
                token_publico_hash=token_hash,
                observaciones_agenda=payload.observaciones_agenda,
                creado_por_usuario_id=operador.id,
            )
            self._repo.turnos.append(turno)

            rol_principal = sorted(rol.value for rol in operador.roles)[0] if operador.roles else None
            self._repo.auditoria.append(
                AuditoriaEvento(
                    consultorio_id=consultorio.id,
                    usuario_id=operador.id,
                    rol_activo=rol_principal,
                    entidad="turno",
                    entidad_id=turno.id,
                    accion="crear",
                    detalle_json={
                        "profesional_id": str(profesional.id),
                        "sillon_id": str(sillon.id),
                        "prestacion_id": str(prestacion.id),
                        "inicio": inicio.isoformat(),
                        "fin": fin.isoformat(),
                        "duracion_minutos": duracion_minutos,
                        "sobrecarga": payload.sobrecarga,
                    },
                    created_at=datetime.now(timezone.utc),
                )
            )

            self._repo.eventos_emitidos.append(
                TurnoCreado(
                    turno_id=turno.id,
                    consultorio_id=consultorio.id,
                    profesional_id=profesional.id,
                    sillon_id=sillon.id,
                    inicio=inicio,
                    fin=fin,
                    estado=turno.estado,
                )
            )

        return turno

    def _validar_permiso_operador(self, operador: Usuario, sobrecarga: bool) -> None:
        if not operador.activo:
            raise PermisoDenegadoError("El usuario operador se encuentra inactivo.")
        if not (operador.roles & ROLES_CREACION_TURNO):
            raise PermisoDenegadoError("El rol del usuario no está autorizado para crear turnos en agenda.")
        if sobrecarga and not (operador.roles & ROLES_SOBRECARGA):
            raise PermisoDenegadoError("Solo recepción o dueño pueden agendar turnos en sobrecarga.")

    def _obtener_consultorio(self, consultorio_id: UUID) -> Consultorio:
        consultorio = self._repo.consultorios.get(consultorio_id)
        if consultorio is None:
            raise RecursoNoEncontradoError("Consultorio no encontrado.")
        if not consultorio.activo:
            raise RecursoInactivoError("El consultorio se encuentra inactivo.")
        return consultorio

    def _obtener_y_validar_recurso(
        self,
        recurso: Usuario | Sillon | Prestacion | Paciente | None,
        consultorio_id: UUID,
        nombre_recurso: str,
    ) -> Any:
        if recurso is None:
            raise RecursoNoEncontradoError(f"El recurso '{nombre_recurso}' no existe.")
        if recurso.consultorio_id != consultorio_id:
            raise AislamientoConsultorioError(
                f"El recurso '{nombre_recurso}' pertenece a otro consultorio (RN-AU-01)."
            )
        if not recurso.activo:
            raise RecursoInactivoError(f"El recurso '{nombre_recurso}' se encuentra inactivo.")
        return recurso

    def _validar_disponibilidad_horaria(
        self,
        consultorio: Consultorio,
        profesional_id: UUID,
        inicio: datetime,
        fin: datetime,
    ) -> None:
        tz = ZoneInfo(consultorio.zona_horaria)
        inicio_local = inicio.astimezone(tz)
        fin_local = fin.astimezone(tz)

        if inicio_local.date() != fin_local.date():
            raise FueraDeDisponibilidadError("El turno no puede extenderse más allá de la jornada del día.")

        dia = inicio_local.weekday()
        hora_inicio_turno = inicio_local.time()
        hora_fin_turno = fin_local.time()

        franjas = [
            d
            for d in self._repo.disponibilidades
            if d.consultorio_id == consultorio.id
            and d.profesional_id == profesional_id
            and d.activo
            and d.dia_semana == dia
        ]
        dentro_de_franja = any(
            d.hora_inicio <= hora_inicio_turno and hora_fin_turno <= d.hora_fin for d in franjas
        )
        if not dentro_de_franja:
            raise FueraDeDisponibilidadError(
                "El horario solicitado cae fuera de las franjas de disponibilidad configuradas para el profesional."
            )

    def _validar_bloqueos(
        self,
        consultorio_id: UUID,
        profesional_id: UUID,
        sillon_id: UUID,
        inicio: datetime,
        fin: datetime,
    ) -> None:
        for bloqueo in self._repo.bloqueos:
            if bloqueo.consultorio_id != consultorio_id:
                continue
            afecta_profesional = bloqueo.profesional_id == profesional_id
            afecta_sillon = bloqueo.sillon_id == sillon_id
            if not (afecta_profesional or afecta_sillon):
                continue
            if hay_solapamiento_semiabierto(inicio, fin, bloqueo.inicio, bloqueo.fin):
                raise BloqueoAgendaConflictError(
                    f"El horario solicitado invade un bloqueo de agenda vigente: {bloqueo.motivo}."
                )

    def _validar_solapamientos_activos(
        self,
        consultorio_id: UUID,
        profesional: Usuario,
        sillon: Sillon,
        inicio: datetime,
        fin: datetime,
    ) -> None:
        for existente in self._repo.turnos:
            if existente.consultorio_id != consultorio_id:
                continue
            if existente.estado == EstadoTurno.CANCELADO:
                continue
            if not hay_solapamiento_semiabierto(inicio, fin, existente.inicio, existente.fin):
                continue
            if existente.profesional_id == profesional.id:
                raise SolapamientoProfesionalError(
                    f"El profesional {profesional.nombre_completo} ya tiene un turno activo en ese rango horario."
                )
            if existente.sillon_id == sillon.id:
                raise SolapamientoSillonError(
                    f"El {sillon.nombre} ya está ocupado en ese rango horario."
                )
