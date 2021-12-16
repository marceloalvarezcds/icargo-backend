from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import FleteComplemento
from app.schemas import FleteComplementoForm


def get_flete_complemento_by(
    db: Session,
    concepto_id: int,
    propietario_moneda_id: int,
    propietario_monto: int,
    remitente_moneda_id: int,
    remitente_monto: int,
    flete_id: int,
) -> Optional[FleteComplemento]:
    return (
        db.query(FleteComplemento)
        .filter(
            FleteComplemento.concepto_id == concepto_id,
            FleteComplemento.propietario_moneda_id == propietario_moneda_id,
            FleteComplemento.propietario_monto == propietario_monto,
            FleteComplemento.remitente_moneda_id == remitente_moneda_id,
            FleteComplemento.remitente_monto == remitente_monto,
            FleteComplemento.flete_id == flete_id,
        )
        .first()
    )


def get_flete_complemento_by_id(
    db: Session,
    id: int,
) -> Optional[FleteComplemento]:
    return db.query(FleteComplemento).filter(FleteComplemento.id == id).first()


def create_flete_complemento(
    db: Session,
    flete_id: int,
    data: FleteComplementoForm,
    modified_by: str,
) -> FleteComplemento:
    obj = FleteComplemento(
        flete_id=flete_id,
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
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_flete_complemento(
    obj: FleteComplemento,
    db: Session,
    data: FleteComplementoForm,
    modified_by: str,
) -> FleteComplemento:
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


def delete_flete_complemento(db: Session, id: int, modified_by: str):
    obj = db.query(FleteComplemento).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()
