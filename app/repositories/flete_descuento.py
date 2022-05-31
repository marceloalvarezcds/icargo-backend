from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import FleteDescuento
from app.schemas import FleteDescuentoForm


def get_flete_descuento_by(
    db: Session,
    concepto_id: int,
    propietario_moneda_id: int,
    propietario_monto: int,
    proveedor_moneda_id: int,
    proveedor_monto: int,
    flete_id: int,
) -> Optional[FleteDescuento]:
    return (
        db.query(FleteDescuento)
        .filter(
            FleteDescuento.concepto_id == concepto_id,
            FleteDescuento.propietario_moneda_id == propietario_moneda_id,
            FleteDescuento.propietario_monto == propietario_monto,
            FleteDescuento.proveedor_moneda_id == proveedor_moneda_id,
            FleteDescuento.proveedor_monto == proveedor_monto,
            FleteDescuento.flete_id == flete_id,
        )
        .first()
    )


def get_flete_descuento_by_id(
    db: Session,
    id: int,
) -> Optional[FleteDescuento]:
    return db.query(FleteDescuento).filter(FleteDescuento.id == id).first()


def create_flete_descuento(
    db: Session,
    flete_id: int,
    data: FleteDescuentoForm,
    modified_by: str,
) -> FleteDescuento:
    obj = FleteDescuento(
        flete_id=flete_id,
        concepto_id=data.concepto_id,
        detalle=data.detalle,
        habilitar_pago_proveedor=data.habilitar_pago_proveedor,
        # INICIO Monto a cobrar al Propietario
        propietario_monto=data.propietario_monto,
        propietario_moneda_id=data.propietario_moneda_id,
        # FIN Monto a cobrar al Propietario
        # INICIO Monto a pagar al Proveedor
        proveedor_monto=data.proveedor_monto,
        proveedor_moneda_id=data.proveedor_moneda_id,
        proveedor_id=data.proveedor_id,
        # FIN Monto a pagar al Proveedor
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_flete_descuento(
    obj: FleteDescuento,
    db: Session,
    data: FleteDescuentoForm,
    modified_by: str,
) -> FleteDescuento:
    obj.concepto_id = data.concepto_id
    obj.detalle = data.detalle
    obj.habilitar_pago_proveedor = data.habilitar_pago_proveedor
    # INICIO Monto a cobrar al Propietario
    obj.propietario_monto = data.propietario_monto
    obj.propietario_moneda_id = data.propietario_moneda_id
    # FIN Monto a cobrar al Propietario
    # INICIO Monto a pagar al Proveedor
    obj.proveedor_monto = data.proveedor_monto
    obj.proveedor_moneda_id = data.proveedor_moneda_id
    obj.proveedor_id = data.proveedor_id
    # FIN Monto a pagar al Proveedor
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_flete_descuento(db: Session, id: int, modified_by: str):
    obj = db.query(FleteDescuento).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()
