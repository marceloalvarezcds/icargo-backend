from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas, repositories
from app.models.comentarios_flota import ComentarioFlota
from .camion_check_files import check_files

async def create_comentario_flota(
    db: Session,
    data: schemas.ComentarioFlotaForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> schemas.ComentarioFlota:

    if data.comentable_type not in ["camion", "semi", "chofer", "propietario"]:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo comentable no válido: {data.comentable_type}",
        )

    return repositories.create_comentario_flota(
        db,
        data,
        gestor_carga_id,
        modified_by,
    )


def get_comentarios_flota_by_entidad(
    db: Session,
    comentable_type: str,
    comentable_id: int,
    gestor_carga_id: Optional[int]
) -> List[ComentarioFlota]:
    if gestor_carga_id:
        return repositories.get_comentarios_flota_by_entidad_and_gestor(
            db, comentable_type, comentable_id, gestor_carga_id
        )
    return repositories.get_comentarios_flota_by_entidad(
        db, comentable_type, comentable_id
    )
