from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/{id}", response_model=schemas.OrdenCargaComplemento)
async def read_orden_carga_complemento_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.ORDEN_CARGA_COMPLEMENTO)),  # noqa: B008
):
    return services.get_orden_carga_complemento_by_id(db, id)


@api.post("/", response_model=schemas.OrdenCargaComplemento)
async def add_new_orden_carga_complemento(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.OrdenCargaComplementoForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.ORDEN_CARGA_COMPLEMENTO)),  # noqa: B008
):
    return services.create_orden_carga_complemento(
        db,
        data,  # type: ignore
        current_user.username,
    )


@api.put("/{id}", response_model=schemas.OrdenCargaComplemento)
async def edit_orden_carga_complemento(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.OrdenCargaComplementoForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.ORDEN_CARGA_COMPLEMENTO)),  # noqa: B008
):
    return services.edit_orden_carga_complemento(
        id,
        db,
        data,  # type: ignore
        current_user.username,
    )


@api.delete("/{id}", response_model=schemas.OrdenCargaComplemento)
async def delete_orden_carga_complemento(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.ORDEN_CARGA_COMPLEMENTO)),  # noqa: B008
):
    return services.delete_orden_carga_complemento(db, id, current_user.username)
