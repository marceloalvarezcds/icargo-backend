from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoRegistro


def get_tipo_registro_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoRegistro]:
    return (
        db.query(TipoRegistro).filter(TipoRegistro.descripcion == descripcion).first()
    )


def get_tipo_registro_list(db: Session) -> List[TipoRegistro]:
    return db.query(TipoRegistro).order_by(TipoRegistro.descripcion).all()
