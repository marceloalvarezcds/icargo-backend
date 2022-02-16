from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.enums import TipoAnticipoEnum
from app.models import TipoAnticipo


def tipo_anticipo_seeds(db: Session):
    try:
        db.add(TipoAnticipo(descripcion=TipoAnticipoEnum.EFECTIVO.value))
        db.add(TipoAnticipo(descripcion=TipoAnticipoEnum.INSUMOS.value))
        db.commit()
    except IntegrityError:
        db.rollback()
