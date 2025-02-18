from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore

from app.enums import TipoCuentaEnum
from app.enums.estado import EstadoEnum
from app.models import TipoCuenta, TipoMovimiento


def get_tipo_movimiento_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoMovimiento]:
    return (
        db.query(TipoMovimiento)
        .filter(TipoMovimiento.descripcion == descripcion)
        .first()
    )


def get_tipo_movimiento_list(db: Session) -> List[TipoMovimiento]:
    return db.query(TipoMovimiento).order_by(TipoMovimiento.id.desc()).all()


def get_tipo_movimiento_list_by_tipo_cuenta_other_than_viajes(
    db: Session,
) -> List[TipoMovimiento]:
    return (
        db.query(TipoMovimiento)
        .join(TipoMovimiento.cuenta)
        .filter(TipoCuenta.descripcion != TipoCuentaEnum.VIAJES.value)
        .order_by(TipoMovimiento.id.desc())
        .all()
    )


def get_tipo_movimiento_active_list_by_tipo_cuenta_other_than_viajes(
    db: Session,
) -> List[TipoMovimiento]:
    return (
        db.query(TipoMovimiento)
        .join(TipoMovimiento.cuenta)
        .filter(
            and_(
                TipoCuenta.descripcion != TipoCuentaEnum.VIAJES.value,
                TipoMovimiento.estado == EstadoEnum.ACTIVO.value,
            )
        )
        .order_by(TipoMovimiento.id.desc())
        .all()
    )


def get_tipo_movimiento_active_list(
    db: Session,
) -> List[TipoMovimiento]:
    return (
        db.query(TipoMovimiento)
        .join(TipoMovimiento.cuenta)
        .filter(
            TipoMovimiento.estado == EstadoEnum.ACTIVO.value,
        )
        .order_by(TipoMovimiento.id.desc())
        .all()
    )
