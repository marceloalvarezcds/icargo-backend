from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories


def create_orden_carga_descuento_by_flete(
    db: Session,
    orden_carga: models.OrdenCarga,
    data: models.FleteDescuento,
    modified_by: str,
) -> models.OrdenCargaDescuento:
    return repositories.create_orden_carga_descuento_by_flete(
        db,
        orden_carga,
        data,
        modified_by,
    )
