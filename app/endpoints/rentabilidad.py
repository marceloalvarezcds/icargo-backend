from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import models, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.Rentabilidad])
async def read_rentabilidad_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.RENTABILIDAD)),  # noqa: B008
):
    return services.get_rentabilidad_list(db, current_user.gestor_carga_id)


@api.get("/reports")
async def rentabilidad_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.RENTABILIDAD)),  # noqa: B008
):
    return services.get_rentabilidad_reports(db, current_user.gestor_carga_id)
