from sqlalchemy.orm import Session  # type: ignore

from app.models import Producto
from app.repositories import get_producto_by_descripcion, get_tipo_carga_by_descripcion


def create_producto(db: Session, descripcion: str, tipo_carga_id: int):
    producto = get_producto_by_descripcion(db, descripcion)
    if producto is None:
        producto = Producto(descripcion=descripcion, tipo_carga_id=tipo_carga_id)
        db.add(producto)
        db.commit()


def producto_seeds(db: Session):
    seca = get_tipo_carga_by_descripcion(db, "SECA")
    liquida = get_tipo_carga_by_descripcion(db, "LÍQUIDA")
    if seca and liquida:
        create_producto(db, "Trigo en granos", seca.id)
        create_producto(db, "Soja en granos", seca.id)
        create_producto(db, "Fertilizante a Granel", seca.id)
        create_producto(db, "Canola en granos", seca.id)
        create_producto(db, "Aceite de Soja", liquida.id)
