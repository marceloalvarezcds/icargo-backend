from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/insumo/{insumo_id}", response_model=List[schemas.InsumoPuntoVenta])
async def read_insumo_punto_venta_list_by_insumo_id(
    insumo_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.INSUMO_PUNTO_VENTA)),  # noqa: B008
):
    return repositories.get_insumo_punto_venta_list_by_insumo_id(
        db, insumo_id, current_user.gestor_carga_id
    )
