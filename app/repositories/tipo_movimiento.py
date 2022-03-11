from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoMovimiento


def get_tipo_movimiento_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoMovimiento]:
    return (
        db.query(TipoMovimiento)
        .filter(TipoMovimiento.descripcion == descripcion)
        .first()
    )


def get_tipo_movimiento_list(db: Session) -> List[TipoMovimiento]:
    return db.query(TipoMovimiento).order_by(TipoMovimiento.descripcion).all()
