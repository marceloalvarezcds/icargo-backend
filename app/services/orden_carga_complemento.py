from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.models import OrdenCargaComplemento
from datetime import datetime

from app.models.orden_carga import OrdenCarga

from .orden_carga_anticipo_saldo import (
    update_orden_carga_anticipo_saldo_by_orden_carga_id,
)
from .moneda_cotizacion import get_cotizacion_moneda
from app.repositories.moneda import get_moneda_by_gestor_carga

def create_orden_carga_complemento(
    db: Session,
    data: schemas.OrdenCargaComplementoForm,
    modified_by: str,
) -> schemas.OrdenCargaComplemento:

    orden_carga = db.query(OrdenCarga).filter(OrdenCarga.id == data.orden_carga_id).first()
    if not orden_carga:
        raise HTTPException(status_code=404, detail="Orden de carga no encontrada.")

    orden_carga_anticipo = (
        db.query(OrdenCargaComplemento)
        .filter(OrdenCargaComplemento.orden_carga_id == data.orden_carga_id)
        .first()
    )

    moneda_gestor_carga = get_moneda_by_gestor_carga(db, orden_carga.gestor_carga_id)
    if not moneda_gestor_carga:
        raise HTTPException(status_code=404, detail="Moneda del gestor de carga no encontrada.")

    cotizacion_origen_gestor_carga = get_cotizacion_moneda(db, orden_carga_anticipo.remitente_moneda_id, orden_carga.gestor_carga_id)
    cotizacion_destino_gestor_carga_ml = get_cotizacion_moneda(db, moneda_gestor_carga.id, orden_carga.gestor_carga_id)

    cotizacion_origen_propietario = get_cotizacion_moneda(db, data.propietario_moneda_id, orden_carga.gestor_carga_id)

    remitente_monto_ml = data.remitente_monto * cotizacion_origen_gestor_carga.cotizacion_moneda / cotizacion_destino_gestor_carga_ml.cotizacion_moneda
    propietario_monto_ml= data.propietario_monto * cotizacion_origen_propietario.cotizacion_moneda / cotizacion_destino_gestor_carga_ml.cotizacion_moneda
    complemento = repositories.create_orden_carga_complemento(
        db,
        data,
        modified_by,
        remitente_monto_ml,
        propietario_monto_ml
    )
    update_orden_carga_anticipo_saldo_by_orden_carga_id(
        db, data.orden_carga_id, modified_by
    )
    return complemento


def get_orden_carga_complemento_by_id(db: Session, id: int) -> OrdenCargaComplemento:
    obj = repositories.get_orden_carga_complemento_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Complemento no encontrado")
    return obj


def edit_orden_carga_complemento(
    id: int,
    db: Session,
    data: schemas.OrdenCargaComplementoForm,
    modified_by: str,
) -> schemas.OrdenCargaComplemento:
    to_edit_obj = get_orden_carga_complemento_by_id(db, id)
    complemento = repositories.edit_orden_carga_complemento(
        to_edit_obj,
        db,
        data,
        modified_by,
    )
    update_orden_carga_anticipo_saldo_by_orden_carga_id(
        db, data.orden_carga_id, modified_by
    )
    return complemento


# def delete_orden_carga_complemento(
#     db: Session, id: int, modified_by: str
# ) -> schemas.OrdenCargaComplemento:
#     return repositories.delete_orden_carga_complemento(db, id, modified_by)

def delete_orden_carga_complemento(db: Session, id: int, modified_by: str) -> schemas.OrdenCargaComplemento:
    obj = db.query(OrdenCargaComplemento).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="OrdenCargaComplemento not found")

    # Actualizar los campos de auditoría
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()

    # Serializar los datos antes de eliminar
    result = schemas.OrdenCargaComplemento.from_orm(obj)

    # Eliminar el objeto
    db.delete(obj)
    db.commit()

    return result
