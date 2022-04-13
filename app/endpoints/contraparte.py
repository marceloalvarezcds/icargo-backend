from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, services
from app.dependencies import Permiso, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get(
    "/tipo_contraparte/{tipo_contraparte_id}", response_model=List[schemas.Contraparte]
)
async def read_contraparte_list_by_tipo_contraparte_id(
    tipo_contraparte_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TIPO_CONTRAPARTE)),  # noqa: B008
):
    return services.get_contraparte_list_by_tipo_contraparte_id(db, tipo_contraparte_id)
