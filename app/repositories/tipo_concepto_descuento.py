from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoConceptoDescuento


def get_tipo_concepto_descuento_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoConceptoDescuento]:
    return (
        db.query(TipoConceptoDescuento)
        .filter(TipoConceptoDescuento.descripcion == descripcion)
        .first()
    )


def get_tipo_concepto_descuento_list(db: Session) -> List[TipoConceptoDescuento]:
    return (
        db.query(TipoConceptoDescuento)
        .order_by(TipoConceptoDescuento.descripcion)
        .all()
    )
