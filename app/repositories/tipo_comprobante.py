from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoComprobante


def get_tipo_comprobante_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoComprobante]:
    return (
        db.query(TipoComprobante)
        .filter(TipoComprobante.descripcion == descripcion)
        .first()
    )


def get_tipo_comprobante_list(db: Session) -> List[TipoComprobante]:
    return db.query(TipoComprobante).order_by(TipoComprobante.descripcion).all()
