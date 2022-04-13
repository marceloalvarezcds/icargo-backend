from typing import List

from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get(
    "/camion/{camion_id}",
    response_model=List[schemas.CamionSemiNeto],
)
async def read_camion_semi_neto_list_by_camion_id(
    camion_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CAMION_SEMI_NETO)),  # noqa: B008
):
    return repositories.get_camion_semi_neto_list_by_camion_id(db, camion_id)


@api.get(
    "/camion/{camion_id}/semi/{semi_id}",
    response_model=schemas.CamionSemiNeto,
)
async def read_camion_semi_neto_by_camion_id_and_semi_id(
    camion_id: int,
    semi_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.CAMION_SEMI_NETO)),  # noqa: B008
):
    return repositories.get_camion_semi_neto_by_camion_id_and_semi_id(
        db, camion_id, semi_id, current_user.gestor_carga_id
    )


@api.get(
    "/camion/{camion_id}/semi/{semi_id}/producto/{producto_id}",
    response_model=schemas.CamionSemiNeto,
)
async def read_camion_semi_neto_by_camion_id_and_semi_id_and_producto_id(
    camion_id: int,
    semi_id: int,
    producto_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.CAMION_SEMI_NETO)),  # noqa: B008
):
    return services.get_camion_semi_neto_by_camion_id_and_semi_id_and_producto_id(
        db, camion_id, semi_id, producto_id, current_user.gestor_carga_id
    )


@api.post("/", response_model=schemas.CamionSemiNeto)
async def add_new_camion_semi_neto(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.CamionSemiNetoForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.CAMION_SEMI_NETO)),  # noqa: B008
):
    return services.create_camion_semi_neto(
        db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.put("/{id}", response_model=schemas.CamionSemiNeto)
async def edit_camion_semi_neto(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.CamionSemiNetoForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.CAMION_SEMI_NETO)),  # noqa: B008
):
    return services.edit_camion_semi_neto(
        id, db, data, current_user.gestor_carga_id, current_user.username  # type: ignore
    )


@api.delete("/{id}", response_model=schemas.CamionSemiNeto)
async def delete_camion_semi_neto(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.CAMION_SEMI_NETO)),  # noqa: B008
):
    return services.delete_camion_semi_neto(db, id, current_user.username)
