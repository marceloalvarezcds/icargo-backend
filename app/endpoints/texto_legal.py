from typing import List, Optional
from fastapi import APIRouter, Depends,  Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore
from app import schemas, services
from app.models import TextoLegal
from app.enums import EstadoEnum
from app.services import seleccionable_service as service
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.TextoLegalModel])
async def read_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TEXTO_LEGAL)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_texto_legal_list_by_gestor(db, current_user.gestor_carga_id)


@api.get("/gestor_carga_id", response_model=List[schemas.TextoLegalModel])
async def read_list_by_gestor(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TEXTO_LEGAL)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_texto_legal_list_by_gestor(db, current_user.gestor_carga_id)


@api.get("/{id}", response_model=schemas.TextoLegalModel)
async def read_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.TEXTO_LEGAL)),  # noqa: B008
):
    return services.get_texto_legal_by_id(
        db, id
    )


@api.get("/title/get_by_title", response_model=Optional[schemas.TextoLegalModel])
async def read_by_title(
    title: str,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TEXTO_LEGAL)),  # noqa: B008
):
    return service.get_by_title(TextoLegal, db, title)


@api.post("/", response_model=schemas.TextoLegalModel)
async def add_new(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.TextoLegalBaseModel] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.TEXTO_LEGAL)),  # noqa: B008
):
    return services.crear_texto_legal(db, data, current_user)  # type: ignore


@api.put("/{id}", response_model=schemas.TextoLegalModel)
async def edit(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.TextoLegalBaseModel] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.TEXTO_LEGAL)),  # noqa: B008
):
    return services.edit_texto_legal(id, db, data, current_user)  # type: ignore  # noqa: B950


@api.get("/{id}/active", response_model=schemas.TextoLegalModel)
def active_texto_legal_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.TEXTO_LEGAL)),  # noqa: B008
):
    return service.change_status(
        TextoLegal, db, id, EstadoEnum.ACTIVO, current_user.username
    )


@api.get("/{id}/inactive", response_model=schemas.TextoLegalModel)
def inactive_texto_legal_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.TEXTO_LEGAL)),  # noqa: B008
):
    return service.change_status(
        TextoLegal, db, id, EstadoEnum.INACTIVO, current_user.username
    )
