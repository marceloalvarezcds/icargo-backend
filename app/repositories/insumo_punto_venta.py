from typing import List

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore

from app.models import InsumoPuntoVenta


def get_insumo_punto_venta_list_by_insumo_id(
    db: Session, insumo_id: int, gestor_carga_id: int
) -> List[InsumoPuntoVenta]:
    return (
        db.query(InsumoPuntoVenta)
        .filter(
            and_(
                InsumoPuntoVenta.insumo_id == insumo_id,
                InsumoPuntoVenta.gestor_carga_id == gestor_carga_id,
            )
        )
        .order_by(InsumoPuntoVenta.created_at)
        .all()
    )
