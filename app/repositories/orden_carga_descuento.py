from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import OrdenCargaDescuento
from app.schemas import OrdenCargaDescuentoForm


def get_orden_carga_descuento_by(
    db: Session,
    concepto_id: int,
    propietario_moneda_id: Optional[int],
    propietario_monto: Optional[Decimal],
    proveedor_moneda_id: Optional[int],
    proveedor_monto: Optional[Decimal],
    orden_carga_id: int,
    flete_id: Optional[int],
) -> Optional[OrdenCargaDescuento]:
    return (
        db.query(OrdenCargaDescuento)
        .filter(
            OrdenCargaDescuento.concepto_id == concepto_id,
            OrdenCargaDescuento.propietario_moneda_id == propietario_moneda_id,
            OrdenCargaDescuento.propietario_monto == propietario_monto,
            OrdenCargaDescuento.proveedor_moneda_id == proveedor_moneda_id,
            OrdenCargaDescuento.proveedor_monto == proveedor_monto,
            OrdenCargaDescuento.orden_carga_id == orden_carga_id,
            OrdenCargaDescuento.flete_id == flete_id,
        )
        .first()
    )


def get_orden_carga_descuento_by_id(
    db: Session,
    id: int,
) -> Optional[OrdenCargaDescuento]:
    return db.query(OrdenCargaDescuento).filter(OrdenCargaDescuento.id == id).first()


def create_orden_carga_descuento(
    db: Session,
    data: OrdenCargaDescuentoForm,
    modified_by: str,
) -> OrdenCargaDescuento:
    obj = OrdenCargaDescuento(
        concepto_id=data.concepto.id,
        detalle=data.detalle,
        habilitar_pago_proveedor=data.habilitar_pago_proveedor,
        anticipado=data.anticipado,
        # INICIO Monto a cobrar al Propietario
        propietario_monto=data.propietario_monto,
        propietario_moneda_id=data.propietario_moneda.id,
        # FIN Monto a cobrar al Propietario
        # INICIO Monto a pagar al Proveedor
        proveedor_monto=data.proveedor_monto,
        proveedor_moneda_id=data.proveedor_moneda.id if data.proveedor_moneda else None,
        proveedor_id=data.proveedor.id if data.proveedor else None,
        # FIN Monto a pagar al Proveedor
        orden_carga_id=data.orden_carga_id,
        flete_id=data.flete_id,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_orden_carga_descuento(
    obj: OrdenCargaDescuento,
    db: Session,
    data: OrdenCargaDescuentoForm,
    modified_by: str,
) -> OrdenCargaDescuento:
    obj.concepto_id = data.concepto.id
    obj.detalle = data.detalle
    obj.habilitar_pago_proveedor = data.habilitar_pago_proveedor
    obj.anticipado = data.anticipado
    # INICIO Monto a cobrar al Propietario
    obj.propietario_monto = data.propietario_monto
    obj.propietario_moneda_id = data.propietario_moneda.id
    # FIN Monto a cobrar al Propietario
    # INICIO Monto a pagar al Proveedor
    obj.proveedor_monto = data.proveedor_monto
    obj.proveedor_moneda_id = (
        data.proveedor_moneda.id if data.proveedor_moneda else None
    )
    obj.proveedor_id = data.proveedor.id if data.proveedor else None
    # FIN Monto a pagar al Proveedor
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_orden_carga_descuento(db: Session, id: int, modified_by: str):
    obj = db.query(OrdenCargaDescuento).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()
