from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoContraparte


def tipo_contraparte_seeds(db: Session):
    try:
        db.add(TipoContraparte(descripcion="Propietario"))
        db.add(TipoContraparte(descripcion="Chofer"))
        db.add(TipoContraparte(descripcion="Remitente"))
        db.add(TipoContraparte(descripcion="Proveedor"))
        db.add(TipoContraparte(descripcion="Otros"))
        db.commit()
    except IntegrityError:
        db.rollback()
