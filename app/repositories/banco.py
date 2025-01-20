from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore

from app.enums import EstadoEnum
from app.models import Banco
from app.schemas import BancoForm


def get_banco_list(db: Session) -> List[Banco]:
    return (
        db.query(Banco)
        .filter(Banco.estado != EstadoEnum.ELIMINADO.value)
        .order_by(Banco.id.desc())
        .all()
    )


def get_banco_list_by_gestor_carga_id(db: Session, gestor_carga_id: int) -> List[Banco]:
    return (
        db.query(Banco)
        .filter(
            and_(
                Banco.gestor_carga_id == gestor_carga_id,
                Banco.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(Banco.id.desc())
        .all()
    )


def get_banco_by(
    db: Session, numero_cuenta: str, gestor_carga_id: int
) -> Optional[Banco]:
    return (
        db.query(Banco)
        .filter(
            and_(
                Banco.numero_cuenta == numero_cuenta,
                Banco.gestor_carga_id == gestor_carga_id,
            )
        )
        .first()
    )


def get_banco_by_id(db: Session, id: int) -> Optional[Banco]:
    return db.query(Banco).get(id)


def create_banco(
    db: Session,
    data: BancoForm,
    gestor_carga_id: int,
    modified_by: str,
) -> Banco:
    obj = Banco(
        numero_cuenta=data.numero_cuenta,
        titular=data.titular,
        nombre=data.nombre,
        moneda_id=data.moneda_id,
        gestor_carga_id=gestor_carga_id,
        estado=EstadoEnum.ACTIVO.value,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_banco(
    obj: Banco,
    db: Session,
    data: BancoForm,
    gestor_carga_id: int,
    modified_by: str,
) -> Banco:
    obj.numero_cuenta = data.numero_cuenta
    obj.titular = data.titular
    obj.nombre = data.nombre
    obj.moneda_id = data.moneda_id
    obj.gestor_carga_id = gestor_carga_id
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def change_banco_saldos(
    obj: Banco,
    db: Session,
    saldo_confirmado: Decimal,
    saldo_provisional: Decimal,
    modified_by: str,
) -> Banco:
    obj.saldo_confirmado = saldo_confirmado
    obj.saldo_provisional = saldo_provisional
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def change_banco_status(
    obj: Banco,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> Banco:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_banco(
    obj: Banco,
    db: Session,
    modified_by: str,
) -> Banco:
    return change_banco_status(obj, db, EstadoEnum.ELIMINADO, modified_by)
