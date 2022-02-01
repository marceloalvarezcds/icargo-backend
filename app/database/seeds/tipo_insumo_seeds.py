from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.enums import TipoInsumoEnum
from app.models import TipoInsumo


def tipo_insumo_seeds(db: Session):
    try:
        db.add(TipoInsumo(descripcion=TipoInsumoEnum.COMBUSTIBLE.value))
        db.add(TipoInsumo(descripcion=TipoInsumoEnum.LUBRICANTES.value))
        db.commit()
    except IntegrityError:
        db.rollback()
