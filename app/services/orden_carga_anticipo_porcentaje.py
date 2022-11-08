from decimal import Decimal
from http import HTTPStatus
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app.models import FleteAnticipo, OrdenCargaAnticipoPorcentaje
from app.repositories import get_orden_carga_anticipo_saldo_by
from app.schemas import OrdenCargaAnticipoPorcentajeForm

from . import generic_service as service
from .orden_carga_anticipo_porcentaje_create import (
    create_orden_carga_anticipo_porcentaje,
)
from .orden_carga_anticipo_saldo import update_orden_carga_anticipo_saldo


def create_orden_carga_anticipo_porcentaje_by_flete_anticipo_list(
    db: Session,
    orden_carga_id: int,
    flete_anticipo_list: List[FleteAnticipo],
    modified_by: str,
):
    for flete_anticipo in flete_anticipo_list:
        create_orden_carga_anticipo_porcentaje(
            db, orden_carga_id, flete_anticipo, modified_by
        )


def edit_orden_carga_anticipo_porcentaje(
    id: int,
    orden_carga_id: int,
    db: Session,
    to_edit: OrdenCargaAnticipoPorcentaje,
    data: OrdenCargaAnticipoPorcentajeForm,
    modified_by: str,
) -> Optional[OrdenCargaAnticipoPorcentaje]:
    if data.porcentaje == to_edit.porcentaje:
        return to_edit  # Si no hay cambios no se edita
    if data.porcentaje and data.porcentaje < to_edit.porcentaje_minimo:
        err = f"El porcentaje {data.porcentaje}% de anticipo debe ser mayor o igual que {to_edit.porcentaje_minimo}"  # noqa: B950
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=err)
    flete_anticipo_id = data.flete_anticipo_id
    obj: OrdenCargaAnticipoPorcentaje = service.edit(
        OrdenCargaAnticipoPorcentaje,
        db,
        id,
        data,
        modified_by,
        "El Porcentaje de Anticipo",
        flete_anticipo_id=flete_anticipo_id,
        orden_carga_id=orden_carga_id,
    )
    # Se actualiza la tabla de saldos con el nuevo porcentaje
    saldo = get_orden_carga_anticipo_saldo_by(db, flete_anticipo_id, orden_carga_id)
    if saldo:
        update_orden_carga_anticipo_saldo(
            db,
            obj.flete_anticipo,
            obj.orden_carga,
            Decimal(0),
            saldo.total_complemento,
            modified_by,
        )
    return obj


def edit_orden_carga_anticipo_porcentaje_by_oc_porcentaje_anticipos(
    orden_carga_id: int,
    db: Session,
    to_edit_list: List[OrdenCargaAnticipoPorcentaje],
    lista: List[OrdenCargaAnticipoPorcentajeForm],
    modified_by: str,
):
    for data in lista:
        filtered_list: List[OrdenCargaAnticipoPorcentaje] = [
            x
            for x in to_edit_list
            if x.flete_anticipo_id == data.flete_anticipo_id
            and x.orden_carga_id == data.orden_carga_id
        ]
        to_edit = filtered_list[0] if len(filtered_list) > 0 else None
        if to_edit:
            edit_orden_carga_anticipo_porcentaje(
                to_edit.id, orden_carga_id, db, to_edit, data, modified_by
            )
