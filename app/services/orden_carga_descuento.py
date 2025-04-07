from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.models import OrdenCargaDescuento
from datetime import datetime

from app.schemas.orden_carga import OrdenCarga
from .moneda_cotizacion import get_cotizacion_moneda
from app.repositories.moneda import get_moneda_by_gestor_carga

def create_orden_carga_descuento(
    db: Session,
    data: schemas.OrdenCargaDescuentoForm,
    modified_by: str,
) -> schemas.OrdenCargaDescuento:

    orden_carga = db.query(OrdenCarga).filter(OrdenCarga.id == data.orden_carga_id).first()
    if not orden_carga:
        raise HTTPException(status_code=404, detail="Orden de carga no encontrada.")

    orden_carga_anticipo = (
        db.query(OrdenCargaDescuento)
        .filter(OrdenCargaDescuento.orden_carga_id == data.orden_carga_id)
        .first()
    )

    moneda_gestor_carga = get_moneda_by_gestor_carga(db, orden_carga.gestor_carga_id)
    if not moneda_gestor_carga:
        raise HTTPException(status_code=404, detail="Moneda del gestor de carga no encontrada.")

    cotizacion_origen_gestor_carga = get_cotizacion_moneda(db, orden_carga_anticipo.proveedor_moneda_id, orden_carga.gestor_carga_id)
    cotizacion_destino_gestor_carga_ml = get_cotizacion_moneda(db, moneda_gestor_carga.id, orden_carga.gestor_carga_id)

    cotizacion_origen_propietario = get_cotizacion_moneda(db, data.propietario_moneda_id, orden_carga.gestor_carga_id)

    proveedor_monto_ml= data.propietario_monto * cotizacion_origen_propietario.cotizacion_moneda / cotizacion_destino_gestor_carga_ml.cotizacion_moneda
    propietario_monto_ml = data.remitente_monto * cotizacion_origen_gestor_carga.cotizacion_moneda / cotizacion_destino_gestor_carga_ml.cotizacion_moneda

    return repositories.create_orden_carga_descuento(
        db,
        data,
        modified_by,
        proveedor_monto_ml,
        propietario_monto_ml,
    )


def get_orden_carga_descuento_by_id(db: Session, id: int) -> OrdenCargaDescuento:
    obj = repositories.get_orden_carga_descuento_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Descuento no encontrado")
    return obj


def edit_orden_carga_descuento(
    id: int,
    db: Session,
    data: schemas.OrdenCargaDescuentoForm,
    modified_by: str,
) -> schemas.OrdenCargaDescuento:
    to_edit_obj = get_orden_carga_descuento_by_id(db, id)
    return repositories.edit_orden_carga_descuento(
        to_edit_obj,
        db,
        data,
        modified_by,
    )


# def delete_orden_carga_descuento(
#     db: Session, id: int, modified_by: str
# ) -> schemas.OrdenCargaDescuento:
#     return repositories.delete_orden_carga_descuento(db, id, modified_by)

def delete_orden_carga_descuento(db: Session, id: int, modified_by: str) -> schemas.OrdenCargaDescuento:
    obj = db.query(OrdenCargaDescuento).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="OrdenCargaDescuento not found")

    # Actualizar los campos de auditoría
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()

    # Serializar los datos antes de eliminar
    result = schemas.OrdenCargaDescuento.from_orm(obj)

    # Eliminar el objeto
    db.delete(obj)
    db.commit()

    return result
