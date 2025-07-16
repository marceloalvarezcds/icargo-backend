from typing import List, Optional
from app.models import ComentarioFlota
from app.schemas import ComentarioFlotaForm
from sqlalchemy.orm import Session
from datetime import datetime

def create_comentario_flota(
    db: Session,
    data: ComentarioFlotaForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> ComentarioFlota:
    obj = ComentarioFlota(
        comentable_type=data.comentable_type,
        comentable_id=data.comentable_id,
        comentario=data.comentario,
        tipo_evento=data.tipo_evento,
        archivo=data.archivo,
        gestor_carga_id=gestor_carga_id,
        modified_by=modified_by,
        created_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_comentarios_flota_by_entidad_and_gestor(
    db: Session,
    comentable_type: str,
    comentable_id: int,
    gestor_carga_id: int
) -> List[ComentarioFlota]:
    return (
        db.query(ComentarioFlota)
        .filter(
            ComentarioFlota.comentable_type == comentable_type,
            ComentarioFlota.comentable_id == comentable_id,
            ComentarioFlota.gestor_carga_id == gestor_carga_id,
        )
        .order_by(ComentarioFlota.id.desc())
        .all()
    )

def get_comentarios_flota_by_entidad(
    db: Session,
    comentable_type: str,
    comentable_id: int
) -> List[ComentarioFlota]:
    return (
        db.query(ComentarioFlota)
        .filter(
            ComentarioFlota.comentable_type == comentable_type,
            ComentarioFlota.comentable_id == comentable_id,
        )
        .order_by(ComentarioFlota.id.desc())
        .all()
    )
