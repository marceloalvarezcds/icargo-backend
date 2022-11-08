from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoCuenta, TipoMovimiento


def tipo_movimiento_seeds(db: Session, descripcion: str, cuenta: TipoCuenta):
    try:
        db.add(
            TipoMovimiento(
                descripcion=descripcion,
                cuenta_id=cuenta.id,
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
