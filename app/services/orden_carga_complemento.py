from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas
from app.models import OrdenCargaComplemento
from datetime import datetime

from app.models.orden_carga import OrdenCarga

from .orden_carga_anticipo_saldo import (
    update_orden_carga_anticipo_saldo_by_orden_carga_id,
)

def create_orden_carga_complemento(
    db: Session,
    data: schemas.OrdenCargaComplementoForm,
    modified_by: str,
) -> schemas.OrdenCargaComplemento:

    complemento = repositories.create_orden_carga_complemento(
        db,
        data,
        modified_by,
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
