from typing import List

from sqlalchemy import case, func, literal_column, null  # type: ignore
from sqlalchemy.engine.row import Row  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import Liquidacion, Movimiento, TipoContraparte


def get_estado_cuenta_list(db: Session) -> List[Row]:
    table = (
        db.query(
            Movimiento.contraparte,
            Movimiento.contraparte_numero_documento,
            Movimiento.tipo_contraparte_id,
            TipoContraparte.descripcion.label("tipo_contraparte_descripcion"),
            case(
                (Movimiento.liquidacion_id == null(), Movimiento.monto),
                else_=literal_column("0"),
            ).label("pendiente"),
            case(
                (Liquidacion.estado == EstadoEnum.EN_PROCESO.value, Movimiento.monto),
                else_=literal_column("0"),
            ).label("en_proceso"),
            case(
                (Liquidacion.estado == EstadoEnum.CONFIRMADO.value, Movimiento.monto),
                else_=literal_column("0"),
            ).label("confirmado"),
            case(
                (Liquidacion.estado == EstadoEnum.FINALIZADO.value, Movimiento.monto),
                else_=literal_column("0"),
            ).label("finalizado"),
        )
        .join(Movimiento.tipo_contraparte)
        .outerjoin(Movimiento.liquidacion)
        .subquery()
    )
    return (
        db.query(
            table.c.contraparte,
            table.c.contraparte_numero_documento,
            table.c.tipo_contraparte_id,
            table.c.tipo_contraparte_descripcion,
            func.sum(table.c.pendiente).label("pendiente"),
            func.sum(table.c.en_proceso).label("en_proceso"),
            func.sum(table.c.confirmado).label("confirmado"),
            func.sum(table.c.finalizado).label("finalizado"),
        )
        .group_by(
            table.c.contraparte,
            table.c.contraparte_numero_documento,
            table.c.tipo_contraparte_id,
            table.c.tipo_contraparte_descripcion,
        )
        .order_by(
            table.c.contraparte,
            table.c.contraparte_numero_documento,
            table.c.tipo_contraparte_id,
            table.c.tipo_contraparte_descripcion,
        )
        .all()
    )


def get_estado_cuenta_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: int
) -> List[Row]:
    table = (
        db.query(
            Movimiento.contraparte,
            Movimiento.contraparte_numero_documento,
            Movimiento.tipo_contraparte_id,
            TipoContraparte.descripcion.label("tipo_contraparte_descripcion"),
            case(
                (Movimiento.liquidacion_id == null(), Movimiento.monto),
                else_=literal_column("0"),
            ).label("pendiente"),
            case(
                (Liquidacion.estado == EstadoEnum.EN_PROCESO.value, Movimiento.monto),
                else_=literal_column("0"),
            ).label("en_proceso"),
            case(
                (Liquidacion.estado == EstadoEnum.CONFIRMADO.value, Movimiento.monto),
                else_=literal_column("0"),
            ).label("confirmado"),
            case(
                (Liquidacion.estado == EstadoEnum.FINALIZADO.value, Movimiento.monto),
                else_=literal_column("0"),
            ).label("finalizado"),
        )
        .join(Movimiento.tipo_contraparte)
        .outerjoin(Movimiento.liquidacion)
        .filter(Movimiento.gestor_carga_id == gestor_carga_id)
        .subquery()
    )
    return (
        db.query(
            table.c.contraparte,
            table.c.contraparte_numero_documento,
            table.c.tipo_contraparte_id,
            table.c.tipo_contraparte_descripcion,
            func.sum(table.c.pendiente).label("pendiente"),
            func.sum(table.c.en_proceso).label("en_proceso"),
            func.sum(table.c.confirmado).label("confirmado"),
            func.sum(table.c.finalizado).label("finalizado"),
        )
        .group_by(
            table.c.contraparte,
            table.c.contraparte_numero_documento,
            table.c.tipo_contraparte_id,
            table.c.tipo_contraparte_descripcion,
        )
        .order_by(
            table.c.contraparte,
            table.c.contraparte_numero_documento,
            table.c.tipo_contraparte_id,
            table.c.tipo_contraparte_descripcion,
        )
        .all()
    )
