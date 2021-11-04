from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoDocumento


def get_tipo_documento_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoDocumento]:
    return (
        db.query(TipoDocumento).filter(TipoDocumento.descripcion == descripcion).first()
    )


def get_tipo_documento_list(db: Session) -> List[TipoDocumento]:
    return db.query(TipoDocumento).order_by(TipoDocumento.descripcion).all()
