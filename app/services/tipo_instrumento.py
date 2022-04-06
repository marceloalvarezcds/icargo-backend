from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app.enums import InstrumentoViaEnum
from app.models import InstrumentoVia, TipoInstrumento
from app.repositories import (
    get_instrumento_via_by_descripcion,
    get_tipo_instrumento_list_by_via_id,
)


def get_instrumento_via_by_enum(db: Session, via: InstrumentoViaEnum) -> InstrumentoVia:
    obj = get_instrumento_via_by_descripcion(db, via.value)
    if not obj:
        raise HTTPException(status_code=404, detail="Vía no encontrada")
    return obj


def get_tipo_instrumento_via_banco(db: Session) -> List[TipoInstrumento]:
    via_banco = get_instrumento_via_by_enum(db, InstrumentoViaEnum.BANCO)
    return get_tipo_instrumento_list_by_via_id(db, via_banco.id)
