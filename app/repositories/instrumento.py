from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum, OperacionEstadoEnum
from app.models import Instrumento
from app.schemas import InstrumentoSaldoForm


def get_instrumento_list(db: Session) -> List[Instrumento]:
    return (
        db.query(Instrumento)
        .filter(Instrumento.estado != EstadoEnum.ELIMINADO.value)
        .order_by(Instrumento.contraparte, Instrumento.liquidacion_id)
        .all()
    )


def get_instrumento_by_id(db: Session, id: int) -> Optional[Instrumento]:
    return db.query(Instrumento).get(id)


def create_instrumento(
    db: Session,
    data: InstrumentoSaldoForm,
    modified_by: str,
) -> Instrumento:
    obj = Instrumento(
        via_id=data.via_id,
        caja_id=data.caja_id,
        banco_id=data.banco_id,
        liquidacion_id=data.liquidacion_id,
        fecha_instrumento=data.fecha_instrumento,
        numero_referencia=data.numero_referencia,
        comentario=data.comentario,
        tipo_instrumento_id=data.tipo_instrumento_id,
        operacion_estado=data.operacion_estado.value,
        # Saldos
        credito=data.credito,
        debito=data.debito,
        saldo_confirmado=data.saldo_confirmado,
        # Datos mostrados solo para Banco
        provision=data.provision,
        saldo_provisional=data.saldo_provisional,
        # Solo para cheque
        cheque_es_diferido=data.cheque_es_diferido,
        cheque_fecha_vencimiento=data.cheque_fecha_vencimiento,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_instrumento(
    obj: Instrumento,
    db: Session,
    data: InstrumentoSaldoForm,
    modified_by: str,
) -> Instrumento:
    obj.via_id = data.via_id
    obj.caja_id = data.caja_id
    obj.banco_id = data.banco_id
    obj.liquidacion_id = data.liquidacion_id
    obj.fecha_instrumento = data.fecha_instrumento
    obj.numero_referencia = data.numero_referencia
    obj.comentario = data.comentario
    obj.tipo_instrumento_id = data.tipo_instrumento_id
    # Saldos
    obj.credito = data.credito
    obj.debito = data.debito
    obj.saldo_confirmado = data.saldo_confirmado
    # Datos mostrados solo para Banco
    obj.provision = data.provision
    obj.saldo_provisional = data.saldo_provisional
    # Solo para cheque
    obj.cheque_es_diferido = data.cheque_es_diferido
    obj.cheque_fecha_vencimiento = data.cheque_fecha_vencimiento
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def change_instrumento_operacion_estado(
    obj: Instrumento,
    db: Session,
    status: OperacionEstadoEnum,
    modified_by: str,
) -> Instrumento:
    obj.operacion_estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def change_instrumento_status(
    obj: Instrumento,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> Instrumento:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_instrumento(
    obj: Instrumento,
    db: Session,
    modified_by: str,
) -> Instrumento:
    return change_instrumento_status(obj, db, EstadoEnum.ELIMINADO, modified_by)
