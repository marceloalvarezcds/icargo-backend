from sqlalchemy.orm import Session  # type: ignore

from app.models import FleteDescuento, OrdenCarga, OrdenCargaDescuento


def create_orden_carga_descuento_by_flete(
    db: Session,
    orden_carga: OrdenCarga,
    data: FleteDescuento,
    modified_by: str,
) -> OrdenCargaDescuento:
    obj = OrdenCargaDescuento(
        concepto_id=data.concepto_id,
        detalle=data.detalle,
        habilitar_pago_proveedor=data.habilitar_pago_proveedor,
        anticipado=data.anticipado,
        # INICIO Monto a cobrar al Propietario
        propietario_monto=data.propietario_monto,
        propietario_moneda_id=data.propietario_moneda_id,
        # FIN Monto a cobrar al Propietario
        # INICIO Monto a pagar al Proveedor
        proveedor_monto=data.proveedor_monto,
        proveedor_moneda_id=data.proveedor_moneda_id,
        proveedor_id=data.proveedor_id,
        # FIN Monto a pagar al Proveedor
        orden_carga_id=orden_carga.id,
        flete_id=data.flete_id,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
