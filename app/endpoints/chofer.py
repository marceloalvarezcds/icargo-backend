from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums.estado import EstadoEnum

api = APIRouter()


@api.get("/", response_model=List[schemas.ChoferList])
async def read_chofer_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CHOFER)),  # noqa: B008
):
    return repositories.get_chofer_list(db)


@api.get("/gestor_cuenta", response_model=List[schemas.ChoferList])
async def read_chofer_list_by_gestor_cuenta(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CHOFER)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return repositories.get_chofer_list_by_gestor_cuenta_id(
        db, current_user.gestor_carga_id
    )


@api.get("/without_camion", response_model=List[schemas.ChoferList])
async def read_chofer_list_by_without_camion(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CHOFER)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return repositories.get_chofer_list_without_camion(db, current_user.gestor_carga_id)


@api.get("/without_camion/{camion_id}", response_model=List[schemas.ChoferList])
async def read_chofer_list_by_without_camion_by_camion_id(
    camion_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CHOFER)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_chofer_list_without_camion_by_camion_id(
        db, camion_id, current_user.gestor_carga_id
    )


@api.get("/reports")
async def chofer_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.CHOFER)),  # noqa: B008
):
    return services.get_chofer_reports(db)


@api.get("/{id}", response_model=schemas.Chofer)
async def read_chofer_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.CHOFER)),  # noqa: B008
):
    return services.get_chofer_by_id_and_gestor_cuenta_id(
        db, id, current_user.gestor_carga_id
    )


@api.post("/", response_model=schemas.Chofer)
async def add_new_chofer(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.ChoferForm] = Form(...),  # type: ignore  # noqa: B008
    foto_documento_frente_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_documento_reverso_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_perfil_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_registro_frente_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_registro_reverso_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_documento_frente_propietario_file: Optional[UploadFile] = File(  # noqa: B008
        None
    ),
    foto_documento_reverso_propietario_file: Optional[UploadFile] = File(  # noqa: B008
        None
    ),
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.CHOFER)),  # noqa: B008
):
    return await services.create_chofer(
        db,
        data,  # type: ignore
        foto_documento_frente_file,
        foto_documento_reverso_file,
        foto_perfil_file,
        foto_registro_frente_file,
        foto_registro_reverso_file,
        foto_documento_frente_propietario_file,
        foto_documento_reverso_propietario_file,
        current_user.gestor_carga_id,
        current_user.username,
        current_user.id,
    )


@api.put("/{id}", response_model=schemas.Chofer)
async def edit_chofer(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.ChoferEditForm] = Form(...),  # type: ignore  # noqa: B008
    foto_documento_frente_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_documento_reverso_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_perfil_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_registro_frente_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_registro_reverso_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_documento_frente_propietario_file: UploadFile = File(None),  # noqa: B008
    foto_documento_reverso_propietario_file: UploadFile = File(None),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.CHOFER)),  # noqa: B008
):
    return await services.edit_chofer(
        id,
        db,
        data,  # type: ignore
        foto_documento_frente_file,
        foto_documento_reverso_file,
        foto_perfil_file,
        foto_registro_frente_file,
        foto_registro_reverso_file,
        foto_documento_frente_propietario_file,
        foto_documento_reverso_propietario_file,
        current_user.gestor_carga_id,
        current_user.username,
    )


@api.delete("/{id}", response_model=schemas.Chofer)
async def delete_chofer(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.CHOFER)),  # noqa: B008
):
    return services.delete_chofer(
        db, id, current_user.gestor_carga_id, current_user.username
    )


@api.get("/{id}/active", response_model=schemas.Chofer)
def active_chofer_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.CHOFER)),  # noqa: B008
):
    return services.change_chofer_status(
        db, id, EstadoEnum.ACTIVO, current_user.username
    )


@api.get("/{id}/inactive", response_model=schemas.Chofer)
def inactive_chofer_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.CHOFER)),  # noqa: B008
):
    return services.change_chofer_status(
        db, id, EstadoEnum.INACTIVO, current_user.username
    )
