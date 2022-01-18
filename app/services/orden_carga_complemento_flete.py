from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories


def create_orden_carga_complemento_by_flete(
    db: Session,
    orden_carga: models.OrdenCarga,
    data: models.FleteComplemento,
    modified_by: str,
) -> models.OrdenCargaComplemento:
    if repositories.get_orden_carga_complemento_by(
        db,
        data.concepto_id,
        data.propietario_moneda_id,
        data.propietario_monto,
        data.remitente_moneda_id,
        data.remitente_monto,
        orden_carga.id,
        data.flete_id,
    ):
        raise HTTPException(status_code=409, detail="El Complemento ya existe")
    return repositories.create_orden_carga_complemento_by_flete(
        db,
        orden_carga,
        data,
        modified_by,
    )
