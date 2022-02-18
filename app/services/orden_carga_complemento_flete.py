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
