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


@api.get("/", response_model=List[schemas.SemiList])
async def read_semi_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.SEMIRREMOLQUE)),  # noqa: B008
):
    return repositories.get_semi_list(db)


@api.get(
    "/camion/{camion_id}/producto/{producto_id}", response_model=List[schemas.SemiList]
)
async def read_semi_list_by_camion_id(
    camion_id: int,
    producto_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.SEMIRREMOLQUE)),  # noqa: B008
):
    return services.get_semi_list_by_camion_id_and_producto_id(
        db, camion_id, producto_id, current_user.gestor_carga_id
    )

@api.get(
    "/camion/{camion_id}", response_model=List[schemas.SemiList]
)
async def read_semi_list_by_combinacion_camion_id(
    camion_id: int,

    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.SEMIRREMOLQUE)),  # noqa: B008
):
    return services.get_semi_list_by_camion_id(
        db, camion_id, current_user.gestor_carga_id
    )



@api.get("/propietario/{propietario_id}", response_model=List[schemas.SemiList])
async def read_semi_list_by_propietario_id(
    propietario_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.SEMIRREMOLQUE)),  # noqa: B008
):
    return repositories.get_semi_list_by_propietario_id(db, propietario_id)


@api.get("/reports")
async def semi_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.SEMIRREMOLQUE)),  # noqa: B008
):
    return services.get_semi_reports(db)


@api.get("/{id}", response_model=schemas.Semi)
async def read_semi_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.SEMIRREMOLQUE)),  # noqa: B008
):
    return services.get_semi_by_id(db, id)


@api.post("/", response_model=schemas.Semi)
async def add_new_semi(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.SemiForm] = Form(...),  # type: ignore  # noqa: B008
    foto_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_habilitacion_municipal_frente_file: Optional[UploadFile] = File(  # noqa: B008
        None
    ),
    foto_habilitacion_municipal_reverso_file: Optional[UploadFile] = File(  # noqa: B008
        None
    ),
    foto_habilitacion_transporte_frente_file: Optional[UploadFile] = File(  # noqa: B008
        None
    ),
    foto_habilitacion_transporte_reverso_file: Optional[
        UploadFile
    ] = File(  # noqa: B008
        None
    ),
    foto_habilitacion_automotor_frente_file: Optional[UploadFile] = File(  # noqa: B008
        None
    ),
    foto_habilitacion_automotor_reverso_file: Optional[UploadFile] = File(  # noqa: B008
        None
    ),
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.SEMIRREMOLQUE)),  # noqa: B008
):
    return await services.create_semi(
        db,
        data,  # type: ignore
        foto_file,
        foto_habilitacion_municipal_frente_file,
        foto_habilitacion_municipal_reverso_file,
        foto_habilitacion_transporte_frente_file,
        foto_habilitacion_transporte_reverso_file,
        foto_habilitacion_automotor_frente_file,
        foto_habilitacion_automotor_reverso_file,
        current_user.gestor_carga_id,
        current_user.username,
        current_user.id,
    )


@api.put("/{id}", response_model=schemas.Semi)
async def edit_semi(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.SemiForm] = Form(...),  # type: ignore  # noqa: B008
    foto_file: Optional[UploadFile] = File(None),  # noqa: B008
    foto_habilitacion_municipal_frente_file: Optional[UploadFile] = File(  # noqa: B008
        None
    ),
    foto_habilitacion_municipal_reverso_file: Optional[UploadFile] = File(  # noqa: B008
        None
    ),
    foto_habilitacion_transporte_frente_file: Optional[UploadFile] = File(  # noqa: B008
        None
    ),
    foto_habilitacion_transporte_reverso_file: Optional[
        UploadFile
    ] = File(  # noqa: B008
        None
    ),
    foto_habilitacion_automotor_frente_file: Optional[UploadFile] = File(  # noqa: B008
        None
    ),
    foto_habilitacion_automotor_reverso_file: Optional[UploadFile] = File(  # noqa: B008
        None
    ),
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.EDITAR, m.SEMIRREMOLQUE)),  # noqa: B008
):
    return await services.edit_semi(
        id,
        db,
        data,  # type: ignore
        foto_file,
        foto_habilitacion_municipal_frente_file,
        foto_habilitacion_municipal_reverso_file,
        foto_habilitacion_transporte_frente_file,
        foto_habilitacion_transporte_reverso_file,
        foto_habilitacion_automotor_frente_file,
        foto_habilitacion_automotor_reverso_file,
        current_user.username,
    )


@api.delete("/{id}", response_model=schemas.Semi)
async def delete_semi(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.SEMIRREMOLQUE)),  # noqa: B008
):
    return services.delete_semi(db, id, current_user.username)


@api.get("/{id}/active", response_model=schemas.Semi)
def active_semi_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.SEMIRREMOLQUE)),  # noqa: B008
):
    return services.change_semi_status(db, id, EstadoEnum.ACTIVO, current_user.username)


@api.get("/{id}/inactive", response_model=schemas.Semi)
def inactive_semi_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.SEMIRREMOLQUE)),  # noqa: B008
):
    return services.change_semi_status(
        db, id, EstadoEnum.INACTIVO, current_user.username
    )
