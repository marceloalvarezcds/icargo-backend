from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import InsumoPuntoVenta, InsumoPuntoVentaPrecio


def insumo_punto_venta_precio_seeds(
    db: Session,
    insumo_punto_venta: Optional[InsumoPuntoVenta],
    precio: Decimal,
    fecha: date,
):
    try:
        if insumo_punto_venta:
            db.add(
                InsumoPuntoVentaPrecio(
                    insumo_punto_venta_id=insumo_punto_venta.id,
                    precio=precio,
                    fecha_inicio=fecha,
                )
            )
            db.commit()
    except IntegrityError:
        db.rollback()
