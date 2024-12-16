from typing import List

from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.InsumoPuntoVentaPrecioList])
async def read_insumo_punto_venta_precio_list(
    db: Session = Depends(get_db_session),
    current_user: schemas.AuthUser = Depends(get_current_user),
    _: bool = Depends(Permiso(a.LISTAR, m.INSUMO_PUNTO_VENTA_PRECIO)),
):
    return services.get_insumo_punto_venta_precio_list(db, current_user.gestor_carga_id)


@api.get("/gestor-carga/activo", response_model=List[schemas.InsumoPuntoVentaPrecioList])
async def read_insumo_punto_venta_precio_list(
    db: Session = Depends(get_db_session),
    current_user: schemas.AuthUser = Depends(get_current_user),
    _: bool = Depends(Permiso(a.LISTAR, m.INSUMO_PUNTO_VENTA_PRECIO)),
):
    return services.get_insumo_punto_venta_precio_list_by_estado_activo(db, current_user.gestor_carga_id)


@api.get("/inactivos", response_model=List[schemas.InsumoPuntoVentaPrecioList])
async def read_inactive_insumo_punto_venta_precio_list(
    db: Session = Depends(get_db_session),
    current_user: schemas.AuthUser = Depends(get_current_user),
    _: bool = Depends(Permiso(a.LISTAR, m.INSUMO_PUNTO_VENTA_PRECIO)),
):
    return services.get_inactive_insumo_punto_venta_precio_list(db, current_user.gestor_carga_id)


@api.get("/all", response_model=List[schemas.InsumoPuntoVentaPrecioList])
async def read_all_insumo_punto_venta_precio_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.INSUMO_PUNTO_VENTA_PRECIO)),  # noqa: B008
):
    return services.get_all_insumo_punto_venta_precio_list(db)


@api.get("/flete/{fleteId}", response_model=List[schemas.InsumoPuntoVentaPrecioList])
async def read_insumo_punto_venta_precio_list(
    fleteId: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.INSUMO_PUNTO_VENTA_PRECIO)),  # noqa: B008
):
    return repositories.get_insumo_punto_venta_precio_list_by_gestor_carga_id(
        db, fleteId, current_user.gestor_carga_id
    )


@api.get(
    "/insumos/punto_venta/{punto_venta_id}",
    response_model=List[schemas.InsumoPuntoVentaPrecioList],  
)
async def read_insumos_by_punto_venta(
    punto_venta_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.INSUMO_PUNTO_VENTA_PRECIO)),  # noqa: B008
):
    return services.get_insumos_by_punto_venta_id_and_gestor_carga(
        db, punto_venta_id, current_user.gestor_carga_id
    )


@api.get(
    "/insumo/{insumo_id}/moneda/{moneda_id}/punto_venta/{punto_venta_id}",
    response_model=schemas.InsumoPuntoVentaPrecioList,
)
async def read_last_insumo_punto_venta_precio(
    insumo_id: int,
    moneda_id: int,
    punto_venta_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.INSUMO_PUNTO_VENTA_PRECIO)),  # noqa: B008
):
    return services.get_insumo_punto_venta_precio_by_insumo_id_and_moneda_id_and_punto_venta_id(
        db, insumo_id, moneda_id, punto_venta_id, current_user.gestor_carga_id
    )


@api.get("/reports")
async def insumo_venta_precio_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.INSUMO_PUNTO_VENTA_PRECIO)),  # noqa: B008
):
    return services.get_insumo_punto_venta_precio_reports(db)


@api.get("/{id}", response_model=schemas.InsumoPuntoVentaPrecio)
async def read_insumo_precio_venta_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.INSUMO_PUNTO_VENTA_PRECIO)),  # noqa: B008
):
    return services.get_insumo_punto_venta_precio_by_id(db, id)


@api.post(
    "/",
    response_model=schemas.InsumoPuntoVentaPrecioList,
)
async def add_new_insumo_punto_venta_precio(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.InsumoPuntoVentaPrecioForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.INSUMO_PUNTO_VENTA_PRECIO)),  # noqa: B008
):
    return services.create_insumo_punto_venta_precio(
        db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put(
    "/{id}",response_model=schemas.InsumoPuntoVentaPrecioList,
)
async def edit_insumo_punto_venta_precio(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.InsumoPuntoVentaPrecioUpdate] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.INSUMO_PUNTO_VENTA_PRECIO)),  # noqa: B008
):
    return services.edit_insumo_punto_venta_precio(
        id, db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )
