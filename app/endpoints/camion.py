from http.client import HTTPException
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


@api.get("/", response_model=List[schemas.CamionList])
async def read_camion_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CAMION)),  # noqa: B008
):
    return repositories.get_camion_list(db)


@api.get("/camion/combinacion", response_model=List[schemas.CamionList])
async def read_camion_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CAMION)),  # noqa: B008
):
   return services.check_combinaciones_activas(db)


@api.get("/combinacion_por_camion/{camion_id}", response_model=schemas.Combinacion)
async def read_combinacion_by_camion_and_gestor(
    camion_id: int,  # ID del camión a buscar
    db: Session = Depends(get_db_session),  # Dependencia para obtener la sesión de la base de datos
    current_user: schemas.AuthUser = Depends(get_current_user),  # Dependencia para obtener el usuario actual
    _: bool = Depends(Permiso(a.LISTAR, m.COMBINACION)),  # Verificación de permisos
):
    # Obtener las combinaciones asociadas al camión y al gestor actual
    combinacion = repositories.get_combinacion_tracto_ids(
        db, camion_id, current_user.gestor_carga_id
    )

    if not combinacion:
        # Si no se encuentra ninguna combinación, retornar un mensaje indicando que no está en una combinación
        raise HTTPException(
            status_code=404,
            detail=f"El camión con ID {camion_id} no está asociado a ninguna combinación."
        )

    return combinacion


@api.get("/gestor_carga", response_model=List[schemas.CamionList])
async def read_camion_list_by_gestor_carga(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CAMION)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return repositories.get_camion_list_by_gestor_cuenta_id(
        db, current_user.gestor_carga_id
    )


@api.get("/producto/{producto_id}", response_model=List[schemas.CamionList])
async def read_camion_list_by_producto_id(
    producto_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CAMION)),  # noqa: B008
):
    return services.get_camion_list_by_producto_id(
        db, producto_id, current_user.gestor_carga_id
    )

@api.get("/combinacion/", response_model=List[schemas.CamionList])
async def read_camion_list_for_combinacion(
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CAMION)),  # noqa: B008
):
    return services.get_camion_list_combinacion(
        db, current_user.gestor_carga_id
    )


@api.get("/propietario/{propietario_id}", response_model=List[schemas.CamionList])
async def read_camion_list_by_propietario_id(
    propietario_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.CAMION)),  # noqa: B008
):
    return repositories.get_camion_list_by_propietario_id(db, propietario_id)


@api.get("/reports")
async def camion_reports(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.REPORTE, m.CAMION)),  # noqa: B008
):
    return services.get_camion_reports(db)


@api.get("/{id}", response_model=schemas.Camion)
async def read_camion_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.CAMION)),  # noqa: B008
):
    return services.get_camion_by_id(db, id)


@api.post("/", response_model=schemas.Camion)
async def add_new_camion(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.CamionForm] = Form(...),  # type: ignore  # noqa: B008
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
    _: bool = Depends(Permiso(a.CREAR, m.CAMION)),  # noqa: B008
):
    return await services.create_camion(
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


@api.put("/{id}", response_model=schemas.Camion)
async def edit_camion(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.CamionForm] = Form(...),  # type: ignore  # noqa: B008
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
    _: bool = Depends(Permiso(a.EDITAR, m.CAMION)),  # noqa: B008
):
    return await services.edit_camion(
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


@api.delete("/{id}", response_model=schemas.Camion)
async def delete_camion(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.ELIMINAR, m.CAMION)),  # noqa: B008
):
    return services.delete_camion(db, id, current_user.username)


@api.get("/{id}/active", response_model=schemas.Camion)
def active_camion_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.CAMION)),  # noqa: B008
):
    return services.change_camion_status(
        db, id, EstadoEnum.ACTIVO, current_user.username
    )


@api.get("/{id}/inactive", response_model=schemas.Camion)
def inactive_camion_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.CAMION)),  # noqa: B008
):
    return services.change_camion_status(
        db, id, EstadoEnum.INACTIVO, current_user.username
    )


@api.get("/combinacion/camion_list/{id}", response_model=schemas.CamionList)
def inactive_camion_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CAMBIAR_ESTADO, m.CAMION)),  # noqa: B008
):
    return services.get_camion_by_id(db, id)
