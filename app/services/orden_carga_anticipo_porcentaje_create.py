from decimal import Decimal

from sqlalchemy.orm import Session  # type: ignore

from app.models import FleteAnticipo, OrdenCargaAnticipoPorcentaje
from app.schemas import OrdenCargaAnticipoPorcentajeForm

from . import generic_service as service


def get_orden_carga_anticipo_porcentaje_by(
    db: Session, flete_anticipo_id: int, orden_carga_id: int
) -> OrdenCargaAnticipoPorcentaje:
    obj: OrdenCargaAnticipoPorcentaje = service.get_by_unique_columns(
        OrdenCargaAnticipoPorcentaje,
        db,
        flete_anticipo_id=flete_anticipo_id,
        orden_carga_id=orden_carga_id,
    )
    return obj


def create_orden_carga_anticipo_porcentaje(
    db: Session,
    orden_carga_id: int,
    flete_anticipo: FleteAnticipo,
    modified_by: str,
) -> OrdenCargaAnticipoPorcentaje:
    data = OrdenCargaAnticipoPorcentajeForm(
        flete_anticipo_id=flete_anticipo.id,
        orden_carga_id=orden_carga_id,
        porcentaje=flete_anticipo.porcentaje,
        porcentaje_minimo=Decimal(0),
    )
    obj: OrdenCargaAnticipoPorcentaje = service.create(
        OrdenCargaAnticipoPorcentaje,
        db,
        data,
        modified_by,
        "El Porcentaje de Anticipo",
        flete_anticipo_id=flete_anticipo.id,
        orden_carga_id=orden_carga_id,
    )
    return obj
