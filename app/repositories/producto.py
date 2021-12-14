from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Producto


def get_producto_by_descripcion(db: Session, descripcion: str) -> Optional[Producto]:
    return db.query(Producto).filter(Producto.descripcion == descripcion).first()


def get_producto_list(db: Session) -> List[Producto]:
    return (
        db.query(Producto)
        .order_by(Producto.descripcion)
        .order_by(Producto.descripcion)
        .all()
    )
