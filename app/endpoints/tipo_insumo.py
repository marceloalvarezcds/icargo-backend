from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.TipoInsumo])
async def read_tipo_insumo_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TIPO_INSUMO)),  # noqa: B008
):
    return repositories.get_tipo_insumo_list(db)


@api.get("/flete/{flete_id}", response_model=List[schemas.TipoInsumo])
async def read_tipo_insumo_list_by_flete_id(
    flete_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TIPO_INSUMO)),  # noqa: B008
):
    return services.get_tipo_insumo_list_by_flete_id_and_gestor_carga_id(
        db, flete_id, current_user.gestor_carga_id
    )
