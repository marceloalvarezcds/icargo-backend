from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import OrdenCargaComplemento
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
    remitente_monto_ml: Optional[float] = None,
    propietario_monto_ml: Optional[float] = None,
) -> OrdenCargaComplemento:
    obj = OrdenCargaComplemento(
        concepto_id=data.concepto.id,
        detalle=data.detalle,
        habilitar_cobro_remitente=data.habilitar_cobro_remitente,
        anticipado=data.anticipado,
        # INICIO Monto a pagar al Propietario
        propietario_monto=data.propietario_monto,
        propietario_monto_ml=propietario_monto_ml,
        propietario_moneda_id=data.propietario_moneda.id,
        # FIN Monto a pagar al Propietario
        # INICIO Monto a cobrar al Remitente
        remitente_monto=data.remitente_monto,
        remitente_moneda_id=data.remitente_moneda.id if data.remitente_moneda else None,
        remitente_monto_ml=remitente_monto_ml,
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
    obj.propietario_moneda_id = data.propietario_moneda.id
    # FIN Monto a pagar al Propietario
    # INICIO Monto a cobrar al Remitente
    obj.remitente_monto = data.remitente_monto
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
