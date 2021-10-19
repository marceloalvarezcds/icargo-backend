from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoDocumento


def tipo_documento_seeds(db: Session):
    try:
        db.add(TipoDocumento(descripcion="RUC"))
        db.add(TipoDocumento(descripcion="Cédula"))
        db.add(TipoDocumento(descripcion="Pasaporte"))
        db.commit()
    except IntegrityError:
        db.rollback()
