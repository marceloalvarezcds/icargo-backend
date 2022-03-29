from typing import List, Optional

from sqlalchemy import case, func, literal_column, null  # type: ignore
from sqlalchemy.engine.row import Row  # type: ignore
from sqlalchemy.orm import Query, Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore

from app.enums import EstadoEnum
from app.models import Liquidacion, Movimiento, TipoContraparte


def get_estado_cuenta_subquery(db: Session) -> Query:
    return (
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
                (Liquidacion.etapa == EstadoEnum.EN_PROCESO.value, Movimiento.monto),
                else_=literal_column("0"),
            ).label("en_proceso"),
            case(
                (Liquidacion.etapa == EstadoEnum.CONFIRMADO.value, Movimiento.monto),
                else_=literal_column("0"),
            ).label("confirmado"),
            case(
                (Liquidacion.etapa == EstadoEnum.FINALIZADO.value, Movimiento.monto),
                else_=literal_column("0"),
            ).label("finalizado"),
            case(
                (Movimiento.liquidacion_id == null(), literal_column("1")),
                else_=literal_column("0"),
            ).label("cantidad_pendiente"),
            case(
                (
                    Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                    literal_column("1"),
                ),
                else_=literal_column("0"),
            ).label("cantidad_en_proceso"),
            case(
                (
                    Liquidacion.etapa == EstadoEnum.CONFIRMADO.value,
                    literal_column("1"),
                ),
                else_=literal_column("0"),
            ).label("cantidad_confirmado"),
            case(
                (
                    Liquidacion.etapa == EstadoEnum.FINALIZADO.value,
                    literal_column("1"),
                ),
                else_=literal_column("0"),
            ).label("cantidad_finalizado"),
        )
        .join(Movimiento.tipo_contraparte)
        .outerjoin(Movimiento.liquidacion)
    )


def get_estado_cuenta_group_by_query(db: Session, table: Query) -> Query:
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
            func.sum(table.c.cantidad_pendiente).label("cantidad_pendiente"),
            func.sum(table.c.cantidad_en_proceso).label("cantidad_en_proceso"),
            func.sum(table.c.cantidad_confirmado).label("cantidad_confirmado"),
            func.sum(table.c.cantidad_finalizado).label("cantidad_finalizado"),
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
    )


def get_estado_cuenta_query(db: Session) -> Query:
    table = get_estado_cuenta_subquery(db).subquery()
    return get_estado_cuenta_group_by_query(db, table)


def get_estado_cuenta_list(db: Session) -> List[Row]:
    return get_estado_cuenta_query(db).all()


def get_estado_cuenta_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: int
) -> List[Row]:
    table = (
        get_estado_cuenta_subquery(db)
        .filter(Movimiento.gestor_carga_id == gestor_carga_id)
        .subquery()
    )
    return get_estado_cuenta_group_by_query(db, table).all()


def get_estado_cuenta_by_contraparte(
    db: Session,
    tipo_contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
) -> Optional[Row]:
    table = (
        get_estado_cuenta_subquery(db)
        .filter(
            and_(
                Movimiento.tipo_contraparte_id == tipo_contraparte_id,
                Movimiento.contraparte == contraparte,
                Movimiento.contraparte_numero_documento == contraparte_numero_documento,
            )
        )
        .subquery()
    )
    return get_estado_cuenta_group_by_query(db, table).first()
