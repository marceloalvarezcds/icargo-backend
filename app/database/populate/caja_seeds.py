from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Moneda
from app.schemas.caja import CajaForm
from app.services import create_caja


def caja_seeds(
    db: Session,
    nombre: str,
    moneda: Optional[Moneda],
    gestor_carga_id: Optional[int],
    modified_by: str,
):
    if moneda:
        return create_caja(
            db,
            CajaForm(nombre=nombre, moneda_id=moneda.id),
            gestor_carga_id,
            modified_by,
        )
    return None
