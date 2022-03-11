from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoDocumentoRelacionado


def get_tipo_documento_relacionado_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoDocumentoRelacionado]:
    return (
        db.query(TipoDocumentoRelacionado)
        .filter(TipoDocumentoRelacionado.descripcion == descripcion)
        .first()
    )


def get_tipo_documento_relacionado_list(db: Session) -> List[TipoDocumentoRelacionado]:
    return (
        db.query(TipoDocumentoRelacionado)
        .order_by(TipoDocumentoRelacionado.descripcion)
        .all()
    )
