from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
import cProfile
import pstats


api = APIRouter()


@api.get("/{id}", response_model=schemas.OrdenCargaAnticipoRetirado)
async def read_orden_carga_anticipo_retirado_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.ORDEN_CARGA_ANTICIPO_RETIRADO)),  # noqa: B008
):
    return services.get_orden_carga_anticipo_retirado_by_id(db, id)


@api.get("/{id}/pdf/retirados")
async def read_orden_carga_anticipo_retirado_pdf_by_id(
    id: int,
    db: Session = Depends(get_db_session),
    _: bool = Depends(Permiso(a.VER, m.ORDEN_CARGA_ANTICIPO_RETIRADO)),
):
    profiler = cProfile.Profile()
    profiler.enable()

    try:
        result = services.get_orden_carga_anticipo_retirado_pdf_by_id(db, id)
    finally:
        profiler.disable()
        s = StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        ps.print_stats()
        print(s.getvalue())

    return result


@api.post("/", response_model=schemas.OrdenCargaAnticipoRetirado)
async def add_new_orden_carga_anticipo_retirado(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.OrdenCargaAnticipoRetiradoForm] = (  # type: ignore
        Form(...)  # noqa: B008
    ),
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.ORDEN_CARGA_ANTICIPO_RETIRADO)),  # noqa: B008
):
    return services.create_orden_carga_anticipo_retirado(
        db,
        data,  # type: ignore
        current_user.username,
    )


@api.put("/{id}", response_model=schemas.OrdenCargaAnticipoRetirado)
async def edit_orden_carga_anticipo_retirado(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.OrdenCargaAnticipoRetiradoForm] = (  # type: ignore
        Form(...)  # noqa: B008
    ),
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.ORDEN_CARGA_ANTICIPO_RETIRADO)),  # noqa: B008
):
    return services.edit_orden_carga_anticipo_retirado(
        id,
        db,
        data,  # type: ignore
        current_user.username,
    )


@api.delete("/{id}", response_model=schemas.OrdenCargaAnticipoRetirado)
async def delete_orden_carga_anticipo_retirado(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(  # noqa: B008
        Permiso(a.ELIMINAR, m.ORDEN_CARGA_ANTICIPO_RETIRADO)  # noqa: B008
    ),
):
    return services.delete_orden_carga_anticipo_retirado(db, id, current_user.username)


