from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories

from .orden_carga_anticipo_saldo import (
    update_orden_carga_anticipo_saldo_by_orden_carga_id,
)


def create_orden_carga_complemento_by_flete(
    db: Session,
    orden_carga: models.OrdenCarga,
    data: models.FleteComplemento,
    modified_by: str,
) -> models.OrdenCargaComplemento:
    complemento = repositories.create_orden_carga_complemento_by_flete(
        db,
        orden_carga,
        data,
        modified_by,
    )
    update_orden_carga_anticipo_saldo_by_orden_carga_id(db, orden_carga.id, modified_by)
    return complemento


def change_flete_create_orden_carga_complemento_by_flete(
    db: Session,
    orden_carga: models.OrdenCarga,
    data: models.FleteComplemento,
    modified_by: str,
) -> models.OrdenCargaComplemento:
    complemento_existente = db.query(models.OrdenCargaComplemento).filter(
        models.OrdenCargaComplemento.flete_id == data.flete_id,
        models.OrdenCargaComplemento.orden_carga_id == orden_carga.id,
    ).first()

    if complemento_existente:

        complemento_existente.concepto_id = data.concepto_id
        complemento_existente.detalle = data.detalle
        complemento_existente.habilitar_cobro_remitente = data.habilitar_cobro_remitente
        complemento_existente.anticipado = data.anticipado
        complemento_existente.propietario_monto = data.propietario_monto
        complemento_existente.propietario_monto_ml = data.propietario_monto_ml
        complemento_existente.propietario_moneda_id = data.propietario_moneda_id
        complemento_existente.remitente_monto = data.remitente_monto
        complemento_existente.remitente_monto_ml = data.remitente_monto_ml
        complemento_existente.remitente_moneda_id = data.remitente_moneda_id

        db.commit()
        db.refresh(complemento_existente)

        return complemento_existente
    else:
        complemento = repositories.create_orden_carga_complemento_by_flete(
            db,
            orden_carga,
            data,
            modified_by,
        )

        update_orden_carga_anticipo_saldo_by_orden_carga_id(db, orden_carga.id, modified_by)
        return complemento
