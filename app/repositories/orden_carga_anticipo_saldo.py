from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import OrdenCargaAnticipoSaldo
from app.models.flete_anticipo import FleteAnticipo
from app.schemas import OrdenCargaAnticipoSaldoForm


def get_orden_carga_anticipo_saldo_by(
    db: Session,
    flete_anticipo_id: int,
    orden_carga_id: int,
    tipo_anticipo: Optional[str] = None  # Parámetro adicional para filtrar por tipo de anticipo
) -> Optional[OrdenCargaAnticipoSaldo]:
    query = db.query(OrdenCargaAnticipoSaldo).filter(
        OrdenCargaAnticipoSaldo.flete_anticipo_id == flete_anticipo_id,
        OrdenCargaAnticipoSaldo.orden_carga_id == orden_carga_id,
    )
    
    if tipo_anticipo:
        query = query.filter(OrdenCargaAnticipoSaldo.tipo_anticipo == tipo_anticipo)
    
    return query.first()


def get_orden_carga_anticipo_saldo_insumo_by(
    db: Session,
    flete_anticipo_id: int,
    orden_carga_id: int,
) -> Optional[OrdenCargaAnticipoSaldo]:
    return (
        db.query(OrdenCargaAnticipoSaldo)
        .join(FleteAnticipo, FleteAnticipo.id == OrdenCargaAnticipoSaldo.flete_anticipo_id)  # Join entre las tablas
        .filter(
            OrdenCargaAnticipoSaldo.flete_anticipo_id == flete_anticipo_id,
            OrdenCargaAnticipoSaldo.orden_carga_id == orden_carga_id,
            FleteAnticipo.tipo_insumo_id.isnot(None)  # Filtrar solo donde tipo_insumo_id no es NULL
        )
        .all()
    )



def create_flete_anticipo(
    db: Session,
    flete_anticipo_id: int,
    tipo_descripcion: str,
    created_by: str
) -> FleteAnticipo:
    nuevo_flete_anticipo = FleteAnticipo(
        id=flete_anticipo_id,
        tipo_descripcion=tipo_descripcion,
        created_by=created_by,
        created_at=datetime.utcnow()  
    )
    db.add(nuevo_flete_anticipo)
    db.commit()  
    db.refresh(nuevo_flete_anticipo) 
    return nuevo_flete_anticipo


def get_orden_carga_anticipo_saldo_by_id(
    db: Session,
    id: int,
) -> Optional[OrdenCargaAnticipoSaldo]:
    return (
        db.query(OrdenCargaAnticipoSaldo)
        .filter(OrdenCargaAnticipoSaldo.id == id)
        .first()
    )


def get_orden_carga_anticipo_saldo_by_orden_carga_id(db: Session, orden_carga_id: int):
    return db.query(OrdenCargaAnticipoSaldo).filter(
        OrdenCargaAnticipoSaldo.orden_carga_id == orden_carga_id
    ).all()


def get_orden_carga_anticipo_saldo_by_orden_carga_and_tipo_insumo_id(
    db: Session, orden_carga_id: int, tipo_insumo_id: int
) -> Optional[OrdenCargaAnticipoSaldo]:
    return db.query(OrdenCargaAnticipoSaldo).filter(
        OrdenCargaAnticipoSaldo.orden_carga_id == orden_carga_id,
        OrdenCargaAnticipoSaldo.tipo_insumo_id == tipo_insumo_id
    ).first()



def create_orden_carga_anticipo_saldo(
    db: Session,
    data: OrdenCargaAnticipoSaldoForm,
    saldo_actualizado: float,
    modified_by: str,
) -> OrdenCargaAnticipoSaldo:
    obj = OrdenCargaAnticipoSaldo(
        flete_anticipo_id=data.flete_anticipo_id,
        orden_carga_id=data.orden_carga_id,
        orden_carga_anticipo_porcentaje_id=data.orden_carga_anticipo_porcentaje_id,
        total_anticipo=data.total_anticipo,
        total_complemento=data.total_complemento,
        total_retirado=data.total_retirado,  
        saldo=saldo_actualizado,  
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
    obj.orden_carga_anticipo_porcentaje_id = data.orden_carga_anticipo_porcentaje_id
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
