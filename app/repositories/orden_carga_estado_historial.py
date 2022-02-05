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
