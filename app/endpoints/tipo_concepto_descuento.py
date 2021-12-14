from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.dependencies import Permiso, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.TipoConceptoDescuento])
async def read_tipo_concepto_descuento_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TIPO_CONCEPTO_DESCUENTO)),  # noqa: B008
):
    return repositories.get_tipo_concepto_descuento_list(db)
