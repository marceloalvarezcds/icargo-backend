from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import GestorCargaPropietario, Propietario


def create_gestor_carga_propietario(
    db: Session,
    propietario: Propietario,
    gestor_carga_id: Optional[int],
    alias: Optional[str],
    modified_by: str,
) -> Optional[GestorCargaPropietario]:
    if gestor_carga_id:
        return repositories.create_gestor_carga_propietario(
            db, propietario.id, gestor_carga_id, alias, modified_by
        )
    return None


def edit_gestor_carga_propietario(
    db: Session,
    propietario: Propietario,
    gestor_carga_id: Optional[int],
    alias: Optional[str],
    modified_by: str,
) -> Optional[GestorCargaPropietario]:
    if gestor_carga_id:
        obj = repositories.get_gestor_carga_propietario_by(
            db, propietario.id, gestor_carga_id
        )
        if obj:
            return repositories.edit_gestor_carga_propietario(
                obj,
                db,
                propietario.id,
                gestor_carga_id,
                alias,
                modified_by,
            )
        else:
            return create_gestor_carga_propietario(
                db, propietario, gestor_carga_id, alias, modified_by
            )
    return None
