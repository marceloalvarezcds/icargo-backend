from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import Producto
from app.repositories import get_tipo_carga_by_descripcion


def producto_seeds(db: Session):
    try:
        seca = get_tipo_carga_by_descripcion(db, "SECA")
        liquida = get_tipo_carga_by_descripcion(db, "LÍQUIDA")
        if seca and liquida:
            db.add(Producto(descripcion="Trigo", tipo_carga_id=seca.id))
            db.add(Producto(descripcion="Soja", tipo_carga_id=seca.id))
            db.add(Producto(descripcion="Fertilizante a Granel", tipo_carga_id=seca.id))
            db.add(Producto(descripcion="Canola", tipo_carga_id=seca.id))
            db.add(Producto(descripcion="Aceite de Soja", tipo_carga_id=liquida.id))
            db.add(Producto(descripcion="Ganado", tipo_carga_id=seca.id))
            db.commit()
    except IntegrityError:
        db.rollback()
