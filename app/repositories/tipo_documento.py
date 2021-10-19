from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoDocumento


def get_tipo_documento_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoDocumento]:
    return (
        db.query(TipoDocumento).filter(TipoDocumento.descripcion == descripcion).first()
    )
