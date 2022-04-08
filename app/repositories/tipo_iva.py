from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoIva


def get_tipo_iva_by_descripcion(db: Session, descripcion: str) -> Optional[TipoIva]:
    return db.query(TipoIva).filter(TipoIva.descripcion == descripcion).first()


def get_tipo_iva_list(db: Session) -> List[TipoIva]:
    return (
        db.query(TipoIva)
        .order_by(TipoIva.descripcion)
        .order_by(TipoIva.descripcion)
        .all()
    )
