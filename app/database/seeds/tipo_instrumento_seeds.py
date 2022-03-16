from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoInstrumento
from app.repositories import get_tipo_instrumento_by_descripcion


def create_tipo_instrumento(db: Session, descripcion: str):
    tipo_instrumento = get_tipo_instrumento_by_descripcion(db, descripcion)
    if tipo_instrumento is None:
        tipo_instrumento = TipoInstrumento(descripcion=descripcion)
        db.add(tipo_instrumento)
        db.commit()


def tipo_instrumento_seeds(db: Session):
    create_tipo_instrumento(db, "Cheque")
    create_tipo_instrumento(db, "Transferencia")
    create_tipo_instrumento(db, "Tarjeta de Débito")
