from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import OrdenCargaComplemento
from app.schemas import OrdenCargaComplementoForm


def get_orden_carga_complemento_by(
    db: Session,
    concepto_id: int,
    propietario_moneda_id: Optional[int],
    propietario_monto: Optional[Decimal],
    remitente_moneda_id: Optional[int],
    remitente_monto: Optional[Decimal],
    orden_carga_id: int,
) -> Optional[OrdenCargaComplemento]:
    return (
        db.query(OrdenCargaComplemento)
        .filter(
            OrdenCargaComplemento.concepto_id == concepto_id,
            OrdenCargaComplemento.propietario_moneda_id == propietario_moneda_id,
            OrdenCargaComplemento.propietario_monto == propietario_monto,
            OrdenCargaComplemento.remitente_moneda_id == remitente_moneda_id,
            OrdenCargaComplemento.remitente_monto == remitente_monto,
            OrdenCargaComplemento.orden_carga_id == orden_carga_id,
        )
        .first()
    )


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
    obj.concepto_id = data.concepto_id
    obj.detalle = data.detalle
    obj.habilitar_cobro_remitente = data.habilitar_cobro_remitente
    obj.anticipado = data.anticipado
    # INICIO Monto a pagar al Propietario
    obj.propietario_monto = data.propietario_monto
    obj.propietario_moneda_id = data.propietario_moneda_id
    # FIN Monto a pagar al Propietario
    # INICIO Monto a cobrar al Remitente
    obj.remitente_monto = data.remitente_monto
    obj.remitente_moneda_id = data.remitente_moneda_id
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
