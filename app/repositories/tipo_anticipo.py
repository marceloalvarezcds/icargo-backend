from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoAnticipo


def get_tipo_anticipo_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoAnticipo]:
    return (
        db.query(TipoAnticipo).filter(TipoAnticipo.descripcion == descripcion).first()
    )


def get_tipo_anticipo_by_id(db: Session, id: int) -> Optional[TipoAnticipo]:
    return db.query(TipoAnticipo).get(id)


def get_tipo_anticipo_list(db: Session) -> List[TipoAnticipo]:
    return db.query(TipoAnticipo).order_by(TipoAnticipo.descripcion).all()
