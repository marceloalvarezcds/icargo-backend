from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.dependencies import Permiso, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import TipoIncidente
from app.schemas.seleccionable_base_model import (
    SeleccionableBaseModel,
    SeleccionableFormBaseModel,
)
from app.services import seleccionable_service as service

api = APIRouter()


@api.get("/", response_model=List[schemas.TipoIncidente])
async def read_tipo_incidente_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TIPO_EVALUACION)),  # noqa: B008
):
    return repositories.get_tipo_incidente_list(db)


@api.get("/active_list", response_model=List[SeleccionableBaseModel])
async def read_evaluacion_active_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.TIPO_EVALUACION)),  # noqa: B008
):
    return service.get_active_list(TipoIncidente, db)