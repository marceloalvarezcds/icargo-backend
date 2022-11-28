from typing import Optional

from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoCuenta, TipoDocumentoRelacionado


def tipo_cuenta_seeds(
    db: Session, descripcion: str, tipo_documento_relacionado: TipoDocumentoRelacionado
) -> Optional[TipoCuenta]:
    try:
        cuenta = TipoCuenta(
            descripcion=descripcion,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
        )
        db.add(cuenta)
        db.commit()
        return cuenta
    except IntegrityError:
        db.rollback()
        return None
