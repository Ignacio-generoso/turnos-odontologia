"""Aplicación FastAPI para el endpoint de creación de turnos sin solapamientos."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Request, status
from pydantic import BaseModel

from src.domain.models import (
    CrearTurnoInput,
    DominioAgendaError,
    PermisoDenegadoError,
    TurnoResponse,
    Usuario,
)
from src.domain.services import AgendaTurnosService, RepositorioAgendaMemoria


class HealthResponse(BaseModel):
    """Respuesta del endpoint de salud del servicio."""

    status: str


def _get_repo(request: Request) -> RepositorioAgendaMemoria:
    return request.app.state.repo


def get_agenda_service(
    repo: Annotated[RepositorioAgendaMemoria, Depends(_get_repo)],
) -> AgendaTurnosService:
    """Provee la instancia del servicio de agenda ligada al repositorio de la app."""
    return AgendaTurnosService(repo)


def get_current_user(
    repo: Annotated[RepositorioAgendaMemoria, Depends(_get_repo)],
    x_usuario_id: Annotated[str | None, Header(alias="X-Usuario-Id")] = None,
) -> Usuario:
    """Resuelve y valida el usuario interno activo a partir de la cabecera X-Usuario-Id."""
    if x_usuario_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta cabecera de autenticación X-Usuario-Id.",
        )
    try:
        usuario_uuid = UUID(x_usuario_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identificador de usuario inválido.",
        ) from exc

    usuario = repo.usuarios.get(usuario_uuid)
    if usuario is None or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inexistente o inactivo.",
        )
    return usuario


ServiceDep = Annotated[AgendaTurnosService, Depends(get_agenda_service)]
CurrentUserDep = Annotated[Usuario, Depends(get_current_user)]

router = APIRouter(prefix="/api/v1", tags=["turnos"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Verifica el estado operativo básico de la API."""
    return HealthResponse(status="ok")


@router.post(
    "/turnos",
    response_model=TurnoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def crear_turno_endpoint(
    payload: CrearTurnoInput,
    current_user: CurrentUserDep,
    agenda_service: ServiceDep,
) -> TurnoResponse:
    """Crea un turno odontológico validando solapamientos por profesional y sillón."""
    try:
        turno = agenda_service.crear_turno(current_user, payload)
        return TurnoResponse.model_validate(turno, from_attributes=True)
    except (DominioAgendaError, PermisoDenegadoError) as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail={"codigo": exc.codigo, "mensaje": exc.mensaje},
        ) from exc


def create_app(repo: RepositorioAgendaMemoria | None = None) -> FastAPI:
    """Construye la instancia FastAPI conectada al repositorio de agenda."""
    app = FastAPI(
        title="Turnos Odontología API",
        version="0.1.0",
        description="API del MVP para gestión de turnos odontológicos sin solapamientos.",
    )
    app.state.repo = repo if repo is not None else RepositorioAgendaMemoria()
    app.include_router(router)
    return app
