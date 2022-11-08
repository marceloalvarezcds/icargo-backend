from typing import List

from sqlalchemy.orm import Session  # type: ignore

from app import repositories as r
from app.models import TipoMovimiento


def get_tipo_movimiento_list_by_tipo_cuenta_other_than_viajes(
    db: Session,
) -> List[TipoMovimiento]:
    return r.get_tipo_movimiento_list_by_tipo_cuenta_other_than_viajes(db)


def get_tipo_movimiento_active_list_by_tipo_cuenta_other_than_viajes(
    db: Session,
) -> List[TipoMovimiento]:
    return r.get_tipo_movimiento_active_list_by_tipo_cuenta_other_than_viajes(db)
