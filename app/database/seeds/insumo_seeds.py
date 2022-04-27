from sqlalchemy.orm import Session  # type: ignore

from app.models import Insumo
from app.repositories import (
    get_insumo_by_descripcion,
    get_tipo_insumo_by_descripcion,
    get_unidad_by_descripcion,
)


def create_insumo(db: Session, descripcion: str, tipo_id: int, unidad_id: int):
    insumo = get_insumo_by_descripcion(db, descripcion)
    if insumo is None:
        insumo = Insumo(descripcion=descripcion, tipo_id=tipo_id, unidad_id=unidad_id)
        db.add(insumo)
        db.commit()


def insumo_seeds(db: Session):
    combustible = get_tipo_insumo_by_descripcion(db, "COMBUSTIBLE")
    lubricantes = get_tipo_insumo_by_descripcion(db, "LUBRICANTES")
    # litros = get_unidad_by_descripcion(db, "Litros")  # TODO
    kilogramos = get_unidad_by_descripcion(db, "Kilogramos")
    if combustible and lubricantes and kilogramos:
        create_insumo(
            db,
            "GASOIL COMÚN",
            combustible.id,
            kilogramos.id,
        )
        create_insumo(
            db,
            "ACEITE DE MOTOR",
            lubricantes.id,
            kilogramos.id,
        )
