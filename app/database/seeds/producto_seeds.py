from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import Producto


def producto_seeds(db: Session):
    try:
        db.add(Producto(descripcion="Trigo"))
        db.add(Producto(descripcion="Soja"))
        db.add(Producto(descripcion="Fertilizante a Granel"))
        db.add(Producto(descripcion="Canola"))
        db.add(Producto(descripcion="Aceite de Soja"))
        db.add(Producto(descripcion="Ganado"))
        db.commit()
    except IntegrityError:
        db.rollback()
