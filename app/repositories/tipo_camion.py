from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoCamion


def get_tipo_camion_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoCamion]:
    return db.query(TipoCamion).filter(TipoCamion.descripcion == descripcion).first()


def get_tipo_camion_list(db: Session) -> List[TipoCamion]:
    return db.query(TipoCamion).order_by(TipoCamion.descripcion).all()
