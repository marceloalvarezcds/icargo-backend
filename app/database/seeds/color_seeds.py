from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import Color


def color_seeds(db: Session):
    try:
        db.add(Color(descripcion="AZUL", color="#0000ff"))
        db.add(Color(descripcion="BLANCO", color="#ffffff"))
        db.add(Color(descripcion="GRIS", color="#9b9b9b"))
        db.add(Color(descripcion="NEGRO", color="#000000"))
        db.add(Color(descripcion="ROJO", color="#ff0000"))
        db.add(Color(descripcion="VERDE", color="#00ff00"))
        db.commit()
    except IntegrityError:
        db.rollback()
