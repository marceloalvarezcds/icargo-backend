from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import OrdenCargaComplemento
from app.models.flete_complemento import FleteComplemento
from app.models.orden_carga import OrdenCarga
from app.schemas import OrdenCargaComplementoForm


def get_orden_carga_complemento_by_id(
    db: Session,
    id: int,
) -> Optional[OrdenCargaComplemento]:
    return (
        db.query(OrdenCargaComplemento).filter(OrdenCargaComplemento.id == id).first()
    )


def create_orden_carga_complemento(
    db: Session,
    data: OrdenCargaComplementoForm,
    modified_by: str,

) -> OrdenCargaComplemento:
    obj = OrdenCargaComplemento(
        concepto_id=data.concepto.id,
        detalle=data.detalle,
        habilitar_cobro_remitente=data.habilitar_cobro_remitente,
        anticipado=data.anticipado,
        # INICIO Monto a pagar al Propietario
        propietario_monto=data.propietario_monto,
        propietario_monto_ml= data.propietario_monto_ml,
        propietario_moneda_id=data.propietario_moneda.id,
        # FIN Monto a pagar al Propietario
        # INICIO Monto a cobrar al Remitente
        remitente_monto=data.remitente_monto,
        remitente_moneda_id=data.remitente_moneda.id if data.remitente_moneda else None,
        remitente_monto_ml= data.remitente_monto_ml,
        # FIN Monto a cobrar al Remitente
        orden_carga_id=data.orden_carga_id,
        flete_id=data.flete_id,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_orden_carga_complemento(
    obj: OrdenCargaComplemento,
    db: Session,
    data: OrdenCargaComplementoForm,
    modified_by: str,
) -> OrdenCargaComplemento:
    obj.concepto_id = data.concepto.id
    obj.detalle = data.detalle
    obj.habilitar_cobro_remitente = data.habilitar_cobro_remitente
    obj.anticipado = data.anticipado
    # INICIO Monto a pagar al Propietario
    obj.propietario_monto = data.propietario_monto
    obj.propietario_monto_ml = data.propietario_monto_ml
    obj.propietario_moneda_id = data.propietario_moneda.id
    # FIN Monto a pagar al Propietario
    # INICIO Monto a cobrar al Remitente
    obj.remitente_monto = data.remitente_monto
    obj.remitente_monto_ml = data.remitente_monto_ml
    obj.remitente_moneda_id = (
        data.remitente_moneda.id if data.remitente_moneda else None
    )
    # FIN Monto a cobrar al Remitente
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_orden_carga_complemento(db: Session, id: int, modified_by: str):
    obj = db.query(OrdenCargaComplemento).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()



def update_or_create_orden_carga_complemento_by_flete(
    db: Session,
    orden_carga: OrdenCarga,
    complemento_flete: FleteComplemento,
    modified_by: str,
):
    # Buscar si ya existe complemento con mismo concepto en la OC
    complemento_oc = db.query(OrdenCargaComplemento).filter(
        OrdenCargaComplemento.orden_carga_id == orden_carga.id,
        OrdenCargaComplemento.concepto_id == complemento_flete.concepto_id,
    ).first()

    if complemento_oc:
        # Actualizar campos
        complemento_oc.detalle = complemento_flete.detalle
        complemento_oc.habilitar_cobro_remitente = complemento_flete.habilitar_cobro_remitente
        complemento_oc.anticipado = complemento_flete.anticipado
        complemento_oc.propietario_monto = complemento_flete.propietario_monto
        complemento_oc.propietario_monto_ml = complemento_flete.propietario_monto_ml
        complemento_oc.propietario_moneda_id = complemento_flete.propietario_moneda_id
        complemento_oc.remitente_monto = complemento_flete.remitente_monto
        complemento_oc.remitente_monto_ml = complemento_flete.remitente_monto_ml
        complemento_oc.remitente_moneda_id = complemento_flete.remitente_moneda_id
        complemento_oc.flete_id = complemento_flete.flete_id
        complemento_oc.modified_by = modified_by
        db.add(complemento_oc)
    else:
        # Crear nuevo complemento
        nuevo = OrdenCargaComplemento(
            concepto_id=complemento_flete.concepto_id,
            detalle=complemento_flete.detalle,
            habilitar_cobro_remitente=complemento_flete.habilitar_cobro_remitente,
            anticipado=complemento_flete.anticipado,
            propietario_monto=complemento_flete.propietario_monto,
            propietario_monto_ml=complemento_flete.propietario_monto_ml,
            propietario_moneda_id=complemento_flete.propietario_moneda_id,
            remitente_monto=complemento_flete.remitente_monto,
            remitente_monto_ml=complemento_flete.remitente_monto_ml,
            remitente_moneda_id=complemento_flete.remitente_moneda_id,
            orden_carga_id=orden_carga.id,
            flete_id=complemento_flete.flete_id,
            created_by=modified_by,
            modified_by=modified_by,
        )
        db.add(nuevo)

    db.commit()
