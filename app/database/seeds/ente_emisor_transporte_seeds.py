from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import EnteEmisorTransporte


def ente_emisor_transporte_seeds(db: Session):
    try:
        db.add(
            EnteEmisorTransporte(
                descripcion="Dirección Nacional de Transporte. DINATRAN"
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
