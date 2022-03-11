from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.enums import TipoMovimientoEnum
from app.models import TipoDocumentoRelacionado

from .tipo_cuenta_seeds import tipo_cuenta_seeds
from .tipo_movimiento_seeds import tipo_movimiento_seeds


def tipo_documento_relacionado_seeds(db: Session):
    try:
        oc = TipoDocumentoRelacionado(descripcion="OC")
        otro = TipoDocumentoRelacionado(descripcion="Otro")
        db.add(oc)
        db.add(otro)
        db.commit()
        db.refresh(oc)
        db.refresh(otro)
        tipo_cuenta_seeds(db, "Viajes", oc)
        tipo_cuenta_seeds(db, "Otro", otro)
        tipo_movimiento_seeds(db, TipoMovimientoEnum.ANTICIPO.value, oc)
        tipo_movimiento_seeds(db, TipoMovimientoEnum.FLETE.value, oc)
        tipo_movimiento_seeds(db, TipoMovimientoEnum.COMPLEMENTO.value, oc)
        tipo_movimiento_seeds(db, TipoMovimientoEnum.DESCUENTO.value, oc)
        tipo_movimiento_seeds(db, TipoMovimientoEnum.MERMA.value, oc)
        tipo_movimiento_seeds(db, TipoMovimientoEnum.OTRO.value, otro)
    except IntegrityError:
        db.rollback()
