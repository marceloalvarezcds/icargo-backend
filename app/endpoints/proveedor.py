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


@api.get("/", response_model=List[schemas.ProveedorList])
async def read_proveedor_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.PROVEEDOR)),  # noqa: B008
):
    return repositories.get_proveedor_list(db)


@api.get("/gestor_cuenta_id", response_model=List[schemas.ProveedorList])
async def read_proveedor_list_by_gestor_cuenta_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.PROVEEDOR)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return repositories.get_proveedor_list_by_gestor_cuenta_id(
        db, current_user.gestor_carga_id
    )


@api.get("/insumo/{insumo_id}", response_model=List[schemas.ProveedorList])
async def read_proveedor_list_by_insumo_id(
    insumo_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.PROVEEDOR)),  # noqa: B008
):
    return services.get_proveedor_list_by_insumo_id(
        db, insumo_id, current_user.gestor_carga_id
    )


@api.get("/reports")
async def proveedor_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.PROVEEDOR)),  # noqa: B008
):
    return services.get_proveedor_reports(db)


@api.get("/{id}", response_model=schemas.Proveedor)
async def read_proveedor_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.PROVEEDOR)),  # noqa: B008
):
    return services.get_proveedor_by_id_and_gestor_carga_id(
        db, id, current_user.gestor_carga_id
    )


@api.post("/", response_model=schemas.Proveedor)
async def add_new_proveedor(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.ProveedorForm] = Form(...),  # type: ignore  # noqa: B008
    file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.PROVEEDOR)),  # noqa: B008
):
    return await services.create_proveedor(
        db, data, file, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.Proveedor)
async def edit_proveedor(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.ProveedorForm] = Form(...),  # type: ignore  # noqa: B008
    file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.PROVEEDOR)),  # noqa: B008
):
    return await services.edit_proveedor(
        id, db, data, file, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.Proveedor)
async def delete_proveedor(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.PROVEEDOR)),  # noqa: B008
):
    return services.delete_proveedor(
        db, id, current_user.gestor_carga_id, current_user.username
    )

@api.get("/{id}/active", response_model=schemas.Proveedor)
def active_proveedor_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.PROVEEDOR)),  # noqa: B008
):
    return services.change_proveedor_status(
        db, id, EstadoEnum.ACTIVO, current_user.username
    )


@api.get("/{id}/inactive", response_model=schemas.Proveedor)
def inactive_proveedor_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.PROVEEDOR)),  # noqa: B008
):
    return services.change_proveedor_status(
        db, id, EstadoEnum.INACTIVO, current_user.username
    )
