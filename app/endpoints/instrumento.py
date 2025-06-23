from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/{id}/confirmar", response_model=schemas.Instrumento)
async def confirmar_instrumento(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.INSTRUMENTO)),  # noqa: B008
):
    return services.confirmar_instrumento(db, id, current_user.username)


@api.get("/{id}/rechazar", response_model=schemas.Instrumento)
async def rechazar_instrumento(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.INSTRUMENTO)),  # noqa: B008
):
    return services.rechazar_instrumento(db, id, current_user.username)


@api.get("/{id}/anular", response_model=schemas.Instrumento)
async def anular_instrumento(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.INSTRUMENTO)),  # noqa: B008
):
    return services.anular_instrumento(db, id, current_user.username)
