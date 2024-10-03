from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import OrdenCargaEvaluacionesHistorial
from app.schemas import OrdenCargaEvaluacionesHistorialForm

def get_orden_carga_evaluaciones_historial_by_id(db: Session, id: int):
    return db.query(OrdenCargaEvaluacionesHistorial).filter(OrdenCargaEvaluacionesHistorial.id == id).first()


def create_orden_carga_evaluacion(
    db: Session,
    data: OrdenCargaEvaluacionesHistorialForm,
    modified_by: str,
) -> OrdenCargaEvaluacionesHistorial:
    obj = OrdenCargaEvaluacionesHistorial(
        orden_carga_id=data.orden_carga_id,
        comentarios=data.comentarios,
        tipo_incidente_id=data.tipo_incidente_id,
        gestor_carga_id=data.gestor_carga_id,
        camion_id=data.camion_id,
        semi_id=data.semi_id,
        propietario_id=data.propietario_id,
        chofer_id=data.chofer_id,
        nota=data.nota,
        concepto=data.concepto,
        origen_id=data.origen_id,
        destino_id=data.destino_id,
        producto_id=data.producto_id,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj