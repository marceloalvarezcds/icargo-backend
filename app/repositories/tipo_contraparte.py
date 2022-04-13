from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoContraparte


def get_tipo_contraparte_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoContraparte]:
    return (
        db.query(TipoContraparte)
        .filter(TipoContraparte.descripcion == descripcion)
        .first()
    )


def get_tipo_comprobante_by_id(db: Session, id: int) -> Optional[TipoContraparte]:
    return db.query(TipoContraparte).get(id)


def get_tipo_contraparte_list(db: Session) -> List[TipoContraparte]:
    return db.query(TipoContraparte).order_by(TipoContraparte.descripcion).all()
