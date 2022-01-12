from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import Insumo
from app.repositories import get_tipo_anticipo_by_descripcion, get_unidad_by_descripcion


def insumo_seeds(db: Session):
    try:
        efectivo = get_tipo_anticipo_by_descripcion(db, "EFECTIVO")
        combustible = get_tipo_anticipo_by_descripcion(db, "COMBUSTIBLE")
        lubricantes = get_tipo_anticipo_by_descripcion(db, "LUBRICANTES")
        litros = get_unidad_by_descripcion(db, "Litros")
        if efectivo and combustible and lubricantes and litros:
            db.add(Insumo(descripcion="VIÁTICO", tipo_id=efectivo.id))
            db.add(
                Insumo(
                    descripcion="GASOIL COMÚN",
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
            db.commit()
    except IntegrityError:
        db.rollback()
