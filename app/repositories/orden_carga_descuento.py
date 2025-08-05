from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import OrdenCargaDescuento
from app.models.flete_descuento import FleteDescuento
from app.models.orden_carga import OrdenCarga
from app.schemas import OrdenCargaDescuentoForm


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
        concepto_id=data.concepto_id,
        detalle=data.detalle,
        habilitar_pago_proveedor=data.habilitar_pago_proveedor,
        anticipado=data.anticipado,
        # INICIO Monto a cobrar al Propietario
        propietario_monto=data.propietario_monto,
        propietario_monto_ml= data.propietario_monto_ml,
        propietario_moneda_id=data.propietario_moneda_id,
        # FIN Monto a cobrar al Propietario
        # INICIO Monto a pagar al Proveedor
        proveedor_monto=data.proveedor_monto,
        proveedor_monto_ml= data.proveedor_monto_ml,
        proveedor_moneda_id=data.proveedor_moneda_id,
        proveedor_id=data.proveedor_id,
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
    obj.concepto_id = data.concepto_id
    obj.detalle = data.detalle
    obj.habilitar_pago_proveedor = data.habilitar_pago_proveedor
    obj.anticipado = data.anticipado
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


def delete_orden_carga_descuento(db: Session, id: int, modified_by: str):
    obj: OrdenCargaDescuento = db.query(OrdenCargaDescuento).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()



def update_or_create_orden_carga_descuento_by_flete(
    db: Session,
    orden_carga: OrdenCarga,
    descuento_flete: FleteDescuento,
    modified_by: str,
):
    descuento_oc = db.query(OrdenCargaDescuento).filter(
        OrdenCargaDescuento.orden_carga_id == orden_carga.id,
        OrdenCargaDescuento.concepto_id == descuento_flete.concepto_id,
    ).first()

    if descuento_oc:
        descuento_oc.detalle = descuento_flete.detalle
        descuento_oc.habilitar_pago_proveedor = descuento_flete.habilitar_pago_proveedor
        descuento_oc.anticipado = descuento_flete.anticipado
        descuento_oc.propietario_monto = descuento_flete.propietario_monto
        descuento_oc.propietario_monto_ml = descuento_flete.propietario_monto_ml
        descuento_oc.propietario_moneda_id = descuento_flete.propietario_moneda_id
        descuento_oc.proveedor_monto = descuento_flete.proveedor_monto
        descuento_oc.proveedor_monto_ml = descuento_flete.proveedor_monto_ml
        descuento_oc.proveedor_moneda_id = descuento_flete.proveedor_moneda_id
        descuento_oc.proveedor_id = descuento_flete.proveedor_id
        descuento_oc.flete_id = descuento_flete.flete_id
        descuento_oc.modified_by = modified_by
        db.add(descuento_oc)
    else:
        nuevo = OrdenCargaDescuento(
            concepto_id=descuento_flete.concepto_id,
            detalle=descuento_flete.detalle,
            habilitar_pago_proveedor=descuento_flete.habilitar_pago_proveedor,
            anticipado=descuento_flete.anticipado,
            propietario_monto=descuento_flete.propietario_monto,
            propietario_monto_ml=descuento_flete.propietario_monto_ml,
            propietario_moneda_id=descuento_flete.propietario_moneda_id,
            proveedor_monto=descuento_flete.proveedor_monto,
            proveedor_monto_ml=descuento_flete.proveedor_monto_ml,
            proveedor_moneda_id=descuento_flete.proveedor_moneda_id,
            proveedor_id=descuento_flete.proveedor_id,
            orden_carga_id=orden_carga.id,
            flete_id=descuento_flete.flete_id,
            created_by=modified_by,
            modified_by=modified_by,
        )
        db.add(nuevo)

    db.commit()
