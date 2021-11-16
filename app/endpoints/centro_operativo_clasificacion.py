from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.dependencies import Permiso, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.CentroOperativoClasificacion])
async def read_centro_operativo_clasificacion_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(  # noqa: B008
        Permiso(a.LISTAR, m.CENTRO_OPERATIVO_CLASIFICACION)
    ),
):
    return repositories.get_centro_operativo_clasificacion_list(db)
