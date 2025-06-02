from decimal import Decimal
from typing import List, Optional

from app.models.combinacion import Combinacion
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
from app.models.orden_carga_anticipo_porcentaje import OrdenCargaAnticipoPorcentaje

from .flete_anticipo import get_flete_anticipo_by_id, get_flete_anticipo_by_flete_and_tipo
from .orden_carga_anticipo_porcentaje_create import (
    create_orden_carga_anticipo_porcentaje,
    get_orden_carga_anticipo_porcentaje_by,
)

from .moneda_cotizacion import get_cotizacion_moneda
from app.repositories.moneda import get_moneda_by_gestor_carga


def create_orden_carga_anticipo_saldo(
    db: Session,
    data: schemas.OrdenCargaAnticipoSaldoForm,
    modified_by: str,
) -> OrdenCargaAnticipoSaldo:

    existing_anticipos = repositories.get_orden_carga_anticipo_saldo_by_orden_carga_id(
        db, data.orden_carga_id
    )
    sorted_anticipos = sorted(existing_anticipos, key=lambda a: a.flete_anticipo_id)

    # Recuperar tipo_insumo_id del FleteAnticipo actual
    flete_anticipo_actual = (
        db.query(FleteAnticipo)
        .filter(FleteAnticipo.id == data.flete_anticipo_id)
        .first()
    )
    if not flete_anticipo_actual:
        raise ValueError(f"No se encontró un FleteAnticipo con ID {data.flete_anticipo_id}")

    tipo_insumo_actual = flete_anticipo_actual.tipo_insumo_id

    saldo_actualizado = data.saldo
    # saldo_actualizado_ml = data.saldo_ml
    for anticipo in sorted_anticipos:

        if anticipo.flete_anticipo_id != data.flete_anticipo_id:
            # Recuperar tipo_insumo_id del FleteAnticipo relacionado al anticipo
            tipo_insumo_id = (
                anticipo.flete_anticipo.tipo_insumo_id
                if anticipo.flete_anticipo
                else None
            )
            # Restar según el tipo de insumo
            if tipo_insumo_id is None and tipo_insumo_actual is None:  # Efectivo
                saldo_actualizado -= anticipo.total_retirado
            elif tipo_insumo_id == 1 and tipo_insumo_actual == 1:  # Combustible
                saldo_actualizado -= anticipo.total_retirado
            elif tipo_insumo_id == 2 and tipo_insumo_actual == 2:  # Lubricantes
                saldo_actualizado -= anticipo.total_retirado

    return repositories.create_orden_carga_anticipo_saldo(
        db,
        data,
        saldo_actualizado,
        modified_by
    )


def get_flete_anticipo_by_orden_carga(
    orden_carga: OrdenCarga,
) -> Optional[FleteAnticipo]:
    complemento_list: List[FleteAnticipo] = orden_carga.flete_anticipos
    for item in complemento_list:
        if item.tipo_descripcion == enums.TipoAnticipoEnum.EFECTIVO.value:
            return item
    return None


def get_flete_anticipo_by_orden_carga_insumos(
    orden_carga: OrdenCarga,
) -> Optional[FleteAnticipo]:
    complemento_list: List[FleteAnticipo] = orden_carga.flete_anticipos
    for item in complemento_list:
        if item.tipo_descripcion == enums.TipoAnticipoEnum.INSUMOS.value:
            return item
    return None

# se agrega acá para evitar importación circular
def get_orden_carga_by_id(db: Session, id: int) -> OrdenCarga:
    obj = repositories.get_orden_carga_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Orden de carga no encontrada")
    return obj


def get_orden_carga_by_combinacion_id(db: Session, combinacion_id: int)  -> OrdenCarga:
    obj = repositories.get_combinacion_by_orden_carga(db, combinacion_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Combinacion no encontrada")
    return obj


def get_orden_carga_anticipo_saldo_by_id(
    db: Session, id: int
) -> OrdenCargaAnticipoSaldo:
    obj = repositories.get_orden_carga_anticipo_saldo_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Anticipo no encontrado")
    return obj


def get_saldos_by_orden_carga(db, orden_carga_id):
    orden_carga = db.query(OrdenCarga).filter(OrdenCarga.id == orden_carga_id).first()

    if not orden_carga:
        raise Exception("Orden de carga no encontrada")

    flete_id = orden_carga.flete_id
    saldos = db.query(OrdenCargaAnticipoSaldo).join(FleteAnticipo).filter(
        OrdenCargaAnticipoSaldo.orden_carga_id == orden_carga_id,
        FleteAnticipo.flete_id == flete_id
    ).all()

    return saldos

def get_flete_anticipo_id_by_flete_id_and_orden_carga_id(
    db: Session,
    flete_id: int,
    orden_carga_id: int
) -> int:
    # Buscar el anticipo relacionado con flete_id y orden_carga_id
    flete_anticipo = db.query(FleteAnticipo).filter(
        FleteAnticipo.flete_id == flete_id,
        FleteAnticipo.orden_carga_id == orden_carga_id
    ).first()


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
    camion_monto_disponible: Optional[
        Decimal
    ] = orden_carga.camion_monto_anticipo_disponible
    return (
        camion_monto_disponible
        if camion_monto_disponible and camion_monto_disponible < oc_monto_disponible
        else oc_monto_disponible
    )


def get_total_complemento(complementos: List[OrdenCargaComplemento], es_efectivo: bool):
    if es_efectivo:
        return sum((x.propietario_monto_ml or 0) for x in complementos if x.anticipado)
    else:
        return 0


def edit_orden_carga_anticipo_saldo(
    id: int,
    db: Session,
    data: schemas.OrdenCargaAnticipoSaldoForm,
    modified_by: str,
) -> Optional[OrdenCargaAnticipoSaldo]:
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
    moneda_gestor_carga = get_moneda_by_gestor_carga(db, orden_carga.gestor_carga_id)
    cotizacion_condicion_origen = get_cotizacion_moneda(db, orden_carga.condicion_propietario_moneda_id, orden_carga.gestor_carga_id)
    cotizacion_destino = get_cotizacion_moneda(db, moneda_gestor_carga.id, orden_carga.gestor_carga_id)
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
    monto_retirado_ml = (
    monto_retirado * cotizacion_condicion_origen.cotizacion_moneda / cotizacion_destino.cotizacion_moneda
    if monto_retirado
    else Decimal(0)
    )
    monto_retirado_ml = (monto_retirado_ml)
    camion_monto_disponible = (
        camion_limite - camion_monto_retirado - monto_retirado
        if camion_limite
        else None
    )

    exists = repositories.get_orden_carga_anticipo_saldo_by(
        db, flete_anticipo_id, orden_carga_id
    )
    porcentaje_anticipo: Optional[OrdenCargaAnticipoPorcentaje] = (
        exists.orden_carga_anticipo_porcentaje if exists else None
    )
    porcentaje: Optional[Decimal] = (
        porcentaje_anticipo.porcentaje
        if porcentaje_anticipo
        else flete_anticipo.porcentaje
    )

    oc_limite = (
        orden_carga.flete_proyectado_ml * (porcentaje / Decimal(100))
        if porcentaje
        else Decimal(0)
    )
    oc_limite_ml = (
        orden_carga.flete_proyectado_ml * cotizacion_condicion_origen.cotizacion_moneda / cotizacion_destino.cotizacion_moneda * (porcentaje / Decimal(100))
        if porcentaje
        else Decimal(0)
    )
    oc_monto_retirado = monto_retirado + (exists.total_retirado if exists else Decimal(0))

    oc_monto_disponible = oc_limite + total_complemento - oc_monto_retirado
    saldo = (
        camion_monto_disponible
        if camion_monto_disponible and camion_monto_disponible < oc_monto_disponible
        else oc_monto_disponible
    )

    # if saldo < 0:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Saldo insuficiente para realizar el retiro.",
    #     )

    porcentaje_anticipo = get_orden_carga_anticipo_porcentaje_by(
        db, flete_anticipo_id, orden_carga_id
    )
    if not porcentaje_anticipo:
        porcentaje_anticipo = create_orden_carga_anticipo_porcentaje(
            db,
            orden_carga_id,
            flete_anticipo,
            modified_by,
        )
    if exists:
        schema = schemas.OrdenCargaAnticipoSaldoForm(
            flete_anticipo_id=flete_anticipo_id,
            orden_carga_id=orden_carga_id,
            orden_carga_anticipo_porcentaje_id=porcentaje_anticipo.id,
            total_anticipo=oc_limite,
            total_anticipo_ml=oc_limite_ml,
            total_complemento=total_complemento,
            total_retirado=oc_monto_retirado,
            saldo=saldo,
        )
        anticipo_saldo = edit_orden_carga_anticipo_saldo(
            exists.id,
            db,
            schema,
            modified_by,
        )
    else:
        schema = schemas.OrdenCargaAnticipoSaldoForm(
            flete_anticipo_id=flete_anticipo_id,
            orden_carga_id=orden_carga_id,
            orden_carga_anticipo_porcentaje_id=porcentaje_anticipo.id,
            total_anticipo=oc_limite,
            total_anticipo_ml=oc_limite_ml,
            total_complemento=total_complemento,
            total_retirado=oc_monto_retirado,
            saldo=saldo,
        )
        anticipo_saldo = create_orden_carga_anticipo_saldo(
            db,
            schema,
            modified_by,
        )
    if anticipo_saldo:
        # Se actualiza el porcentaje mínimo de la tabla OC anticipo porcentaje
        flete_proyectado = (
            orden_carga.flete_proyectado if orden_carga.flete_proyectado > 0 else 1
        )
        porcentaje_minimo = (oc_monto_retirado * 100) / flete_proyectado
        porcentaje_minimo = (
            flete_anticipo.porcentaje
            if flete_anticipo.porcentaje is not None and porcentaje_minimo > flete_anticipo.porcentaje
            else porcentaje_minimo
        )
        porcentaje_anticipo.porcentaje_minimo = porcentaje_minimo
        db.commit()
    return anticipo_saldo


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

    if flete_anticipo.tipo_descripcion == enums.TipoAnticipoEnum.INSUMOS.value:
        monto_retirado = data.monto_mon_local - last_monto_retirado
    else:
        monto_retirado = data.monto_mon_local - last_monto_retirado

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
