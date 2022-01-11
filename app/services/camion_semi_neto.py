from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import Camion, CamionSemiNeto, Semi


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
        else repositories.get_camion_semi_neto_list_by_camion_id(
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
    db: Session, camion_id: int, semi_id: int, producto_id: int, gestor_carga_id: int
) -> Optional[CamionSemiNeto]:
    obj = repositories.get_camion_semi_neto_by_camion_id_and_semi_id_and_producto_id(
        db, camion_id, semi_id, producto_id, gestor_carga_id
    )
    if obj is None:
        return repositories.get_camion_semi_neto_by_camion_id_and_semi_id(
            db, camion_id, semi_id, gestor_carga_id
        )
    return obj
