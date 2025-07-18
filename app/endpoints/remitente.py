from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums.estado import EstadoEnum

api = APIRouter()


@api.get("/", response_model=List[schemas.RemitenteList])
async def read_remitente_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.REMITENTE)),  # noqa: B008
):
    return repositories.get_remitente_list(db)


@api.get("/remitente_activos", response_model=List[schemas.RemitenteList])
async def read_remitente_list_activo(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.REMITENTE)),  # noqa: B008
):
    return repositories.get_remitente_list_activo(db)


@api.get("/gestor_cuenta_id", response_model=List[schemas.RemitenteList])
async def read_remitente_list_by_gestor_cuenta_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.REMITENTE)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return repositories.get_remitente_list_by_gestor_cuenta_id(
        db, current_user.gestor_carga_id
    )


@api.get("/reports")
async def remitente_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.REMITENTE)),  # noqa: B008
):
    return services.get_remitente_reports(db)


@api.get("/{id}", response_model=schemas.Remitente)
async def read_remitente_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.REMITENTE)),  # noqa: B008
):
    return services.get_remitente_by_id_and_gestor_carga_id(
        db, id, current_user.gestor_carga_id
    )


@api.post("/", response_model=schemas.Remitente)
async def add_new_remitente(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.RemitenteForm] = Form(...),  # type: ignore  # noqa: B008
    file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.REMITENTE)),  # noqa: B008
):
    return await services.create_remitente(
        db, data, file, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.Remitente)
async def edit_remitente(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.RemitenteForm] = Form(...),  # type: ignore  # noqa: B008
    file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.REMITENTE)),  # noqa: B008
):
    return await services.edit_remitente(
        id, db, data, file, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.Remitente)
async def delete_remitente(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.REMITENTE)),  # noqa: B008
):
    return services.delete_remitente(
        db, id, current_user.gestor_carga_id, current_user.username
    )


@api.get("/{id}/active", response_model=schemas.Remitente)
def active_remitente_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.REMITENTE)),  # noqa: B008
):
    return services.change_remitente_status(
        db, id, EstadoEnum.ACTIVO, current_user.username
    )


@api.get("/{id}/inactive", response_model=schemas.Remitente)
def inactive_remitente_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.REMITENTE)),  # noqa: B008
):
    return services.change_remitente_status(
        db, id, EstadoEnum.INACTIVO, current_user.username
    )
