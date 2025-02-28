from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.PuntoVentaList])
async def read_punto_venta_list_by_gestor_carga_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.PUNTO_VENTA)),  # noqa: B008
):
    return repositories.get_punto_venta_list_by_gestor_carga_id(
        db, current_user.gestor_carga_id
    )

@api.get("/activos", response_model=List[schemas.PuntoVentaList])
async def read_punto_venta_list_with_active_prices_by_gestor_carga_id(
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.PUNTO_VENTA)),  # noqa: B008
):
    return repositories.get_punto_venta_list_with_active_prices_by_gestor_carga_id(
        db, current_user.gestor_carga_id
    )


@api.get("/proveedor/{proveedor_id}", response_model=List[schemas.PuntoVentaList])
async def read_punto_venta_list(
    proveedor_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.PUNTO_VENTA)),  # noqa: B008
):
    return repositories.get_punto_venta_list(db, proveedor_id)


@api.get(
    "/insumo/{insumo_id}/proveedor/{proveedor_id}",
    response_model=List[schemas.PuntoVentaList],
)
async def read_punto_venta_list_by_insumo_id(
    insumo_id: int,
    proveedor_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.PUNTO_VENTA)),  # noqa: B008
):
    return services.get_punto_venta_list_by_insumo_id_and_proveedor_id(
        db, insumo_id, proveedor_id, current_user.gestor_carga_id
    )


@api.get("/reports/{proveedor_id}")
async def punto_venta_reports(
    proveedor_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.PUNTO_VENTA)),  # noqa: B008
):
    return services.get_punto_venta_reports(db, proveedor_id)


@api.get("/detail/{id}", response_model=schemas.PuntoVenta)
async def read_punto_venta_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.PUNTO_VENTA)),  # noqa: B008
):
    return services.get_punto_venta_by_id_and_gestor_carga_id(
        db, id, current_user.gestor_carga_id
    )


@api.post("/", response_model=schemas.PuntoVenta)
async def add_new_punto_venta(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.PuntoVentaForm] = Form(...),  # type: ignore  # noqa: B008
    file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.PUNTO_VENTA)),  # noqa: B008
):

    return await services.create_punto_venta(
        db, data, file, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.PuntoVenta)
async def edit_punto_venta(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.PuntoVentaForm] = Form(...),  # type: ignore  # noqa: B008
    file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.PUNTO_VENTA)),  # noqa: B008
):

    return await services.edit_punto_venta(
        id, db, data, file, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.PuntoVenta)
async def delete_punto_venta(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.PUNTO_VENTA)),  # noqa: B008
):
    return services.delete_punto_venta(
        db, id, current_user.gestor_carga_id, current_user.username
    )
