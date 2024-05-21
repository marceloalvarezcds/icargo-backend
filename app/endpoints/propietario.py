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


@api.get("/", response_model=List[schemas.PropietarioList])
async def read_propietario_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.PROPIETARIO)),  # noqa: B008
):
    return repositories.get_propietario_list(db)


@api.get("/gestor_cuenta", response_model=List[schemas.PropietarioList])
async def read_propietario_list_by_gestor_cuenta(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.PROPIETARIO)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return repositories.get_propietario_list_by_gestor_cuenta_id(
        db, current_user.gestor_carga_id
    )


@api.get(
    "/gestor_cuenta/camion/{camion_id}", response_model=List[schemas.PropietarioList]
)
async def read_propietario_list_by_gestor_cuenta_and_camion_id(
    camion_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.PROPIETARIO)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_propietario_list_by_gestor_cuenta_and_camion_id(
        db, camion_id, current_user.gestor_carga_id
    )


@api.get("/gestor_cuenta/semi/{semi_id}", response_model=List[schemas.PropietarioList])
async def read_propietario_list_by_gestor_cuenta_and_semi_id(
    semi_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.PROPIETARIO)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return services.get_propietario_list_by_gestor_cuenta_and_semi_id(
        db, semi_id, current_user.gestor_carga_id
    )

@api.get("/tipo_persona/{tipo_persona_id}", response_model=List[schemas.Propietario])
async def read_propietario_list_by_tipo_persona_id(
    tipo_persona_id: int, 
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.PROPIETARIO)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
  
):
    return services.get_propietario_list_by_tipo_persona_id(
        db, tipo_persona_id
    )

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
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.PROPIETARIO)),  # noqa: B008
):
    return services.get_propietario_by_id_and_gestor_cuenta_id(
        db, id, current_user.gestor_carga_id
    )


@api.post("/", response_model=schemas.Propietario)
async def add_new_propietario(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.PropietarioForm] = Form(...),  # type: ignore  # noqa: B008
    foto_documento_frente_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_documento_reverso_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_perfil_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_documento_frente_chofer_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_documento_reverso_chofer_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_registro_frente_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_registro_reverso_file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.PROPIETARIO)),  # noqa: B008
):
    return await services.create_propietario(
        db,
        data,  # type: ignore
        foto_documento_frente_file,
        foto_documento_reverso_file,
        foto_perfil_file,
        foto_documento_frente_chofer_file,
        foto_documento_reverso_chofer_file,
        foto_registro_frente_file,
        foto_registro_reverso_file,
        current_user.gestor_carga_id,
        current_user.username,
    )


@api.put("/{id}", response_model=schemas.Propietario)
async def edit_propietario(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.PropietarioEditForm] = Form(...),  # type: ignore  # noqa: B008
    foto_documento_frente_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_documento_reverso_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_perfil_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_documento_frente_chofer_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_documento_reverso_chofer_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_registro_frente_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_registro_reverso_file: Optional[UploadFile] = File(None),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.PROPIETARIO)),  # noqa: B008
):
    return await services.edit_propietario(
        id,
        db,
        data,  # type: ignore
        foto_documento_frente_file,
        foto_documento_reverso_file,
        foto_perfil_file,
        foto_documento_frente_chofer_file,
        foto_documento_reverso_chofer_file,
        foto_registro_frente_file,
        foto_registro_reverso_file,
        current_user.gestor_carga_id,
        current_user.username,
    )


@api.delete("/{id}", response_model=schemas.Propietario)
async def delete_propietario(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.PROPIETARIO)),  # noqa: B008
):
    return services.delete_propietario(
        db, id, current_user.gestor_carga_id, current_user.username
    )


@api.get("/{id}/active", response_model=schemas.Propietario)
def active_propietario_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.PROPIETARIO)),  # noqa: B008
):
    return services.change_propietario_status(
        db, id, EstadoEnum.ACTIVO, current_user.username
    )


@api.get("/{id}/inactive", response_model=schemas.Propietario)
def inactive_propietario_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.PROPIETARIO)),  # noqa: B008
):
    return services.change_propietario_status(
        db, id, EstadoEnum.INACTIVO, current_user.username
    )
