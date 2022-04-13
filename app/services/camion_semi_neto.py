from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import Camion, CamionSemiNeto, Semi
from app.schemas import CamionSemiNetoForm


def get_camion_semi_neto_list_by_producto_id(
    db: Session, producto_id: int, gestor_carga_id: int
) -> List[CamionSemiNeto]:
    camion_semi_neto_list = repositories.get_camion_semi_neto_list_by_producto_id(
        db, producto_id, gestor_carga_id
    )
    return (
        camion_semi_neto_list
        if len(camion_semi_neto_list) > 0
        else repositories.get_camion_semi_neto_list_by_producto_id_null(
            db, gestor_carga_id
        )
    )


def get_camion_semi_neto_list_by_camion_id_and_producto_id(
    db: Session, camion_id: int, producto_id: int, gestor_carga_id: int
) -> List[CamionSemiNeto]:
    camion_semi_neto_list = (
        repositories.get_camion_semi_neto_list_by_camion_id_and_producto_id(
            db, camion_id, producto_id, gestor_carga_id
        )
    )
    return (
        camion_semi_neto_list
        if len(camion_semi_neto_list) > 0
        else repositories.get_camion_semi_neto_list_by_camion_id_and_producto_id_null(
            db, camion_id, gestor_carga_id
        )
    )


def get_camion_list_by_producto_id(
    db: Session, producto_id: int, gestor_carga_id: int
) -> List[Camion]:
    id_list = []
    filtered_list = []
    original_list = get_camion_semi_neto_list_by_producto_id(
        db, producto_id, gestor_carga_id
    )
    camion_list: List[Camion] = list(map(lambda x: x.camion, original_list))
    for item in camion_list:
        # check if exists in unique_list or not
        if item.id not in id_list:
            id_list.append(item.id)
            filtered_list.append(item)
    return filtered_list


def get_semi_list_by_camion_id_and_producto_id(
    db: Session, camion_id: int, producto_id: int, gestor_carga_id: int
) -> List[Semi]:
    id_list = []
    filtered_list = []
    original_list = get_camion_semi_neto_list_by_camion_id_and_producto_id(
        db, camion_id, producto_id, gestor_carga_id
    )
    semi_list: List[Semi] = list(map(lambda x: x.semi, original_list))
    for item in semi_list:
        # check if exists in unique_list or not
        if item.id not in id_list:
            id_list.append(item.id)
            filtered_list.append(item)
    return filtered_list


def get_camion_semi_neto_by_camion_id_and_semi_id_and_producto_id(
    db: Session,
    camion_id: int,
    semi_id: int,
    producto_id: Optional[int],
    gestor_carga_id: int,
) -> Optional[CamionSemiNeto]:
    obj = None
    if producto_id:
        obj = (
            repositories.get_camion_semi_neto_by_camion_id_and_semi_id_and_producto_id(
                db, camion_id, semi_id, producto_id, gestor_carga_id
            )
        )
    if obj is None:
        return repositories.get_camion_semi_neto_by_camion_id_and_semi_id(
            db, camion_id, semi_id, gestor_carga_id
        )
    return obj


def check_if_combination_exists(
    db: Session,
    data: CamionSemiNetoForm,
    gestor_carga_id: int,
    id: Optional[int] = None,
):
    producto_id = data.producto_id
    exists = get_camion_semi_neto_by_camion_id_and_semi_id_and_producto_id(
        db, data.camion_id, data.semi_id, data.producto_id, gestor_carga_id
    )
    if producto_id:
        msg = f"La combinación de Camion Nº {data.camion_id} con Semi Nº {data.semi_id} y Producto Nº {producto_id} ya existe"  # noqa
        error = HTTPException(status_code=409, detail=msg)
        if id:
            if exists and exists.id != id:
                raise error
        elif exists:
            raise error
    else:
        msg = f"La combinación de Camion Nº {data.camion_id} con Semi Nº {data.semi_id} ya existe"  # noqa
        error = HTTPException(status_code=409, detail=msg)
        if id:
            if exists and exists.id != id:
                raise error
        elif exists:
            raise error


def create_camion_semi_neto(
    db: Session,
    data: CamionSemiNetoForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> CamionSemiNetoForm:
    if not gestor_carga_id:
        raise HTTPException(status_code=409, detail="Debe elegir un Gestor de carga")
    check_if_combination_exists(db, data, gestor_carga_id)
    return repositories.create_camion_semi_neto(
        db,
        data,
        gestor_carga_id,
        modified_by,
    )


def get_camion_semi_neto_by_id(db: Session, id: int) -> CamionSemiNeto:
    obj = repositories.get_camion_semi_neto_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Camion no encontrado")
    return obj


def edit_camion_semi_neto(
    id: int,
    db: Session,
    data: CamionSemiNetoForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> CamionSemiNetoForm:
    to_edit_obj = get_camion_semi_neto_by_id(db, id)
    gestor_id = gestor_carga_id if gestor_carga_id else to_edit_obj.gestor_carga_id
    check_if_combination_exists(db, data, gestor_id, id)
    return repositories.edit_camion_semi_neto(
        to_edit_obj,
        db,
        data,
        modified_by,
    )


def delete_camion_semi_neto(
    db: Session, id: int, modified_by: str
) -> CamionSemiNetoForm:
    co = get_camion_semi_neto_by_id(db, id)
    return repositories.delete_camion_semi_neto(co, db, modified_by)
