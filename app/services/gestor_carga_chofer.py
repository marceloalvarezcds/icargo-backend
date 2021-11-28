from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import Chofer, GestorCargaChofer


def create_gestor_carga_chofer(
    db: Session,
    chofer: Chofer,
    gestor_carga_id: Optional[int],
    alias: Optional[str],
    modified_by: str,
) -> Optional[GestorCargaChofer]:
    if gestor_carga_id:
        alias_or_nombre = alias if alias else chofer.nombre
        return repositories.create_gestor_carga_chofer(
            db, chofer.id, gestor_carga_id, alias_or_nombre, modified_by
        )
    return None


def edit_gestor_carga_chofer(
    db: Session,
    chofer: Chofer,
    gestor_carga_id: Optional[int],
    alias: Optional[str],
    modified_by: str,
) -> Optional[GestorCargaChofer]:
    if gestor_carga_id:
        obj = repositories.get_gestor_carga_chofer_by(db, chofer.id, gestor_carga_id)
        if obj:
            alias_or_nombre = (
                alias if alias else obj.alias if obj.alias else chofer.nombre
            )
            return repositories.edit_gestor_carga_chofer(
                obj,
                db,
                chofer.id,
                gestor_carga_id,
                alias_or_nombre,
                modified_by,
            )
        else:
            return create_gestor_carga_chofer(
                db, chofer, gestor_carga_id, alias, modified_by
            )
    return None
