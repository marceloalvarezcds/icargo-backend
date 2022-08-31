from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.Insumo])
async def read_insumo_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.INSUMO)),  # noqa: B008
):
    return repositories.get_insumo_list(db)


@api.get("/tipo_insumo/{tipo_insumo_id}", response_model=List[schemas.Insumo])
async def read_insumo_list_by_tipo_insumo_id(
    tipo_insumo_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.INSUMO)),  # noqa: B008
):
    return services.get_insumo_list_by_tipo_insumo_id_and_gestor_carga_id(
        db, tipo_insumo_id, current_user.gestor_carga_id
    )
