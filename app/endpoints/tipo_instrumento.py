from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, services
from app.dependencies import Permiso, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/via_banco", response_model=List[schemas.TipoInstrumento])
async def read_tipo_instrumento_list_via_banco(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TIPO_INSTRUMENTO)),  # noqa: B008
):
    return services.get_tipo_instrumento_via_banco(db)
