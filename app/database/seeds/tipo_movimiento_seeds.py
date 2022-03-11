from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoDocumentoRelacionado, TipoMovimiento


def tipo_movimiento_seeds(
    db: Session, descripcion: str, tipo_documento_relacionado: TipoDocumentoRelacionado
):
    try:
        db.add(
            TipoMovimiento(
                descripcion=descripcion,
                tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
