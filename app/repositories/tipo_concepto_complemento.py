from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoConceptoComplemento


def get_tipo_concepto_complemento_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoConceptoComplemento]:
    return (
        db.query(TipoConceptoComplemento)
        .filter(TipoConceptoComplemento.descripcion == descripcion)
        .first()
    )


def get_tipo_concepto_complemento_list(db: Session) -> List[TipoConceptoComplemento]:
    return (
        db.query(TipoConceptoComplemento)
        .order_by(TipoConceptoComplemento.descripcion)
        .all()
    )
