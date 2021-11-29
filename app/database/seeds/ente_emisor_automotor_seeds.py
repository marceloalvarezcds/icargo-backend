from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import EnteEmisorAutomotor


def ente_emisor_automotor_seeds(db: Session):
    try:
        db.add(EnteEmisorAutomotor(descripcion="Dirección del Registro de Automotores"))
        db.commit()
    except IntegrityError:
        db.rollback()
