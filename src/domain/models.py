"""Entidades, enumeraciones, esquemas y excepciones del dominio de turnos."""

from __future__ import annotations

from datetime import datetime, time
from decimal import Decimal
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class RolUsuario(StrEnum):
    """Roles válidos del personal interno del consultorio."""

    DUENO = "dueno"
    ODONTOLOGO = "odontologo"
    RECEPCION = "recepcion"
    ADMINISTRACION = "administracion"


class EstadoTurno(StrEnum):
    """Estados posibles en el ciclo de vida de un turno odontológico."""

    RESERVADO = "reservado"
    CONFIRMADO = "confirmado"
    EN_ATENCION = "en_atencion"
    ATENDIDO = "atendido"
    AUSENTE = "ausente"
    CANCELADO = "cancelado"


class OrigenTurno(StrEnum):
    """Canal de origen del turno."""

    INTERNO = "interno"
    PUBLICO = "publico"


def _validar_datetime_con_tz(valor: datetime) -> datetime:
    """Exige que toda marca temporal incluya zona horaria explícita (TIMESTAMPTZ)."""
    if valor.tzinfo is None or valor.utcoffset() is None:
        raise ValueError("La fecha/hora debe incluir zona horaria explícita (TIMESTAMPTZ).")
    return valor


class Consultorio(BaseModel):
    """Configuración base del consultorio odontológico."""

    id: UUID = Field(default_factory=uuid4)
    nombre: str
    slug: str
    zona_horaria: str = "America/Argentina/Buenos_Aires"
    anticipacion_minima_cancelacion_hs: int = 24
    activo: bool = True


class Usuario(BaseModel):
    """Usuario interno del consultorio con sus roles asignados."""

    id: UUID = Field(default_factory=uuid4)
    consultorio_id: UUID
    nombre_completo: str
    email: str
    roles: set[RolUsuario]
    matricula_profesional: str | None = None
    activo: bool = True


class Sillon(BaseModel):
    """Sillón o box físico de atención odontológica."""

    id: UUID = Field(default_factory=uuid4)
    consultorio_id: UUID
    nombre: str
    ubicacion: str | None = None
    activo: bool = True


class Prestacion(BaseModel):
    """Tipo de atención del catálogo del consultorio con duración base y arancel ARS."""

    id: UUID = Field(default_factory=uuid4)
    consultorio_id: UUID
    nombre: str
    duracion_minutos: int = Field(gt=0)
    precio_referencia_ars: Decimal = Field(ge=Decimal("0.00"))
    visible_publico: bool = True
    activo: bool = True


class DisponibilidadProfesional(BaseModel):
    """Franja horaria semanal configurada para un odontólogo (0=Lunes .. 6=Domingo)."""

    id: UUID = Field(default_factory=uuid4)
    consultorio_id: UUID
    profesional_id: UUID
    dia_semana: int = Field(ge=0, le=6)
    hora_inicio: time
    hora_fin: time
    sillon_preferido_id: UUID | None = None
    activo: bool = True


class BloqueoAgenda(BaseModel):
    """Bloqueo puntual de horario por profesional y/o sillón dentro del consultorio."""

    id: UUID = Field(default_factory=uuid4)
    consultorio_id: UUID
    profesional_id: UUID | None = None
    sillon_id: UUID | None = None
    inicio: datetime
    fin: datetime
    motivo: str

    @field_validator("inicio", "fin")
    @classmethod
    def _check_tz(cls, v: datetime) -> datetime:
        return _validar_datetime_con_tz(v)


class Paciente(BaseModel):
    """Ficha administrativa ficticia de paciente asociada a un consultorio."""

    id: UUID = Field(default_factory=uuid4)
    consultorio_id: UUID
    nombre: str
    apellido: str
    dni: str
    telefono_whatsapp: str
    opt_in_whatsapp: bool = False
    activo: bool = True


class Turno(BaseModel):
    """Turno odontológico agendado con intervalo semiabierto [inicio, fin)."""

    id: UUID = Field(default_factory=uuid4)
    consultorio_id: UUID
    paciente_id: UUID
    profesional_id: UUID
    sillon_id: UUID
    prestacion_id: UUID
    inicio: datetime
    fin: datetime
    duracion_minutos: int = Field(gt=0)
    estado: EstadoTurno = EstadoTurno.RESERVADO
    origen: OrigenTurno = OrigenTurno.INTERNO
    token_publico_hash: str
    observaciones_agenda: str | None = None
    creado_por_usuario_id: UUID | None = None

    @field_validator("inicio", "fin")
    @classmethod
    def _check_tz(cls, v: datetime) -> datetime:
        return _validar_datetime_con_tz(v)


class AuditoriaEvento(BaseModel):
    """Registro append-only de eventos auditables de negocio (RN-AU-05)."""

    id: UUID = Field(default_factory=uuid4)
    consultorio_id: UUID
    usuario_id: UUID | None
    rol_activo: str | None
    entidad: str
    entidad_id: UUID
    accion: str
    detalle_json: dict[str, Any]
    created_at: datetime


class TurnoCreado(BaseModel):
    """Evento de dominio emitido al crearse un turno para desacoplar integraciones."""

    turno_id: UUID
    consultorio_id: UUID
    profesional_id: UUID
    sillon_id: UUID
    inicio: datetime
    fin: datetime
    estado: EstadoTurno


class CrearTurnoInput(BaseModel):
    """Contrato de entrada tipado para crear un turno interno sin solapamientos."""

    paciente_id: UUID
    profesional_id: UUID
    sillon_id: UUID
    prestacion_id: UUID
    inicio: datetime
    duracion_minutos: int | None = Field(default=None, gt=0)
    sobrecarga: bool = False
    observaciones_agenda: str | None = Field(default=None, max_length=500)

    @field_validator("inicio")
    @classmethod
    def _check_inicio_tz(cls, v: datetime) -> datetime:
        return _validar_datetime_con_tz(v)


class TurnoResponse(BaseModel):
    """Respuesta pública interna de un turno creado."""

    id: UUID
    consultorio_id: UUID
    paciente_id: UUID
    profesional_id: UUID
    sillon_id: UUID
    prestacion_id: UUID
    inicio: datetime
    fin: datetime
    duracion_minutos: int
    estado: EstadoTurno
    origen: OrigenTurno
    token_publico_hash: str
    observaciones_agenda: str | None = None


class DominioAgendaError(Exception):
    """Excepción base para violaciones de reglas de negocio de agenda."""

    status_code: int = 400
    codigo: str = "error_agenda"

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self.mensaje = mensaje


class PermisoDenegadoError(DominioAgendaError):
    """El usuario autenticado no posee un rol habilitado para la operación."""

    status_code = 403
    codigo = "permiso_denegado"


class AislamientoConsultorioError(DominioAgendaError):
    """Intento de operar sobre un recurso de otro consultorio (RN-AU-01)."""

    status_code = 403
    codigo = "aislamiento_consultorio"


class RecursoNoEncontradoError(DominioAgendaError):
    """Recurso referenciado inexistente en el repositorio."""

    status_code = 404
    codigo = "recurso_no_encontrado"


class RecursoInactivoError(DominioAgendaError):
    """El profesional, sillón, prestación o paciente está inactivo o no posee rol clínico."""

    status_code = 422
    codigo = "recurso_inactivo_o_invalido"


class FueraDeDisponibilidadError(DominioAgendaError):
    """El horario solicitado cae fuera de las franjas activas del profesional (RN-AG-05)."""

    status_code = 422
    codigo = "fuera_de_disponibilidad"


class SolapamientoProfesionalError(DominioAgendaError):
    """Conflicto de agenda: el profesional ya tiene un turno activo superpuesto (RN-AG-03)."""

    status_code = 409
    codigo = "solapamiento_profesional"


class SolapamientoSillonError(DominioAgendaError):
    """Conflicto de agenda: el sillón/box ya tiene un turno activo superpuesto (RN-AG-04)."""

    status_code = 409
    codigo = "solapamiento_sillon"


class BloqueoAgendaConflictError(DominioAgendaError):
    """El rango horario invade un bloqueo vigente de profesional o sillón."""

    status_code = 409
    codigo = "conflicto_bloqueo_agenda"
