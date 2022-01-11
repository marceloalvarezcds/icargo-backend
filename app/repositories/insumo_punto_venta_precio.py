from typing import Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore

from app.enums import EstadoEnum
from app.models import InsumoPuntoVenta, InsumoPuntoVentaPrecio


def get_last_insumo_punto_venta_precio(
    db: Session,
    insumo_id: int,
    punto_venta_id: int,
    gestor_carga_id: int,
) -> Optional[InsumoPuntoVentaPrecio]:
    return (
        db.query(InsumoPuntoVentaPrecio)
        .filter(
            and_(
                InsumoPuntoVentaPrecio.estado != EstadoEnum.ELIMINADO.value,
                InsumoPuntoVentaPrecio.insumo_punto_venta.has(
                    and_(
                        InsumoPuntoVenta.insumo_id == insumo_id,
                        InsumoPuntoVenta.punto_venta_id == punto_venta_id,
                        InsumoPuntoVenta.gestor_carga_id == gestor_carga_id,
                    )
                ),
            )
        )
        .order_by(InsumoPuntoVentaPrecio.fecha_inicio.desc())
        .first()
    )
