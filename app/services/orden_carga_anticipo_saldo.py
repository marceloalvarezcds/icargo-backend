from decimal import Decimal
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import enums, repositories, schemas
from app.models import (
    Camion,
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
    modified_by: str,
) -> Decimal:
    exists: Optional[
        schemas.OrdenCargaAnticipoSaldo
    ] = repositories.get_orden_carga_anticipo_saldo_by(
        db, flete_anticipo_id, orden_carga_id
    )
    orden_carga = get_orden_carga_by_id(db, orden_carga_id)
    if not exists:
        flete_anticipo = repositories.get_flete_anticipo_by_id(db, flete_anticipo_id)
        if flete_anticipo is None:
            flete_anticipo = get_flete_anticipo_by_orden_carga(orden_carga)
        if flete_anticipo:
            total_complemento = get_total_complemento(
                orden_carga.complementos,
                flete_anticipo.tipo_descripcion
                == enums.TipoAnticipoEnum.EFECTIVO.value,
            )
            exists = update_orden_carga_anticipo_saldo(
                db,
                flete_anticipo,
                orden_carga,
                Decimal(0),
                total_complemento,
                modified_by,
            )
    oc_monto_disponible: Decimal = exists.saldo if exists else Decimal(0)
    camion_monto_disponible = orden_carga.camion_monto_anticipo_disponible
    return (
        camion_monto_disponible
        if camion_monto_disponible and camion_monto_disponible < oc_monto_disponible
        else oc_monto_disponible
    )


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
    camion: Camion = orden_carga.camion
    camion_limite: Optional[Decimal] = orden_carga.camion_limite_monto_anticipos
    total_anticipos_retirados_en_estado_pendiente_o_en_proceso = (
        repositories.get_total_anticipo_retirado_by_camion_id(db, camion.id)
    )
    camion_monto_retirado: Decimal = (
        total_anticipos_retirados_en_estado_pendiente_o_en_proceso
        if total_anticipos_retirados_en_estado_pendiente_o_en_proceso
        else Decimal(0)
    )
    camion_monto_disponible = (
        camion_limite - camion_monto_retirado - monto_retirado
        if camion_limite
        else None
    )
    exists = repositories.get_orden_carga_anticipo_saldo_by(
        db, flete_anticipo_id, orden_carga_id
    )
    oc_limite = (
        orden_carga.flete_proyectado * (flete_anticipo.porcentaje / Decimal(100))
        if flete_anticipo.porcentaje
        else Decimal(0)
    )
    oc_monto_retirado = monto_retirado + (
        exists.total_retirado if exists else Decimal(0)
    )
    oc_monto_disponible = oc_limite + total_complemento - oc_monto_retirado
    saldo = (
        camion_monto_disponible
        if camion_monto_disponible and camion_monto_disponible < oc_monto_disponible
        else oc_monto_disponible
    )
    if exists:
        schema = schemas.OrdenCargaAnticipoSaldoForm(
            flete_anticipo_id=flete_anticipo_id,
            orden_carga_id=orden_carga_id,
            total_anticipo=oc_limite,
            total_complemento=total_complemento,
            total_retirado=oc_monto_retirado,
            saldo=saldo,
        )
        return edit_orden_carga_anticipo_saldo(
            exists.id,
            db,
            schema,
            modified_by,
        )
    schema = schemas.OrdenCargaAnticipoSaldoForm(
        flete_anticipo_id=flete_anticipo_id,
        orden_carga_id=orden_carga_id,
        total_anticipo=oc_limite,
        total_complemento=total_complemento,
        total_retirado=oc_monto_retirado,
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
    total_complemento = (
        get_total_complemento(
            orden_carga.complementos,
            flete_anticipo.tipo_descripcion == enums.TipoAnticipoEnum.EFECTIVO.value,
        )
        if flete_anticipo
        else 0
    )
    if flete_anticipo:
        return update_orden_carga_anticipo_saldo(
            db, flete_anticipo, orden_carga, Decimal(0), total_complemento, modified_by
        )
    return None
