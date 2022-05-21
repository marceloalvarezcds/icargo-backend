from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore
from sqlalchemy.sql.expression import null  # type: ignore

from app.enums import EstadoEnum
from app.models import InsumoPuntoVenta, InsumoPuntoVentaPrecio
from app.schemas import InsumoPuntoVentaPrecioForm


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
