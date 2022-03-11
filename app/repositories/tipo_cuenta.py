from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoCuenta


def get_tipo_cuenta_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoCuenta]:
    return db.query(TipoCuenta).filter(TipoCuenta.descripcion == descripcion).first()


def get_tipo_cuenta_list(db: Session) -> List[TipoCuenta]:
    return db.query(TipoCuenta).order_by(TipoCuenta.descripcion).all()
