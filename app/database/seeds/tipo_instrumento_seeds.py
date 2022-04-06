from sqlalchemy.orm import Session  # type: ignore

from app.enums import InstrumentoViaEnum
from app.models import TipoInstrumento
from app.repositories import (
    get_instrumento_via_by_descripcion,
    get_tipo_instrumento_by_descripcion,
)


def create_tipo_instrumento(db: Session, descripcion: str, via: InstrumentoViaEnum):
    instrumento_via = get_instrumento_via_by_descripcion(db, via.value)
    tipo_instrumento = get_tipo_instrumento_by_descripcion(db, descripcion)
    if instrumento_via and tipo_instrumento is None:
        tipo_instrumento = TipoInstrumento(
            descripcion=descripcion, via_id=instrumento_via.id
        )
        db.add(tipo_instrumento)
        db.commit()


def tipo_instrumento_seeds(db: Session):
    create_tipo_instrumento(db, "Efectivo", InstrumentoViaEnum.CAJA)
    create_tipo_instrumento(db, "Cheque", InstrumentoViaEnum.BANCO)
    create_tipo_instrumento(db, "Transferencia", InstrumentoViaEnum.BANCO)
    create_tipo_instrumento(db, "Tarjeta de Débito", InstrumentoViaEnum.BANCO)
