from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session,Permisos
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums.estado import EstadoEnum

api = APIRouter()


@api.get("/", response_model=List[schemas.CentroOperativoList])
async def read_centro_operativo_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CENTRO_OPERATIVO)),  # noqa: B008
):
    return repositories.get_centro_operativo_list(db)


@api.get("/gestor_cuenta_id", response_model=List[schemas.CentroOperativoList])
async def read_centro_operativo_list_by_gestor_cuenta_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CENTRO_OPERATIVO)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return repositories.get_centro_operativo_list_by_gestor_cuenta_id(
        db, current_user.gestor_carga_id
    )


@api.get("/origen-ambos", response_model=List[schemas.CentroOperativoList])
async def read_centro_operativo_origen_ambos(
    db: Session = Depends(get_db_session),
    _: bool = Depends(Permisos(a.LISTAR, [m.CENTRO_OPERATIVO, m.FLETE])),
    current_user: schemas.AuthUser = Depends(get_current_user),
):
    return repositories.get_centro_operativo_list_origen_ambos(db, current_user.gestor_carga_id)


@api.get("/reports")
async def centro_operativo_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.CENTRO_OPERATIVO)),  # noqa: B008
):
    return services.get_centro_operativo_reports(db)

@api.get("/gestor_cuenta_id/destino-ambos", response_model=List[schemas.CentroOperativoList])
async def read_centro_operativo_destino_ambos(
    db: Session = Depends(get_db_session),
    _: bool = Depends(Permisos(a.LISTAR, [m.CENTRO_OPERATIVO, m.FLETE])),
    current_user: schemas.AuthUser = Depends(get_current_user),
):
    return repositories.get_centro_operativo_list_destino_ambos(db, current_user.gestor_carga_id)

@api.get("/{id}", response_model=schemas.CentroOperativo)
async def read_centro_operativo_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.CENTRO_OPERATIVO)),  # noqa: B008
):
    return services.get_centro_operativo_by_id_and_gestor_carga_id(
        db, id, current_user.gestor_carga_id
    )


@api.post("/", response_model=schemas.CentroOperativo)
async def add_new_centro_operativo(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.CentroOperativoForm] = Form(...),  # type: ignore  # noqa: B008
    file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.CENTRO_OPERATIVO)),  # noqa: B008
):
    return await services.create_centro_operativo(
        db, data, file, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.CentroOperativo)
async def edit_centro_operativo(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.CentroOperativoForm] = Form(...),  # type: ignore  # noqa: B008
    file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.CENTRO_OPERATIVO)),  # noqa: B008
):
    return await services.edit_centro_operativo(
        id, db, data, file, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.CentroOperativo)
async def delete_centro_operativo(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.CENTRO_OPERATIVO)),  # noqa: B008
):
    return services.delete_centro_operativo(
        db, id, current_user.gestor_carga_id, current_user.username
    )


@api.get("/{id}/active", response_model=schemas.CentroOperativo)
def active_centro_operativo_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.CENTRO_OPERATIVO)),  # noqa: B008
):
    return services.change_centro_operativo_status(
        db, id, EstadoEnum.ACTIVO, current_user.username
    )


@api.get("/{id}/inactive", response_model=schemas.CentroOperativo)
def inactive_centro_operativo_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.CENTRO_OPERATIVO)),  # noqa: B008
):
    return services.change_centro_operativo_status(
        db, id, EstadoEnum.INACTIVO, current_user.username
    )
