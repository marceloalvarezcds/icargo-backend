from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import EnteEmisorAutomotor
from app.repositories import get_pais_by_nombre_corto


def ente_emisor_automotor_seeds(db: Session):
    try:
        paraguay = get_pais_by_nombre_corto(db, "PY")
        if paraguay:
            db.add(
                EnteEmisorAutomotor(
                    descripcion="Dirección del Registro de Automotores",
                    pais_id=paraguay.id,
                )
            )
            db.commit()
    except IntegrityError:
        db.rollback()
