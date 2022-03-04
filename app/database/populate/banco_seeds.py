from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Moneda
from app.schemas.banco import BancoForm
from app.services import create_banco


def banco_seeds(
    db: Session,
    numero_cuenta: str,
    titular: str,
    nombre: str,
    moneda: Optional[Moneda],
    gestor_carga_id: Optional[int],
    modified_by: str,
):
    if moneda:
        return create_banco(
            db,
            BancoForm(
                numero_cuenta=numero_cuenta,
                titular=titular,
                nombre=nombre,
                moneda_id=moneda.id,
            ),
            gestor_carga_id,
            modified_by,
        )
    return None
