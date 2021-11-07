from typing import Optional

from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import (
    Cargo,
    Contacto,
    GestorCarga,
    Proveedor,
    ProveedorContactoGestorCarga,
)


def proveedor_contacto_gestor_carga_seeds(
    db: Session,
    cargo: Optional[Cargo],
    proveedor: Proveedor,
    contacto: Optional[Contacto],
    gestor_carga: GestorCarga,
    alias: str,
):
    try:
        db.add(
            ProveedorContactoGestorCarga(
                cargo_id=cargo.id if cargo else None,
                proveedor_id=proveedor.id,
                contacto_id=contacto.id if contacto else None,
                gestor_carga_id=gestor_carga.id,
                alias=alias,
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
