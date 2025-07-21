from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_db_session, Permisos
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/tipo_anticipo_insumo", response_model=List[schemas.FleteAnticipoForm])
async def read_tipo_anticipo_insumo_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permisos(a.LISTAR, [m.FLETE_ANTICIPO, m.FLETE])),  # noqa: B008
):
    return services.get_tipo_anticipo_insumo_list(db)


@api.get(
    "/tipo/{tipo_id}/flete/{flete_id}",
    response_model=schemas.FleteAnticipo,
)
async def read_flete_anticipo_by_tipo_id_and_flete_id(
    tipo_id: int,
    flete_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.FLETE_ANTICIPO)),  # noqa: B008
):
    return repositories.get_flete_anticipo_by(db, tipo_id, flete_id)


@api.get(
    "/tipo/{tipo_id}/flete/{flete_id}/tipo_insumo/{tipo_insumo_id}",
    response_model=schemas.FleteAnticipo,
)
async def read_flete_anticipo_by_tipo_id_and_flete_id_and_tipo_insumo_id(
    tipo_id: int,
    flete_id: int,
    tipo_insumo_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.FLETE_ANTICIPO)),  # noqa: B008
):
    return repositories.get_flete_anticipo_by(db, tipo_id, flete_id, tipo_insumo_id)
