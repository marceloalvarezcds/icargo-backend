from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.models import OrdenCargaDescuento
from datetime import datetime

def create_orden_carga_descuento(
    db: Session,
    data: schemas.OrdenCargaDescuentoForm,
    modified_by: str,
) -> schemas.OrdenCargaDescuento:
    return repositories.create_orden_carga_descuento(
        db,
        data,
        modified_by,
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