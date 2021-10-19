from typing import Optional

from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import (
    Cargo,
    CentroOperativo,
    CentroOperativoContactoGestorCarga,
    Contacto,
    GestorCarga,
)


def centro_operativo_contacto_gestor_carga_seeds(
    db: Session,
    cargo: Optional[Cargo],
    centro_operativo: CentroOperativo,
    contacto: Optional[Contacto],
    gestor_carga: GestorCarga,
):
    try:
        db.add(
            CentroOperativoContactoGestorCarga(
                cargo_id=cargo.id if cargo else None,
                centro_operativo_id=centro_operativo.id,
                contacto_id=contacto.id if contacto else None,
                gestor_carga_id=gestor_carga.id,
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
