from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import GestorCargaProveedor, Proveedor


def create_gestor_carga_proveedor(
    db: Session,
    proveedor: Proveedor,
    gestor_carga_id: Optional[int],
    alias: Optional[str],
    modified_by: str,
) -> Optional[GestorCargaProveedor]:
    if gestor_carga_id:
        return repositories.create_gestor_carga_proveedor(
            db, proveedor.id, gestor_carga_id, alias, modified_by
        )
    return None


def edit_gestor_carga_proveedor(
    db: Session,
    proveedor: Proveedor,
    gestor_carga_id: Optional[int],
    alias: Optional[str],
    modified_by: str,
) -> Optional[GestorCargaProveedor]:
    if gestor_carga_id:
        obj = repositories.get_gestor_carga_proveedor_by(
            db, proveedor.id, gestor_carga_id
        )
        if obj:
            return repositories.edit_gestor_carga_proveedor(
                obj,
                db,
                proveedor.id,
                gestor_carga_id,
                alias,
                modified_by,
            )
        else:
            return create_gestor_carga_proveedor(
                db, proveedor, gestor_carga_id, alias, modified_by
            )
    return None
