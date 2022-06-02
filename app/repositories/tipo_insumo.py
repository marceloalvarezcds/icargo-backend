from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoInsumo


def get_tipo_insumo_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoInsumo]:
    return db.query(TipoInsumo).filter(TipoInsumo.descripcion == descripcion).first()


def get_tipo_insumo_by_id(db: Session, id: int) -> Optional[TipoInsumo]:
    return db.query(TipoInsumo).get(id)


def get_tipo_insumo_list(db: Session) -> List[TipoInsumo]:
    return db.query(TipoInsumo).order_by(TipoInsumo.descripcion).all()
