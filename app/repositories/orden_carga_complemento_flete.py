from sqlalchemy.orm import Session  # type: ignore

from app.models import FleteComplemento, OrdenCarga, OrdenCargaComplemento


def create_orden_carga_complemento_by_flete(
    db: Session,
    orden_carga: OrdenCarga,
    data: FleteComplemento,
    modified_by: str,
) -> OrdenCargaComplemento:
    obj = OrdenCargaComplemento(
        concepto_id=data.concepto_id,
        detalle=data.detalle,
        habilitar_cobro_remitente=data.habilitar_cobro_remitente,
        anticipado=data.anticipado,
        # INICIO Monto a pagar al Propietario
        propietario_monto=data.propietario_monto,
        propietario_moneda_id=data.propietario_moneda_id,
        # FIN Monto a pagar al Propietario
        # INICIO Monto a cobrar al Remitente
        remitente_monto=data.remitente_monto,
        remitente_moneda_id=data.remitente_moneda_id,
        # FIN Monto a cobrar al Remitente
        orden_carga_id=orden_carga.id,
        flete_id=data.flete_id,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
