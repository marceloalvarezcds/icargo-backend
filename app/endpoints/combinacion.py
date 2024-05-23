from typing import List

from app.enums.estado import EstadoEnum
from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m


api = APIRouter()



@api.get("/", response_model=List[schemas.CombinacionesBD])
async def read_combinacion_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.COMBINACION)),  # noqa: B008
):
    return repositories.get_combinacion_list(db)



@api.get("/reports")
async def combinacion_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.COMBINACION)), 
     current_user: schemas.AuthUser = Depends(get_current_user), # noqa: B008
):
    return services.get_combinacion_reports(db)


@api.get("/{id}", response_model=schemas.CombinacionGet)
async def read_combinacion_by_id(
     id: int,
     db: Session = Depends(get_db_session),  # noqa: B008
     current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
     _: bool = Depends(Permiso(a.VER, m.COMBINACION)),  # noqa: B008
 ):   
     return services.get_combinacion_by_id(
         db, id
     )

@api.post("/", response_model=schemas.CombinacionGet)
async def add_new_combinacion(
    db: Session = Depends(get_db_session),
    data: Json[schemas.CombinacionCreateModel] = Form(...),
    current_user: schemas.AuthUser = Depends(get_current_user),
    _: bool = Depends(Permiso(a.CREAR, m.COMBINACION)),
):
    print("Crear ")
    return await services.create_combinacion(
        db,
        data,
        current_user.username,
        current_user.gestor_carga_id,
    )

@api.put("/{id}", response_model=schemas.CombinacionBaseModel)
async def edit_combinacion(
    id: int,
    db: Session = Depends(get_db_session),
    data: Json[schemas.CombinacionCreateModel] = Form(...),
    current_user: schemas.AuthUser = Depends(get_current_user),
    _: bool = Depends(Permiso(a.EDITAR, m.COMBINACION)),
):
    return await services.edit_combinacion(
        id,
        db,
        data,
        current_user.username,
    )

@api.get("/{id}/active", response_model=schemas.CombinacionesBD)
def active_combinacion_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.COMBINACION)),  # noqa: B008
):
    return services.change_combinacion_status(
        db, id, EstadoEnum.ACTIVO, current_user.username
    )


@api.get("/{id}/inactive", response_model=schemas.CombinacionesBD)
def inactive_combinacion_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.COMBINACION)),  # noqa: B008
):
    return services.change_combinacion_status(
        db, id, EstadoEnum.INACTIVO, current_user.username
    )
