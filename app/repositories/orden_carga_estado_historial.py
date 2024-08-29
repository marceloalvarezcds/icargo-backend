from fastapi import HTTPException
from typing import Union

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum, OrdenCargaEstadoEnum
from app.models import OrdenCargaEstadoHistorial


def create_orden_carga_estado_historial(
    db: Session,
    orden_carga_id: int,
    estado: Union[EstadoEnum, OrdenCargaEstadoEnum],
    modified_by: str,
) -> OrdenCargaEstadoHistorial:
    # Verificar si el estado ya está como ACEPTADO
    current_estado = db.query(OrdenCargaEstadoHistorial).filter_by(
        orden_carga_id=orden_carga_id
    ).order_by(OrdenCargaEstadoHistorial.created_at.desc()).first()
    
    if current_estado and current_estado.estado == EstadoEnum.ACEPTADO.value:
        raise HTTPException(status_code=400, detail="La orden de carga ya ha sido aceptada.")

    if current_estado and current_estado.estado == EstadoEnum.CANCELADO.value:
        raise HTTPException(status_code=400, detail="La orden de carga ya ha sido cancelada.")

    # Si no está aceptado, se procede a crear el historial
    obj = OrdenCargaEstadoHistorial(
        estado=estado.value,
        orden_carga_id=orden_carga_id,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj