from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import FleteAnticipo, OrdenCargaAnticipoPorcentaje
from app.schemas import OrdenCargaAnticipoPorcentajeForm

from . import generic_service as service


def get_orden_carga_anticipo_porcentaje_by(
    db: Session, flete_anticipo_id: int, orden_carga_id: int
) -> Optional[OrdenCargaAnticipoPorcentaje]:
    obj: Optional[OrdenCargaAnticipoPorcentaje] = service.get_by_unique_columns_or_none(
        OrdenCargaAnticipoPorcentaje,
        db,
        False,
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
    porcentaje = flete_anticipo.porcentaje if flete_anticipo.porcentaje else Decimal(0)
    data = OrdenCargaAnticipoPorcentajeForm(
        flete_anticipo_id=flete_anticipo.id,
        orden_carga_id=orden_carga_id,
        porcentaje=porcentaje,
        porcentaje_minimo=Decimal(0),
    )
    try:
        obj: OrdenCargaAnticipoPorcentaje = service.create_oc(
            OrdenCargaAnticipoPorcentaje,
            db,
            data,
            modified_by,
            None,
            flete_anticipo_id=flete_anticipo.id,
            orden_carga_id=orden_carga_id,
        )
        return obj
    except Exception as e:
        # Manejo silencioso del error
        print(f"Conflicto detectado: {str(e)}")  # Solo para depuración
        return None  # O maneja el retorno según tu lógica
