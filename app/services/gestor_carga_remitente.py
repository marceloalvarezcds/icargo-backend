from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import GestorCargaRemitente, Remitente


def create_gestor_carga_remitente(
    db: Session,
    remitente: Remitente,
    gestor_carga_id: Optional[int],
    alias: Optional[str],
    modified_by: str,
) -> Optional[GestorCargaRemitente]:
    if gestor_carga_id:
        alias_or_nombre = alias if alias else remitente.nombre
        return repositories.create_gestor_carga_remitente(
            db, remitente.id, gestor_carga_id, alias_or_nombre, modified_by
        )
    return None


def edit_gestor_carga_remitente(
    db: Session,
    remitente: Remitente,
    gestor_carga_id: Optional[int],
    alias: Optional[str],
    modified_by: str,
) -> Optional[GestorCargaRemitente]:
    if gestor_carga_id:
        obj = repositories.get_gestor_carga_remitente_by(
            db, remitente.id, gestor_carga_id
        )
        if obj:
            alias_or_nombre = (
                alias if alias else obj.alias if obj.alias else remitente.nombre
            )
            return repositories.edit_gestor_carga_remitente(
                obj,
                db,
                remitente.id,
                gestor_carga_id,
                alias_or_nombre,
                modified_by,
            )
        else:
            return create_gestor_carga_remitente(
                db, remitente, gestor_carga_id, alias, modified_by
            )
    return None
