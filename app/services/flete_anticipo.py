from typing import Dict, List

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import Flete, FleteAnticipo, TipoAnticipo, TipoInsumo
from app.schemas import FleteAnticipoForm


def get_tipo_anticipo_list_by_flete_id(
    db: Session, flete_id: int
) -> List[TipoAnticipo]:
    id_list = []
    filtered_list = []
    original_list = repositories.get_flete_anticipo_list_by_flete_id(db, flete_id)
    tipo_anticipo_list: List[TipoAnticipo] = list(map(lambda x: x.tipo, original_list))
    for item in tipo_anticipo_list:
        # check if exists in unique_list or not
        if item.id not in id_list:
            id_list.append(item.id)
            filtered_list.append(item)
    return filtered_list


def get_tipo_insumo_list_by_flete_id(db: Session, flete_id: int) -> List[TipoInsumo]:
    id_list = []
    filtered_list = []
    original_list = repositories.get_flete_anticipo_list_by_flete_id(db, flete_id)
    tipo_insumo_list: List[TipoInsumo] = list(
        map(lambda x: x.tipo_insumo, original_list)
    )
    for item in tipo_insumo_list:
        # check if exists in unique_list or not
        if item and item.id not in id_list:
            id_list.append(item.id)
            filtered_list.append(item)
    return filtered_list


def get_flete_anticipo_by_id(db: Session, id: int) -> FleteAnticipo:
    obj = repositories.get_flete_anticipo_by_id(db, id)
    if not obj:
        raise HTTPException(
            status_code=404, detail="Complemento de Flete no encontrado"
        )
    return obj


def update_flete_anticipo_list(
    db: Session,
    dataList: List[FleteAnticipoForm],
    flete: Flete,
    modified_by: str,
):
    lista: List[FleteAnticipo] = flete.anticipos
    has_lista = len(lista) > 0
    if has_lista:
        found: Dict[int, bool] = {}
        created: Dict[str, bool] = {}
        for item in lista:
            item_id = item.id
            found[item_id] = found[item_id] if item_id in found else False
            for data in dataList:
                key = f"{data.tipo_id}_{flete.id}"
                if not data.id and key not in created:
                    created[key] = True
                    repositories.create_flete_anticipo(
                        db,
                        flete.id,
                        data,
                        modified_by,
                    )
                elif item_id == data.id and not found[item_id]:
                    obj = repositories.get_flete_anticipo_by_id(db, item_id)
                    if obj:
                        found[item_id] = True
                        repositories.edit_flete_anticipo(
                            obj,
                            db,
                            data,
                            modified_by,
                        )
            if not found[item_id]:
                repositories.delete_flete_anticipo(
                    db,
                    item_id,
                    modified_by,
                )
    else:
        for data in dataList:
            repositories.create_flete_anticipo(
                db,
                flete.id,
                data,
                modified_by,
            )
