from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import GestorCargaPuntoVenta, PuntoVenta


def create_gestor_carga_punto_venta(
    db: Session,
    punto_venta: PuntoVenta,
    gestor_carga_id: Optional[int],
    alias: Optional[str],
    modified_by: str,
) -> Optional[GestorCargaPuntoVenta]:
    if gestor_carga_id:
        alias_or_nombre = alias if alias else punto_venta.nombre
        return repositories.create_gestor_carga_punto_venta(
            db, punto_venta.id, gestor_carga_id, alias_or_nombre, modified_by
        )
    return None


def edit_gestor_carga_punto_venta(
    db: Session,
    punto_venta: PuntoVenta,
    gestor_carga_id: Optional[int],
    alias: Optional[str],
    modified_by: str,
) -> Optional[GestorCargaPuntoVenta]:
    if gestor_carga_id:
        obj = repositories.get_gestor_carga_punto_venta_by(
            db, punto_venta.id, gestor_carga_id
        )
        if obj:
            alias_or_nombre = (
                alias if alias else obj.alias if obj.alias else punto_venta.nombre
            )
            return repositories.edit_gestor_carga_punto_venta(
                obj,
                db,
                punto_venta.id,
                gestor_carga_id,
                alias_or_nombre,
                modified_by,
            )
        else:
            return create_gestor_carga_punto_venta(
                db, punto_venta, gestor_carga_id, alias, modified_by
            )
    return None
