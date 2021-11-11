from typing import Optional

from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import (
    Cargo,
    Contacto,
    GestorCarga,
    PuntoVenta,
    PuntoVentaContactoGestorCarga,
)


def punto_venta_contacto_gestor_carga_seeds(
    db: Session,
    cargo: Optional[Cargo],
    punto_venta: PuntoVenta,
    contacto: Optional[Contacto],
    gestor_carga: GestorCarga,
    alias: str,
):
    try:
        db.add(
            PuntoVentaContactoGestorCarga(
                cargo_id=cargo.id if cargo else None,
                punto_venta_id=punto_venta.id,
                contacto_id=contacto.id if contacto else None,
                gestor_carga_id=gestor_carga.id,
                alias=alias,
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
