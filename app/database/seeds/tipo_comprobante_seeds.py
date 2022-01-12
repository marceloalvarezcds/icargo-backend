from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoComprobante


def tipo_comprobante_seeds(db: Session):
    try:
        db.add(TipoComprobante(descripcion="FACTURA"))
        db.add(TipoComprobante(descripcion="RECIBO"))
        db.add(TipoComprobante(descripcion="TICKET"))
        db.commit()
    except IntegrityError:
        db.rollback()
