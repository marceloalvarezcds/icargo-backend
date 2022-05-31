from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore
from sqlalchemy.sql.expression import null  # type: ignore

from app.enums import EstadoEnum
from app.models import Insumo, InsumoPuntoVenta, InsumoPuntoVentaPrecio
from app.schemas import InsumoPuntoVentaPrecioForm


def get_insumo_punto_venta_by_id(db: Session, id: int) -> Optional[InsumoPuntoVenta]:
    return db.query(InsumoPuntoVenta).get(id)


def get_insumo_punto_venta_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: int
) -> List[InsumoPuntoVenta]:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        db.query(InsumoPuntoVenta)
        .filter(
            and_(
                InsumoPuntoVenta.estado != EstadoEnum.ELIMINADO.value,
                InsumoPuntoVenta.gestor_carga_id == gestor_carga_id,
                InsumoPuntoVenta.precios.any(
                    and_(
                        InsumoPuntoVentaPrecio.estado != EstadoEnum.ELIMINADO.value,
                        InsumoPuntoVentaPrecio.fecha_inicio <= now,
                        or_(
                            InsumoPuntoVentaPrecio.fecha_fin == null(),
                            InsumoPuntoVentaPrecio.fecha_fin >= now,
                        ),
                    ),
                ),
            )
        )
        .order_by(InsumoPuntoVenta.created_at)
        .all()
    )


def get_insumo_punto_venta_list_by_tipo_insumo_id(
    db: Session, tipo_insumo_id: int, gestor_carga_id: int
) -> List[InsumoPuntoVenta]:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        db.query(InsumoPuntoVenta)
        .filter(
            and_(
                InsumoPuntoVenta.estado != EstadoEnum.ELIMINADO.value,
                InsumoPuntoVenta.insumo.has(Insumo.tipo_id == tipo_insumo_id),
                InsumoPuntoVenta.gestor_carga_id == gestor_carga_id,
                InsumoPuntoVenta.precios.any(
                    and_(
                        InsumoPuntoVentaPrecio.estado != EstadoEnum.ELIMINADO.value,
                        InsumoPuntoVentaPrecio.fecha_inicio <= now,
                        or_(
                            InsumoPuntoVentaPrecio.fecha_fin == null(),
                            InsumoPuntoVentaPrecio.fecha_fin >= now,
                        ),
                    ),
                ),
            )
        )
        .order_by(InsumoPuntoVenta.created_at)
        .all()
    )


def get_insumo_punto_venta_list_by_insumo_id(
    db: Session, insumo_id: int, gestor_carga_id: int
) -> List[InsumoPuntoVenta]:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        db.query(InsumoPuntoVenta)
        .filter(
            and_(
                InsumoPuntoVenta.estado != EstadoEnum.ELIMINADO.value,
                InsumoPuntoVenta.insumo_id == insumo_id,
                InsumoPuntoVenta.gestor_carga_id == gestor_carga_id,
                InsumoPuntoVenta.precios.any(
                    and_(
                        InsumoPuntoVentaPrecio.estado != EstadoEnum.ELIMINADO.value,
                        InsumoPuntoVentaPrecio.fecha_inicio <= now,
                        or_(
                            InsumoPuntoVentaPrecio.fecha_fin == null(),
                            InsumoPuntoVentaPrecio.fecha_fin >= now,
                        ),
                    ),
                ),
            )
        )
        .order_by(InsumoPuntoVenta.created_at)
        .all()
    )


def get_insumo_punto_venta_list_by_insumo_id_and_punto_venta_id(
    db: Session, insumo_id: int, punto_venta_id: int, gestor_carga_id: int
) -> List[InsumoPuntoVenta]:
    return (
        db.query(InsumoPuntoVenta)
        .filter(
            and_(
                InsumoPuntoVenta.estado != EstadoEnum.ELIMINADO.value,
                InsumoPuntoVenta.insumo_id == insumo_id,
                InsumoPuntoVenta.punto_venta_id == punto_venta_id,
                InsumoPuntoVenta.gestor_carga_id == gestor_carga_id,
            )
        )
        .order_by(InsumoPuntoVenta.created_at)
        .all()
    )


def get_insumo_punto_venta_by_insumo_id_and_moneda_id_and_punto_venta_id(
    db: Session,
    insumo_id: int,
    moneda_id: int,
    punto_venta_id: int,
    gestor_carga_id: int,
) -> Optional[InsumoPuntoVenta]:
    return (
        db.query(InsumoPuntoVenta)
        .filter(
            and_(
                InsumoPuntoVenta.estado != EstadoEnum.ELIMINADO.value,
                InsumoPuntoVenta.insumo_id == insumo_id,
                InsumoPuntoVenta.moneda_id == moneda_id,
                InsumoPuntoVenta.punto_venta_id == punto_venta_id,
                InsumoPuntoVenta.gestor_carga_id == gestor_carga_id,
            ),
        )
        .first()
    )


def create_insumo_punto_venta(
    db: Session,
    data: InsumoPuntoVentaPrecioForm,
    gestor_carga_id: int,
    modified_by: str,
) -> InsumoPuntoVenta:
    obj = InsumoPuntoVenta(
        insumo_id=data.insumo_id,
        punto_venta_id=data.punto_venta_id,
        gestor_carga_id=gestor_carga_id,
        moneda_id=data.moneda_id,
        estado=EstadoEnum.ACTIVO.value,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
