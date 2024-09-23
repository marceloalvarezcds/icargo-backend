from fastapi import HTTPException
from typing import Union

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum, OrdenCargaEstadoEnum
from app.models import OrdenCargaComentariosHistorial
from typing import Optional


def create_orden_carga_comentarios_historial(
    db: Session,
    orden_carga_id: Optional[int],
    comentario: Optional[str],
    created_by: Optional[str],
    modified_by: Optional[str],
) -> OrdenCargaComentariosHistorial:
    """
    Crea un nuevo registro en la tabla orden_carga_comentarios_historial
    """

    # Crear una instancia de OrdenCargaComentariosHistorial con los valores proporcionados
    obj = OrdenCargaComentariosHistorial(
        orden_carga_id=orden_carga_id,
        comentario=comentario,
        created_by=created_by,
        modified_by=modified_by,
    )
    
    # Agregar el objeto a la sesión y realizar el commit
    db.add(obj)
    db.commit()
    db.refresh(obj)  # Refrescar el objeto para obtener los valores generados, como el ID
    
    return obj