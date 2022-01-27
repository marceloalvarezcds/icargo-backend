from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import InsumoPuntoVentaPrecio
from app.repositories import (
    get_insumo_punto_venta_by_insumo_id_and_moneda_id_and_punto_venta_id,
    get_last_insumo_punto_venta_precio_by_insumo_punto_venta_id,
)


def get_insumo_punto_venta_precio_by_insumo_id_and_moneda_id_and_punto_venta_id(
    db: Session,
    insumo_id: int,
    moneda_id: int,
    punto_venta_id: int,
    gestor_carga_id: int,
) -> Optional[InsumoPuntoVentaPrecio]:
    insumo_punto_venta = (
        get_insumo_punto_venta_by_insumo_id_and_moneda_id_and_punto_venta_id(
            db,
            insumo_id,
            moneda_id,
            punto_venta_id,
            gestor_carga_id,
        )
    )
    if insumo_punto_venta:
        return get_last_insumo_punto_venta_precio_by_insumo_punto_venta_id(
            db, insumo_punto_venta_id=insumo_punto_venta.id
        )
    return None
