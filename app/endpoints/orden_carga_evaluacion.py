from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.OrdenCargaEvaluacionesHistorial])
async def read_evaluaciones_list(
    db: Session = Depends(get_db_session), # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.ORDEN_CARGA_EVALUACION)), # noqa: B008
):
    return repositories.get_evaluacion_list(db)


@api.get("/{id}", response_model=schemas.OrdenCargaEvaluacionesHistorial)
async def read_orden_carga_remision_destino_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.ORDEN_CARGA_EVALUACION)),  # noqa: B008
):
    return services.get_orden_carga_evaluaciones_historial_by_id(db, id)


@api.post("/", response_model=schemas.OrdenCargaEvaluacionesHistorial)
async def add_new_orden_carga_remision_destino(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.OrdenCargaEvaluacionesHistorialForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.ORDEN_CARGA_EVALUACION)),  # noqa: B008
):
    return await services.create_orden_carga_evaluacion(
        db,
        data,  # type: ignore
        current_user.username,
    )


@api.put("/{id}", response_model=schemas.OrdenCargaRemisionDestino)
async def edit_orden_carga_remision_destino(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.OrdenCargaRemisionDestinoForm] = Form(...),  # type: ignore  # noqa: B008
    foto_documento_file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.ORDEN_CARGA_REMISION_DESTINO)),  # noqa: B008
):
    return await services.edit_orden_carga_remision_destino(
        id,
        db,
        data,  # type: ignore
        foto_documento_file,
        current_user.username,
    )


