from typing import List

from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums.estado import EstadoEnum

api = APIRouter()


@api.get("/", response_model=List[schemas.FleteList])
async def read_flete_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.FLETE)),  # noqa: B008
):
    return repositories.get_flete_list(db)


@api.get("/gestor_carga", response_model=List[schemas.FleteList])
async def read_flete_list_by_gestor_carga(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.FLETE)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return repositories.get_flete_list_by_gestor_carga_id(
        db, current_user.gestor_carga_id
    )


@api.get("/reports")
async def flete_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.FLETE)),  # noqa: B008
):
    return services.get_flete_reports(db)


@api.get("/{id}", response_model=schemas.Flete)
async def read_flete_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.FLETE)),  # noqa: B008
):
    return services.get_flete_datail_by_id(db, id)


@api.post("/", response_model=schemas.Flete)
async def add_new_flete(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.FleteForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.FLETE)),  # noqa: B008
):
    return services.create_flete(
        db,
        data,  # type: ignore
        current_user.gestor_carga_id,
        current_user.username,
    )


@api.put("/{id}", response_model=schemas.Flete)
async def edit_flete(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.FleteForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.FLETE)),  # noqa: B008
):
    return services.edit_flete(
        id,
        db,
        data,  # type: ignore
        current_user.gestor_carga_id,
        current_user.username,
    )


@api.delete("/{id}", response_model=schemas.Flete)
async def delete_flete(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.FLETE)),  # noqa: B008
):
    return services.delete_flete(db, id, current_user.username)


@api.get("/{id}/cancel", response_model=schemas.Flete)
def cancel_flete_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.FLETE)),  # noqa: B008
):
    return services.change_flete_status(
        db, id, EstadoEnum.INACTIVO, current_user.username
    )


@api.get("/{id}/publish", response_model=schemas.Flete)
def publish_flete_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.FLETE)),  # noqa: B008
):
    return services.change_flete_public_status(db, id, True, current_user.username)


@api.get("/{id}/unpublish", response_model=schemas.Flete)
def unpublish_flete_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.FLETE)),  # noqa: B008
):
    return services.change_flete_public_status(db, id, False, current_user.username)


@api.get(
    "/destinatarios/{remitente_id}/{origen_id}/{destino_id}",
    response_model=List[schemas.FleteDestinatario],
)
def read_flete_destinatario_list_by_id(
    remitente_id: int,
    origen_id: int,
    destino_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.FLETE)),  # noqa: B008
):
    return services.get_destinatario_list_by(
        db, remitente_id, origen_id, destino_id, current_user.gestor_carga_id
    )


@api.get("/flete-list/{id}", response_model=schemas.FleteList)
async def read_flete_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.FLETE)),  # noqa: B008
):
    return services.get_flete_detail_by_id(db, id)
