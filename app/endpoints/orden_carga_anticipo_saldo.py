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
    "/orden_carga/{orden_carga_id}/anticipo_saldo",
    response_model=RoundedDecimal,
)
async def update_orden_carga_anticipo_saldo_by(
    orden_carga_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.ORDEN_CARGA_ANTICIPO_SALDO)),  # noqa: B008
):
    return services.update_orden_carga_anticipo_saldo_by_orden_carga_id(
        db, orden_carga_id, current_user.username
    )


@api.get("/actualizar-retiro/{flete_id_anterior}/{flete_id_nuevo}/{orden_carga_id}", response_model=Optional[schemas.OrdenCargaAnticipoSaldo])
async def actualizar_total_retirado_oc(
    flete_id_anterior: int,
    flete_id_nuevo: int,
    orden_carga_id: int,
    db: Session = Depends(get_db_session),
    current_user: schemas.AuthUser = Depends(get_current_user),
    _: bool = Depends(Permiso(a.EDITAR, m.ORDEN_CARGA)),
):
    return services.update_total_retirado(
        db,
        orden_carga_id,
        flete_id_anterior,
        flete_id_nuevo,
        current_user.username
    )


@api.get(
    "/crear-saldo-desde-flete-anterior/{flete_anticipo_id}/{orden_carga_id}",
    response_model=RoundedDecimal,
)
async def crear_saldo_desde_flete_anterior(
    flete_anticipo_id: int,
    orden_carga_id: int,
    db: Session = Depends(get_db_session),
    current_user: schemas.AuthUser = Depends(get_current_user),
    _: bool = Depends(Permiso(a.EDITAR, m.ORDEN_CARGA_ANTICIPO_SALDO)),
):
    return services.get_saldo_anticipo_desde_flete_anterior(
        db=db,
        flete_anticipo_id=flete_anticipo_id,
        orden_carga_id=orden_carga_id,
        modified_by=current_user.username
    )


@api.get(
    "/actualizar-saldo-anticipo/{flete_anticipo_id}/{orden_carga_id}/{monto_retirado}",
    response_model=schemas.OrdenCargaAnticipoSaldo,
)
async def actualizar_saldo_anticipo(
    flete_anticipo_id: int,
    orden_carga_id: int,
    monto_retirado: Decimal,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.ORDEN_CARGA_ANTICIPO_SALDO)),  # noqa: B008
):
    flete_anticipo = repositories.get_flete_anticipo_by_id(db, flete_anticipo_id)
    orden_carga = repositories.get_orden_carga_by_id(db, orden_carga_id)

    if not flete_anticipo or not orden_carga:
        raise HTTPException(status_code=404, detail="Flete anticipo u orden de carga no encontrados")

    total_complemento = services.get_total_complemento(
        orden_carga.complementos,
        flete_anticipo.tipo_descripcion == enums.TipoAnticipoEnum.EFECTIVO.value,
    )

    return services.update_orden_carga_anticipo_saldo(
        db=db,
        flete_anticipo=flete_anticipo,
        orden_carga=orden_carga,
        monto_retirado=monto_retirado,
        total_complemento=total_complemento,
        modified_by=current_user.username,
    )
