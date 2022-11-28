from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import InsumoPuntoVentaPrecio
from app.repositories import (
    create_insumo_punto_venta,
    create_insumo_punto_venta_precio_by_insumo_punto_venta,
    get_insumo_punto_venta_by_insumo_id_and_moneda_id_and_punto_venta_id,
    get_last_insumo_punto_venta_precio_by_insumo_punto_venta_id,
)
from app.schemas import InsumoPuntoVentaPrecioForm
from app.utils.gestor_carga import get_gestor_carga_by_params


def get_insumo_punto_venta_precio_by_insumo_id_and_moneda_id_and_punto_venta_id(
    db: Session,
    insumo_id: int,
    moneda_id: int,
    punto_venta_id: int,
    gestor_carga_id: Optional[int],
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


def create_insumo_punto_venta_precio(
    db: Session,
    data: InsumoPuntoVentaPrecioForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> InsumoPuntoVentaPrecio:
    gestor_id = get_gestor_carga_by_params(data, gestor_carga_id)
    obj = create_insumo_punto_venta(
        db,
        data,
        gestor_id,
        modified_by,
    )
    return create_insumo_punto_venta_precio_by_insumo_punto_venta(
        db, obj, data, modified_by
    )
