from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session, Permisos
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.logger import logger

api = APIRouter()


@api.get(
    "/orden_carga/{orden_carga_id}",
    response_model=List[schemas.OrdenCargaRemisionOrigen],
)
async def read_orden_carga_list(
    orden_carga_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.ORDEN_CARGA_REMISION_ORIGEN)),  # noqa: B008
):
    return repositories.get_orden_carga_remision_origen_list_by_orden_carga_id(
        db, orden_carga_id
    )


@api.get("/{id}", response_model=schemas.OrdenCargaRemisionOrigen)
async def read_orden_carga_remision_origen_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.ORDEN_CARGA_REMISION_ORIGEN)),  # noqa: B008
):
    return services.get_orden_carga_remision_origen_by_id(db, id)


@api.post("/", response_model=schemas.OrdenCargaRemisionOrigen)
async def add_new_orden_carga_remision_origen(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.OrdenCargaRemisionOrigenForm] = Form(...),  # type: ignore  # noqa: B008
    foto_documento_file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.ORDEN_CARGA_REMISION_ORIGEN)),  # noqa: B008
):
    return await services.create_orden_carga_remision_origen(
        db,
        data,  # type: ignore
        foto_documento_file,
        current_user.username,
    )


@api.put("/{id}", response_model=schemas.OrdenCargaRemisionOrigen)
async def edit_orden_carga_remision_origen(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.OrdenCargaRemisionOrigenForm] = Form(...),  # type: ignore  # noqa: B008
    foto_documento_file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.ORDEN_CARGA_REMISION_ORIGEN)),  # noqa: B008
):
    return await services.edit_orden_carga_remision_origen(
        id,
        db,
        data,  # type: ignore
        foto_documento_file,
        current_user.username,
    )


@api.delete("/{id}", response_model=schemas.OrdenCargaRemisionOrigen)
async def delete_orden_carga_remision_origen(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.ORDEN_CARGA_REMISION_ORIGEN)),  # noqa: B008
):
    return services.delete_orden_carga_remision_origen(db, id, current_user.username)


@api.get("/oc/recepcion/directa", response_model=schemas.OrdenCarga)
async def read_orden_carga_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.ORDEN_CARGA)),  # noqa: B008
):
    return services.get_orden_carga_list(db, current_user.gestor_carga_id)

@api.get(
    "/oc/remito",
    response_model=List[schemas.OrdenCargaRemisionOrigen],
)
@api.get(
    "/oc/remito/{nro_remito}",
    response_model=List[schemas.OrdenCargaRemisionOrigen],
)
async def read_orden_carga_list_by_remito(
    nro_remito: Optional[str] = None,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permisos(a.LISTAR, [m.ORDEN_CARGA_REMISION_ORIGEN, m.ORDEN_CARGA])),  # noqa: B008
):

    return repositories.get_remision_origen_list_by_nro_remito(
        db, nro_remito
    )
