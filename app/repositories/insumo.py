from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Insumo


def get_insumo_by_descripcion(db: Session, descripcion: str) -> Optional[Insumo]:
    return db.query(Insumo).filter(Insumo.descripcion == descripcion).first()


def get_insumo_list(db: Session) -> List[Insumo]:
    return db.query(Insumo).order_by(Insumo.descripcion).all()


def get_insumo_list_by_tipo_insumo_id(db: Session, tipo_insumo_id: int) -> List[Insumo]:
    return (
        db.query(Insumo)
        .filter(Insumo.tipo_id == tipo_insumo_id)
        .order_by(Insumo.descripcion)
        .all()
    )
