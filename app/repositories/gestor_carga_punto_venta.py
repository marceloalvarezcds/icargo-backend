from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import GestorCargaPuntoVenta


def get_gestor_carga_punto_venta_by(
    db: Session,
    punto_venta_id: int,
    gestor_carga_id: int,
) -> Optional[GestorCargaPuntoVenta]:
    return (
        db.query(GestorCargaPuntoVenta)
        .filter(
            GestorCargaPuntoVenta.punto_venta_id == punto_venta_id,
            GestorCargaPuntoVenta.gestor_carga_id == gestor_carga_id,
        )
        .first()
    )


def create_gestor_carga_punto_venta(
    db: Session,
    punto_venta_id: int,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> GestorCargaPuntoVenta:
    obj = GestorCargaPuntoVenta(
        punto_venta_id=punto_venta_id,
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


def edit_gestor_carga_punto_venta(
    obj: GestorCargaPuntoVenta,
    db: Session,
    punto_venta_id: int,
    gestor_carga_id: int,
    alias: str,
    modified_by: str,
) -> GestorCargaPuntoVenta:
    obj.punto_venta_id = punto_venta_id
    obj.gestor_carga_id = gestor_carga_id
    obj.estado = EstadoEnum.ACTIVO.value
    obj.alias = alias
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj
