from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import OrdenCargaAnticipoSaldo
from app.schemas import OrdenCargaAnticipoSaldoForm


def get_orden_carga_anticipo_saldo_by(
    db: Session,
    flete_anticipo_id: int,
    orden_carga_id: int,
) -> Optional[OrdenCargaAnticipoSaldo]:
    return (
        db.query(OrdenCargaAnticipoSaldo)
        .filter(
            OrdenCargaAnticipoSaldo.flete_anticipo_id == flete_anticipo_id,
            OrdenCargaAnticipoSaldo.orden_carga_id == orden_carga_id,
        )
        .first()
    )


def get_orden_carga_anticipo_saldo_by_id(
    db: Session,
    id: int,
) -> Optional[OrdenCargaAnticipoSaldo]:
    return (
        db.query(OrdenCargaAnticipoSaldo)
        .filter(OrdenCargaAnticipoSaldo.id == id)
        .first()
    )


def create_orden_carga_anticipo_saldo(
    db: Session,
    data: OrdenCargaAnticipoSaldoForm,
    modified_by: str,
) -> OrdenCargaAnticipoSaldo:
    obj = OrdenCargaAnticipoSaldo(
        flete_anticipo_id=data.flete_anticipo_id,
        orden_carga_id=data.orden_carga_id,
        total_anticipo=data.total_anticipo,
        total_complemento=data.total_complemento,
        total_retirado=data.total_retirado,
        saldo=data.saldo,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_orden_carga_anticipo_saldo(
    obj: OrdenCargaAnticipoSaldo,
    db: Session,
    data: OrdenCargaAnticipoSaldoForm,
    modified_by: str,
) -> OrdenCargaAnticipoSaldo:
    obj.flete_anticipo_id = data.flete_anticipo_id
    obj.orden_carga_id = data.orden_carga_id
    obj.total_anticipo = data.total_anticipo
    obj.total_complemento = data.total_complemento
    obj.total_retirado = data.total_retirado
    obj.saldo = data.saldo
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_orden_carga_anticipo_saldo(db: Session, id: int, modified_by: str):
    obj = db.query(OrdenCargaAnticipoSaldo).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()
