from typing import List, Optional

from sqlalchemy import func  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore

from app.enums import MovimientoEstadoEnum
from app.models import Movimiento, TipoContraparte
from app.schemas import Contraparte


def get_contraparte_by_contraparte_and_tipo_contraparte_id(
    db: Session, contraparte: str, tipo_contraparte_id: int
) -> Optional[Contraparte]:
    return (
        db.query(
            Movimiento.id,
            Movimiento.contraparte,
            Movimiento.contraparte_numero_documento,
            Movimiento.tipo_contraparte_id,
            TipoContraparte.descripcion.label("tipo_contraparte_descripcion"),
        )
        .distinct(Movimiento.contraparte)
        .join(Movimiento.tipo_contraparte)
        .filter(
            and_(
                Movimiento.contraparte == contraparte,
                Movimiento.tipo_contraparte_id == tipo_contraparte_id,
                Movimiento.estado != MovimientoEstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            Movimiento.contraparte,
            Movimiento.contraparte_numero_documento,
            Movimiento.tipo_contraparte_id,
        )
        .first()
    )


def get_contraparte_list_by_tipo_contraparte_id(
    db: Session, tipo_contraparte_id: int
) -> List[Contraparte]:
    return (
        db.query(
            Movimiento.id,
            Movimiento.contraparte,
            Movimiento.contraparte_numero_documento,
            func.concat(
                Movimiento.contraparte,
                " - ",
                Movimiento.contraparte_numero_documento,
            ).label("info"),
            Movimiento.tipo_contraparte_id,
            TipoContraparte.descripcion.label("tipo_contraparte_descripcion"),
        )
        .distinct(Movimiento.contraparte)
        .join(Movimiento.tipo_contraparte)
        .filter(
            and_(
                Movimiento.tipo_contraparte_id == tipo_contraparte_id,
                Movimiento.estado != MovimientoEstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            Movimiento.contraparte,
            Movimiento.contraparte_numero_documento,
            Movimiento.tipo_contraparte_id,
        )
        .all()
    )
