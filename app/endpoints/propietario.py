from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.PropietarioList])
async def read_propietario_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.PROPIETARIO)),  # noqa: B008
):
    return repositories.get_propietario_list(db)


@api.get("/reports")
async def propietario_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.PROPIETARIO)),  # noqa: B008
):
    return services.get_propietario_reports(db)


@api.get("/{id}", response_model=schemas.Propietario)
async def read_propietario_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.PROPIETARIO)),  # noqa: B008
):
    return services.get_propietario_by_id_and_gestor_cuenta_id(
        db, id, current_user.gestor_carga_id
    )


@api.post("/", response_model=schemas.Propietario)
async def add_new_propietario(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.PropietarioForm] = Form(...),  # type: ignore  # noqa: B008
    foto_documento_file: UploadFile = File(None),  # noqa: B008
    foto_perfil_file: UploadFile = File(None),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.PROPIETARIO)),  # noqa: B008
):
    return await services.create_propietario(
        db,
        data,  # type: ignore
        foto_documento_file,
        foto_perfil_file,
        current_user.gestor_carga_id,
        current_user.username,
    )


@api.put("/{id}", response_model=schemas.Propietario)
async def edit_propietario(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.PropietarioEditForm] = Form(...),  # type: ignore  # noqa: B008
    foto_documento_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_perfil_file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.PROPIETARIO)),  # noqa: B008
):
    return await services.edit_propietario(
        id,
        db,
        data,  # type: ignore
        foto_documento_file,
        foto_perfil_file,
        current_user.gestor_carga_id,
        current_user.username,
    )


@api.delete("/{id}", response_model=schemas.Propietario)
async def delete_propietario(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.PROPIETARIO)),  # noqa: B008
):
    return services.delete_propietario(
        db, id, current_user.gestor_carga_id, current_user.username
    )
