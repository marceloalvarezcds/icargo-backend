from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app import enums
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.schemas.rounded_decimal_model import RoundedDecimal
from pydantic import Json

api = APIRouter()


@api.get(
    "/flete_anticipo/{flete_anticipo_id}/orden_carga/{orden_carga_id}",
    response_model=RoundedDecimal,
)
async def read_saldo_anticipo_by_flete_anticipo_id_and_orden_carga_id(
    flete_anticipo_id: int,
    orden_carga_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.ORDEN_CARGA_ANTICIPO_SALDO)),  # noqa: B008
):
    return services.get_saldo_anticipo_by_flete_anticipo_id_and_orden_carga_id(
        db, flete_anticipo_id, orden_carga_id, current_user.username
    )


@api.get(
    "/orden-carga/{orden_carga_id}/flete/{flete_id}/saldo-combustible",
    response_model=RoundedDecimal,
)
async def get_saldo_combustible_orden_carga(
    orden_carga_id: int,
    flete_id: int,
    db: Session = Depends(get_db_session),
    current_user: schemas.AuthUser = Depends(get_current_user),
    _: bool = Depends(Permiso(a.EDITAR, m.ORDEN_CARGA_ANTICIPO_SALDO)),
):
    return services.get_saldo_anticipo_por_flete_y_oc(
        db=db,
        orden_carga_id=orden_carga_id,
        flete_id=flete_id,
        modified_by=current_user.username
    )
