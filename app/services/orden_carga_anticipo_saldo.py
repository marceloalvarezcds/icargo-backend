from decimal import Decimal
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import enums, repositories, schemas
from app.models import (
    FleteAnticipo,
    OrdenCarga,
    OrdenCargaAnticipoSaldo,
    OrdenCargaComplemento,
)

from .flete_anticipo import get_flete_anticipo_by_id


def create_orden_carga_anticipo_saldo(
    db: Session,
    data: schemas.OrdenCargaAnticipoSaldoForm,
    modified_by: str,
) -> schemas.OrdenCargaAnticipoSaldo:
    return repositories.create_orden_carga_anticipo_saldo(
        db,
        data,
        modified_by,
    )


def get_flete_anticipo_by_orden_carga(
    orden_carga: OrdenCarga,
) -> Optional[FleteAnticipo]:
    complemento_list: List[FleteAnticipo] = orden_carga.flete_anticipos
    for item in complemento_list:
        if item.tipo_descripcion == enums.TipoAnticipoEnum.EFECTIVO.value:
            return item
    return None


# se agrega acá para evitar importación circular
def get_orden_carga_by_id(db: Session, id: int) -> OrdenCarga:
    obj = repositories.get_orden_carga_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Orden de carga no encontrada")
    return obj


def get_orden_carga_anticipo_saldo_by_id(
    db: Session, id: int
) -> OrdenCargaAnticipoSaldo:
    obj = repositories.get_orden_carga_anticipo_saldo_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Anticipo no encontrado")
    return obj


def get_saldo_anticipo_by_flete_anticipo_id_and_orden_carga_id(
    db: Session,
    flete_anticipo_id: int,
    orden_carga_id: int,
) -> Decimal:
    exists = repositories.get_orden_carga_anticipo_saldo_by(
        db, flete_anticipo_id, orden_carga_id
    )
    if exists:
        return exists.saldo
    else:
        flete_anticipo = get_flete_anticipo_by_id(db, flete_anticipo_id)
        orden_carga = get_orden_carga_by_id(db, orden_carga_id)
        total_complemento = get_total_complemento(
            orden_carga.complementos,
            flete_anticipo.tipo_descripcion == enums.TipoAnticipoEnum.EFECTIVO.value,
        )
        total_anticipo = (
            orden_carga.flete_proyectado * (flete_anticipo.porcentaje / Decimal(100))
            if flete_anticipo.porcentaje
            else 0
        )
        return total_anticipo + total_complemento


def get_total_complemento(complementos: List[OrdenCargaComplemento], es_efectivo: bool):
    if es_efectivo:
        return sum(x.propietario_monto for x in complementos if x.anticipado)
    else:
        return 0


def edit_orden_carga_anticipo_saldo(
    id: int,
    db: Session,
    data: schemas.OrdenCargaAnticipoSaldoForm,
    modified_by: str,
) -> Optional[schemas.OrdenCargaAnticipoSaldo]:
    to_edit_obj = get_orden_carga_anticipo_saldo_by_id(db, id)
    return repositories.edit_orden_carga_anticipo_saldo(
        to_edit_obj,
        db,
        data,
        modified_by,
    )


def delete_orden_carga_anticipo_saldo(
    db: Session, id: int, modified_by: str
) -> schemas.OrdenCargaAnticipoSaldo:
    return repositories.delete_orden_carga_anticipo_saldo(db, id, modified_by)


def update_orden_carga_anticipo_saldo(
    db: Session,
    flete_anticipo: FleteAnticipo,
    orden_carga: OrdenCarga,
    monto_retirado: Decimal,
    total_complemento: Decimal,
    modified_by: str,
) -> Optional[schemas.OrdenCargaAnticipoSaldo]:
    flete_anticipo_id = flete_anticipo.id
    orden_carga_id = orden_carga.id
    exists = repositories.get_orden_carga_anticipo_saldo_by(
        db, flete_anticipo_id, orden_carga_id
    )
    total_anticipo = (
        orden_carga.flete_proyectado * (flete_anticipo.porcentaje / Decimal(100))
        if flete_anticipo.porcentaje
        else 0
    )
    total_retirado = monto_retirado
    total_disponible = total_anticipo + total_complemento
    if exists:
        total_retirado += exists.total_retirado
        saldo = total_disponible - total_retirado
        schema = schemas.OrdenCargaAnticipoSaldoForm(
            flete_anticipo_id=flete_anticipo_id,
            orden_carga_id=orden_carga_id,
            total_anticipo=total_anticipo,
            total_complemento=total_complemento,
            total_retirado=total_retirado,
            saldo=saldo,
        )
        return edit_orden_carga_anticipo_saldo(
            exists.id,
            db,
            schema,
            modified_by,
        )
    saldo = total_disponible - total_retirado
    schema = schemas.OrdenCargaAnticipoSaldoForm(
        flete_anticipo_id=flete_anticipo_id,
        orden_carga_id=orden_carga_id,
        total_anticipo=total_anticipo,
        total_complemento=total_complemento,
        total_retirado=total_retirado,
        saldo=saldo,
    )
    return create_orden_carga_anticipo_saldo(
        db,
        schema,
        modified_by,
    )


def update_orden_carga_anticipo_saldo_by_form(
    db: Session,
    data: schemas.OrdenCargaAnticipoRetiradoForm,
    last_monto_retirado: Decimal,
    modified_by: str,
) -> Optional[schemas.OrdenCargaAnticipoSaldo]:
    flete_anticipo = get_flete_anticipo_by_id(db, data.flete_anticipo_id)
    orden_carga = get_orden_carga_by_id(db, data.orden_carga_id)
    total_complemento = get_total_complemento(
        orden_carga.complementos,
        flete_anticipo.tipo_descripcion == enums.TipoAnticipoEnum.EFECTIVO.value,
    )
    monto_retirado = data.monto_retirado - last_monto_retirado
    return update_orden_carga_anticipo_saldo(
        db,
        flete_anticipo,
        orden_carga,
        monto_retirado,
        total_complemento,
        modified_by,
    )


def update_orden_carga_anticipo_saldo_by_orden_carga_id(
    db: Session,
    orden_carga_id: int,
    modified_by: str,
) -> Optional[schemas.OrdenCargaAnticipoSaldo]:
    orden_carga = get_orden_carga_by_id(db, orden_carga_id)
    flete_anticipo = get_flete_anticipo_by_orden_carga(orden_carga)
    total_complemento = get_total_complemento(orden_carga.complementos, True)
    if flete_anticipo:
        return update_orden_carga_anticipo_saldo(
            db, flete_anticipo, orden_carga, Decimal(0), total_complemento, modified_by
        )
    return None
