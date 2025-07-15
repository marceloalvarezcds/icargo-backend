from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums.estado import EstadoEnum
from app.schemas.user import AuthUser

api = APIRouter()

@api.post("/", response_model=schemas.ComentarioFlota)
async def add_comentario_flota(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.ComentarioFlotaForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.COMBINACION)),  # noqa: B008
):
    return await services.create_comentario_flota(
        db=db,
        data=data,  # type: ignore
        modified_by=current_user.username,
    )


@api.get("/{comentable_type}/{comentable_id}", response_model=List[schemas.ComentarioFlotaList])
async def read_comentarios_flota_by_entidad(
    comentable_type: str,
    comentable_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CAMION)),  # podés ajustar esto según el módulo
):
    return repositories.get_comentarios_flota_by_entidad(db, comentable_type, comentable_id)
