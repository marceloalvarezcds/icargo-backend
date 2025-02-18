from http import HTTPStatus
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import repositories as r
from app.models import TipoCuenta, TipoMovimiento
from app.schemas import TipoMovimientoForm
from app.services import generic_service as service


def get_tipo_movimiento_list(
    db: Session,
) -> List[TipoMovimiento]:
    return r.get_tipo_movimiento_list(db)

def get_tipo_movimiento_list_by_tipo_cuenta_other_than_viajes(
    db: Session,
) -> List[TipoMovimiento]:
    return r.get_tipo_movimiento_list_by_tipo_cuenta_other_than_viajes(db)


def get_tipo_movimiento_active_list_by_tipo_cuenta_other_than_viajes(
    db: Session,
) -> List[TipoMovimiento]:
    return r.get_tipo_movimiento_active_list_by_tipo_cuenta_other_than_viajes(db)


def get_tipo_movimiento_active_list(
    db: Session,
) -> List[TipoMovimiento]:
    return r.get_tipo_movimiento_active_list(db)


def _check_codigo(codigo: str):
    if len(codigo) > 2:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="El código debe poseer hasta 2 caracteres",
        )


def create_tipo_movimiento(
    db: Session, data: TipoMovimientoForm, modified_by: str
) -> TipoMovimiento:
    codigo = data.codigo
    _check_codigo(codigo)
    cuenta: TipoCuenta = service.get_by_id(TipoCuenta, db, data.cuenta_id)
    return service.create(
        TipoMovimiento,
        db,
        data,
        modified_by,
        f"El Concepto con cuenta {cuenta.descripcion} y código {codigo} ya existe",
        codigo=codigo,
        cuenta_id=data.cuenta_id,
    )


def edit_tipo_movimiento(
    id: int, db: Session, data: TipoMovimientoForm, modified_by: str
) -> TipoMovimiento:
    codigo = data.codigo
    _check_codigo(codigo)
    cuenta: TipoCuenta = service.get_by_id(TipoCuenta, db, data.cuenta_id)
    return service.edit(
        TipoMovimiento,
        db,
        id,
        data,
        modified_by,
        f"El Concepto con cuenta {cuenta.descripcion} y código {codigo} ya existe",
        codigo=codigo,
        cuenta_id=data.cuenta_id,
    )
