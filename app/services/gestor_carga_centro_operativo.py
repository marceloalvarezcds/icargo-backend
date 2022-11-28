from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import CentroOperativo, GestorCargaCentroOperativo


def create_gestor_carga_centro_operativo(
    db: Session,
    centro_operativo: CentroOperativo,
    gestor_carga_id: Optional[int],
    alias: Optional[str],
    modified_by: str,
) -> Optional[GestorCargaCentroOperativo]:
    if gestor_carga_id:
        return repositories.create_gestor_carga_centro_operativo(
            db, centro_operativo.id, gestor_carga_id, alias, modified_by
        )
    return None


def edit_gestor_carga_centro_operativo(
    db: Session,
    centro_operativo: CentroOperativo,
    gestor_carga_id: Optional[int],
    alias: Optional[str],
    modified_by: str,
) -> Optional[GestorCargaCentroOperativo]:
    if gestor_carga_id:
        obj = repositories.get_gestor_carga_centro_operativo_by(
            db, centro_operativo.id, gestor_carga_id
        )
        if obj:
            return repositories.edit_gestor_carga_centro_operativo(
                obj,
                db,
                centro_operativo.id,
                gestor_carga_id,
                alias,
                modified_by,
            )
        else:
            return create_gestor_carga_centro_operativo(
                db, centro_operativo, gestor_carga_id, alias, modified_by
            )
    return None
