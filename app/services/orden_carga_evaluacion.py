from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import repositories, schemas
from app.models import OrdenCargaEvaluacionesHistorial

def get_orden_carga_evaluaciones_historial_by_id(
    db: Session, id: int
) -> OrdenCargaEvaluacionesHistorial:
    obj = repositories.get_orden_carga_evaluaciones_historial_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Historial de evaluación de orden de carga no encontrado")
    return obj

async def create_orden_carga_evaluacion(
    db: Session,
    data: schemas.OrdenCargaEvaluacionesHistorialForm,
    modified_by: str,
) -> schemas.OrdenCargaEvaluacionesHistorial:
    return repositories.create_orden_carga_evaluacion(
        db,
        data,
        modified_by,
    )