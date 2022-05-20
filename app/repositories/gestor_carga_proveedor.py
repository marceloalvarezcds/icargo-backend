from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import GestorCargaProveedor


def get_gestor_carga_proveedor_by(
    db: Session,
    proveedor_id: int,
    gestor_carga_id: int,
) -> Optional[GestorCargaProveedor]:
    return (
        db.query(GestorCargaProveedor)
        .filter(
            GestorCargaProveedor.proveedor_id == proveedor_id,
            GestorCargaProveedor.gestor_carga_id == gestor_carga_id,
        )
        .first()
    )


def create_gestor_carga_proveedor(
    db: Session,
    proveedor_id: int,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> GestorCargaProveedor:
    obj = GestorCargaProveedor(
        proveedor_id=proveedor_id,
        gestor_carga_id=gestor_carga_id,
        alias=alias,
        estado=EstadoEnum.ACTIVO.value,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_gestor_carga_proveedor(
    obj: GestorCargaProveedor,
    db: Session,
    proveedor_id: int,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> GestorCargaProveedor:
    obj.proveedor_id = proveedor_id
    obj.gestor_carga_id = gestor_carga_id
    obj.estado = EstadoEnum.ACTIVO.value
    obj.alias = alias
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj
