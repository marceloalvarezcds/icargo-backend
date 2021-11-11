from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import GestorCarga, GestorCargaPuntoVenta, PuntoVenta


def gestor_carga_punto_venta_seeds(
    db: Session,
    punto_venta: PuntoVenta,
    gestor_carga: GestorCarga,
    alias: str,
):
    try:
        db.add(
            GestorCargaPuntoVenta(
                punto_venta_id=punto_venta.id,
                gestor_carga_id=gestor_carga.id,
                alias=alias,
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
