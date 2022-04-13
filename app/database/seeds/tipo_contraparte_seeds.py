from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.enums import TipoContraparteEnum
from app.models import TipoContraparte


def tipo_contraparte_seeds(db: Session):
    try:
        db.add(TipoContraparte(descripcion=TipoContraparteEnum.PROPIETARIO.value))
        db.add(TipoContraparte(descripcion=TipoContraparteEnum.CHOFER.value))
        db.add(TipoContraparte(descripcion=TipoContraparteEnum.REMITENTE.value))
        db.add(TipoContraparte(descripcion=TipoContraparteEnum.PROVEEDOR.value))
        db.add(TipoContraparte(descripcion=TipoContraparteEnum.OTRO.value))
        db.commit()
    except IntegrityError:
        db.rollback()
