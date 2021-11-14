from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.dependencies import Permiso, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/{pais_id}", response_model=List[schemas.Localidad])
async def read_localidad_list(
    pais_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.LOCALIDAD)),  # noqa: B008
):
    return repositories.get_localidad_list(db, pais_id)
