from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Query, Session  # type: ignore
from sqlalchemy.sql import func  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore
from sqlalchemy.sql.expression import null  # type: ignore

from app.enums import EstadoEnum
from app.models import (
    FleteAnticipo,
    Insumo,
    InsumoPuntoVenta,
    InsumoPuntoVentaPrecio,
    PuntoVenta,
)
from app.schemas import InsumoPuntoVentaPrecioForm

def get_insumo_punto_venta_precio_list(
    db: Session, gestor_carga_id: Optional[int]
) -> List[InsumoPuntoVentaPrecio]:
    return (
        db.query(InsumoPuntoVentaPrecio)
        .filter(
            and_(
                InsumoPuntoVentaPrecio.gestor_carga_id == gestor_carga_id,
                InsumoPuntoVentaPrecio.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .all()
    )

# def get_insumo_punto_venta_precio_list(db: Session) -> List[InsumoPuntoVentaPrecio]:
#     return db.query(InsumoPuntoVentaPrecio).all()


def get_last_insumo_punto_venta_precio_by_insumo_punto_venta_id(
    db: Session,
    insumo_punto_venta_id: int,
) -> Optional[InsumoPuntoVentaPrecio]:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        db.query(InsumoPuntoVentaPrecio)
        .filter(
            and_(
                InsumoPuntoVentaPrecio.estado != EstadoEnum.ELIMINADO.value,
                InsumoPuntoVentaPrecio.insumo_punto_venta_id == insumo_punto_venta_id,
                InsumoPuntoVentaPrecio.fecha_inicio <= now,
                or_(
                    InsumoPuntoVentaPrecio.fecha_fin == null(),
                    InsumoPuntoVentaPrecio.fecha_fin >= now,
                ),
            ),
        )
        .order_by(
            InsumoPuntoVentaPrecio.fecha_inicio.desc(),
            InsumoPuntoVentaPrecio.fecha_fin.desc(),
        )
        .first()
    )


def get_insumo_punto_venta_precio_max_fecha_query(
    db: Session, flete_id: int, gestor_carga_id: Optional[int]
) -> Query:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        db.query(
            InsumoPuntoVenta.punto_venta_id,
            InsumoPuntoVenta.insumo_id,
            func.max(InsumoPuntoVentaPrecio.fecha_inicio).label("max_fecha_inicio"),
        )
        .select_from(InsumoPuntoVentaPrecio)
        .join(InsumoPuntoVentaPrecio.insumo_punto_venta)
        .join(InsumoPuntoVenta.insumo)
        .join(InsumoPuntoVenta.punto_venta)
        .join(FleteAnticipo, Insumo.tipo_id == FleteAnticipo.tipo_insumo_id)
        .filter(
            and_(
                FleteAnticipo.flete_id == flete_id,
                InsumoPuntoVenta.gestor_carga_id == gestor_carga_id,
                InsumoPuntoVenta.estado != EstadoEnum.ELIMINADO.value,
                InsumoPuntoVentaPrecio.estado != EstadoEnum.ELIMINADO.value,
                PuntoVenta.estado != EstadoEnum.ELIMINADO.value,
                or_(
                    InsumoPuntoVentaPrecio.fecha_fin >= now,
                    InsumoPuntoVentaPrecio.fecha_fin == null(),
                ),
            )
        )
        .group_by(InsumoPuntoVenta.punto_venta_id, InsumoPuntoVenta.insumo_id)
    ).subquery()


def get_insumo_punto_venta_precio_list_by_gestor_carga_id(
    db: Session, flete_id: int, gestor_carga_id: Optional[int]
) -> List[InsumoPuntoVentaPrecio]:
    sub_query = get_insumo_punto_venta_precio_max_fecha_query(
        db, flete_id, gestor_carga_id
    )
    return (
        db.query(InsumoPuntoVentaPrecio)
        .join(InsumoPuntoVentaPrecio.insumo_punto_venta)
        .join(
            sub_query,
            and_(
                sub_query.c.punto_venta_id == InsumoPuntoVenta.punto_venta_id,
                sub_query.c.insumo_id == InsumoPuntoVenta.insumo_id,
                sub_query.c.max_fecha_inicio == InsumoPuntoVentaPrecio.fecha_inicio,
            ),
        )
        .order_by(
            InsumoPuntoVentaPrecio.fecha_inicio,
            InsumoPuntoVentaPrecio.fecha_fin,
            InsumoPuntoVentaPrecio.modified_by,
        )
        .all()
    )


def create_insumo_punto_venta_precio_by_insumo_punto_venta(
    db: Session,
    obj: InsumoPuntoVenta,
    data: InsumoPuntoVentaPrecioForm,
    modified_by: str,
) -> InsumoPuntoVentaPrecio:
    obj = InsumoPuntoVentaPrecio(
        insumo_punto_venta_id=obj.id,
        precio=data.precio,
        fecha_inicio=data.fecha_inicio,
        fecha_fin=data.fecha_fin,
        estado=EstadoEnum.ACTIVO.value,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
