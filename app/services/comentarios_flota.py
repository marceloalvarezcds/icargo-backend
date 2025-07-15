from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app import schemas, repositories
from .camion_check_files import check_files

async def create_comentario_flota(
    db: Session,
    data: schemas.ComentarioFlotaForm,
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
        modified_by,
    )
