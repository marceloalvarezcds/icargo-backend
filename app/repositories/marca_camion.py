from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import MarcaCamion


def get_marca_camion_by_descripcion(
    db: Session, descripcion: str
) -> Optional[MarcaCamion]:
    return db.query(MarcaCamion).filter(MarcaCamion.descripcion == descripcion).first()


def get_marca_camion_list(db: Session) -> List[MarcaCamion]:
    return db.query(MarcaCamion).order_by(MarcaCamion.descripcion).all()
