from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Insumo, Moneda, Proveedor, PuntoVenta
from app.models.tipo_insumo import TipoInsumo
from app.repositories import (
    get_insumo_punto_venta_list_by_gestor_carga_id,
    get_insumo_punto_venta_list_by_insumo_id,
    get_insumo_punto_venta_list_by_insumo_id_and_punto_venta_id,
    get_insumo_punto_venta_list_by_tipo_insumo_id,
)
from app.services import get_tipo_insumo_list_by_flete_id


def get_moneda_list_by_insumo_id_and_punto_venta_id(
    db: Session, insumo_id: int, punto_venta_id: int, gestor_carga_id: Optional[int]
) -> List[Moneda]:
    id_list = []
    filtered_list = []
    original_list = get_insumo_punto_venta_list_by_insumo_id_and_punto_venta_id(
        db, insumo_id, punto_venta_id, gestor_carga_id
    )
    punto_venta_list: List[Moneda] = list(map(lambda x: x.moneda, original_list))
    for item in punto_venta_list:
        # check if exists in unique_list or not
        if item.id not in id_list:
            id_list.append(item.id)
            filtered_list.append(item)
    return filtered_list


def get_tipo_insumo_list_by_flete_id_and_gestor_carga_id(
    db: Session, flete_id: int, gestor_carga_id: Optional[int]
) -> List[TipoInsumo]:
    if gestor_carga_id:
        id_list = []
        filtered_list = []
        list_by_flete_id = get_tipo_insumo_list_by_flete_id(db, flete_id)
        original_list = get_insumo_punto_venta_list_by_gestor_carga_id(
            db, gestor_carga_id
        )
        list_by_gestor_cuenta_id: List[TipoInsumo] = list(
            map(lambda x: x.insumo.tipo, original_list)
        )
        tipo_insumo_list = list(set(list_by_flete_id) & set(list_by_gestor_cuenta_id))
        for item in tipo_insumo_list:
            # check if exists in unique_list or not
            if item.id not in id_list:
                id_list.append(item.id)
                filtered_list.append(item)
        return filtered_list
    return []


def get_insumo_list_by_tipo_insumo_id_and_gestor_carga_id(
    db: Session, tipo_insumo_id: int, gestor_carga_id: Optional[int]
) -> List[Insumo]:
    id_list = []
    filtered_list = []
    original_list = get_insumo_punto_venta_list_by_tipo_insumo_id(
        db, tipo_insumo_id, gestor_carga_id
    )
    insumo_list: List[Insumo] = list(map(lambda x: x.insumo, original_list))
    for item in insumo_list:
        # check if exists in unique_list or not
        if item.id not in id_list:
            id_list.append(item.id)
            filtered_list.append(item)
    return filtered_list


def get_punto_venta_list_by_insumo_id(
    db: Session, insumo_id: int, gestor_carga_id: Optional[int]
) -> List[PuntoVenta]:
    id_list = []
    filtered_list = []
    original_list = get_insumo_punto_venta_list_by_insumo_id(
        db, insumo_id, gestor_carga_id
    )
    punto_venta_list: List[PuntoVenta] = list(
        map(lambda x: x.punto_venta, original_list)
    )
    for item in punto_venta_list:
        # check if exists in unique_list or not
        if item.id not in id_list:
            id_list.append(item.id)
            filtered_list.append(item)
    return filtered_list


def get_proveedor_list_by_insumo_id(
    db: Session, insumo_id: int, gestor_carga_id: Optional[int]
) -> List[Proveedor]:
    id_list = []
    filtered_list = []
    original_list = get_punto_venta_list_by_insumo_id(db, insumo_id, gestor_carga_id)
    proveedor_list: List[Proveedor] = list(map(lambda x: x.proveedor, original_list))
    for item in proveedor_list:
        # check if exists in unique_list or not
        if item.id not in id_list:
            id_list.append(item.id)
            filtered_list.append(item)
    return filtered_list


def get_punto_venta_list_by_insumo_id_and_proveedor_id(
    db: Session, insumo_id: int, proveedor_id: int, gestor_carga_id: Optional[int]
) -> List[Proveedor]:
    id_list = []
    filtered_list = []
    punto_venta_list = get_punto_venta_list_by_insumo_id(db, insumo_id, gestor_carga_id)
    for item in punto_venta_list:
        if proveedor_id == item.proveedor_id:
            # check if exists in unique_list or not
            if item.id not in id_list:
                id_list.append(item.id)
                filtered_list.append(item)
    return filtered_list
