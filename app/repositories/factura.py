from datetime import datetime
from typing import List, Optional
from sqlalchemy import null
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore
from app.enums import EstadoEnum
from app.models import Factura
from app.schemas import FacturaForm


def get_factura_list_by_liquidacion_id(
    db: Session, liquidacion_id: int
) -> List[Factura]:
    return (
        db.query(Factura)
        .filter(
            and_(
                Factura.estado != EstadoEnum.ELIMINADO.value,
                Factura.liquidacion_id == liquidacion_id,
            )
        )
        .order_by(Factura.modified_at, Factura.numero_factura)
        .all()
    )


def get_factura_by(
    db: Session, liquidacion_id: int, numero_factura: str, moneda_id: int, iva_id: int
) -> Optional[Factura]:
    return (
        db.query(Factura)
        .filter(
            and_(
                Factura.estado != EstadoEnum.ELIMINADO.value,
                Factura.liquidacion_id == liquidacion_id,
                Factura.numero_factura == numero_factura,
                Factura.moneda_id == moneda_id,
                Factura.iva_id == iva_id,
                Factura.numero_factura != null(),
            )
        )
        .first()
    )


def get_factura_by_id(db: Session, id: int) -> Optional[Factura]:
    return db.query(Factura).get(id)


def create_factura(
    db: Session,
    data: FacturaForm,
    foto_url: Optional[str],
    modified_by: str
) -> Factura:
    obj = Factura(
        liquidacion_id=data.liquidacion_id,
        moneda_id=data.moneda_id,
        numero_factura=data.numero_factura,
        monto=data.monto,
        iva_id=data.iva_id,
        fecha_vencimiento=data.fecha_vencimiento,
        foto=foto_url,
        created_by=modified_by,
        modified_by=modified_by,
        timbrado=data.timbrado,
        ruc=data.ruc,
        fecha_factura=data.fecha_factura,
        iva=data.iva,
        tipo_retencion=data.tipo_retencion,
        retencion=data.retencion,
        contribuyente=data.contribuyente,
        iva_incluido=data.iva_incluido,
        sentido_mov_iva=data.sentido_mov_iva,
        sentido_mov_retencion=data.sentido_mov_retencion,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_factura(
    obj: Factura,
    db: Session,
    data: FacturaForm,
    foto_url: Optional[str],
    modified_by: str,
) -> Factura:
    obj.liquidacion_id = data.liquidacion_id
    obj.moneda_id = data.moneda_id
    obj.numero_factura = data.numero_factura
    obj.monto = data.monto
    obj.iva_id = data.iva_id
    obj.fecha_vencimiento = data.fecha_vencimiento
    obj.timbrado=data.timbrado
    obj.ruc=data.ruc
    obj.fecha_factura=data.fecha_factura,
    obj.iva=data.iva
    obj.tipo_retencion=data.tipo_retencion
    obj.retencion=data.retencion,
    obj.contribuyente=data.contribuyente
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    obj.iva_incluido=data.iva_incluido
    obj.sentido_mov_iva = data.sentido_mov_iva
    obj.sentido_mov_retencion = data.sentido_mov_retencion,

    if foto_url:
        obj.foto = foto_url

    db.commit()
    db.refresh(obj)
    return obj


def change_factura_status(
    obj: Factura,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> Factura:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_factura(
    obj: Factura,
    db: Session,
    modified_by: str,
) -> Factura:
    return change_factura_status(obj, db, EstadoEnum.ELIMINADO, modified_by)


def get_all_contribuyente(db: Session, gestor_carga_id: int) -> List[Factura]:
    subquery= (
        db.query(Factura)
        .distinct(Factura.ruc)
    ).subquery('sq')

    return db.query(subquery).order_by(subquery.c.id.desc()).all()

