from typing import Optional

from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import (
    Cargo,
    Contacto,
    GestorCarga,
    Propietario,
    PropietarioContactoGestorCarga,
)


def propietario_contacto_gestor_carga_seeds(
    db: Session,
    cargo: Optional[Cargo],
    propietario: Propietario,
    contacto: Optional[Contacto],
    gestor_carga: GestorCarga,
    alias: str,
):
    try:
        db.add(
            PropietarioContactoGestorCarga(
                cargo_id=cargo.id if cargo else None,
                propietario_id=propietario.id,
                contacto_id=contacto.id if contacto else None,
                gestor_carga_id=gestor_carga.id,
                alias=alias,
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
