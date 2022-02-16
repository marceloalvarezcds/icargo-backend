from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import Insumo
from app.repositories import get_tipo_insumo_by_descripcion, get_unidad_by_descripcion


def insumo_seeds(db: Session):
    try:
        combustible = get_tipo_insumo_by_descripcion(db, "COMBUSTIBLE")
        lubricantes = get_tipo_insumo_by_descripcion(db, "LUBRICANTES")
        litros = get_unidad_by_descripcion(db, "Litros")
        if combustible and lubricantes and litros:
            db.add(
                Insumo(
                    descripcion="GASOIL COMÚN",
                    tipo_id=combustible.id,
                    unidad_id=litros.id,
                )
            )
            db.add(
                Insumo(
                    descripcion="DIESEL PODIUM",
                    tipo_id=combustible.id,
                    unidad_id=litros.id,
                )
            )
            db.add(
                Insumo(
                    descripcion="ACEITE DE MOTOR COMÚN",
                    tipo_id=lubricantes.id,
                    unidad_id=litros.id,
                )
            )
            db.add(
                Insumo(
                    descripcion="ACEITE DE MOTOR PREMIUM",
                    tipo_id=lubricantes.id,
                    unidad_id=litros.id,
                )
            )
            db.commit()
    except IntegrityError:
        db.rollback()
