from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.enums import TipoCuentaEnum, TipoMovimientoEnum
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
        viajes = tipo_cuenta_seeds(db, TipoCuentaEnum.VIAJES.value, oc)
        otra = tipo_cuenta_seeds(db, TipoCuentaEnum.OTRO.value, otro)
        if viajes:
            tipo_movimiento_seeds(db, TipoMovimientoEnum.ANTICIPO.value, viajes)
            tipo_movimiento_seeds(db, TipoMovimientoEnum.FLETE.value, viajes)
            tipo_movimiento_seeds(db, TipoMovimientoEnum.COMPLEMENTO.value, viajes)
            tipo_movimiento_seeds(db, TipoMovimientoEnum.DESCUENTO.value, viajes)
            tipo_movimiento_seeds(db, TipoMovimientoEnum.MERMA.value, viajes)
        if otra:
            tipo_movimiento_seeds(db, TipoMovimientoEnum.OTRO.value, otra)
    except IntegrityError:
        db.rollback()
