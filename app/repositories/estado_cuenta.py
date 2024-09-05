from typing import List, Optional, Tuple

from sqlalchemy import case, exists, func, literal_column, null  # type: ignore
from sqlalchemy.engine.row import Row  # type: ignore
from sqlalchemy.orm import Query, Session  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore
from app.enums import EstadoEnum, TipoContraparteEnum, LiquidacionEstadoEnum
from app.models import (
    Chofer,
    Liquidacion,
    Movimiento,
    Propietario,
    Proveedor,
    Remitente,
    TipoContraparte,
    PuntoVenta,
    OrdenCargaAnticipoRetirado
)


def get_estado_cuenta_case_statement() -> Tuple:
    return (
        Movimiento.tipo_contraparte_id.label("tipo_contraparte_id"),
        TipoContraparte.descripcion.label("tipo_contraparte_descripcion"),
        Movimiento.gestor_carga_id.label("gestor_carga_id"),
        case(
            (
                and_(
                    Movimiento.liquidacion_id == null(),
                    Movimiento.estado == EstadoEnum.PENDIENTE.value,
                ),
                Movimiento.monto,
            ),
            else_=literal_column("0"),
        ).label("pendiente"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                    Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                ),
                Movimiento.monto,
            ),
            else_=literal_column("0"),
        ).label("en_proceso"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.CONFIRMADO.value,
                    Movimiento.estado == EstadoEnum.CONFIRMADO.value,
                ),
                Movimiento.monto,
            ),
            else_=literal_column("0"),
        ).label("confirmado"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.FINALIZADO.value,
                    Movimiento.estado == EstadoEnum.FINALIZADO.value,
                ),
                Movimiento.monto,
            ),
            else_=literal_column("0"),
        ).label("finalizado"),
        case(
            (
                and_(
                    Movimiento.liquidacion_id == null(),
                    Movimiento.estado == EstadoEnum.PENDIENTE.value,
                ),
                literal_column("1"),
            ),
            else_=literal_column("0"),
        ).label("cantidad_pendiente"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                    Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                ),
                literal_column("1"),
            ),
            else_=literal_column("0"),
        ).label("cantidad_en_proceso"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.CONFIRMADO.value,
                    Movimiento.estado == EstadoEnum.CONFIRMADO.value,
                ),
                literal_column("1"),
            ),
            else_=literal_column("0"),
        ).label("cantidad_confirmado"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.FINALIZADO.value,
                    Movimiento.estado == EstadoEnum.FINALIZADO.value,
                ),
                literal_column("1"),
            ),
            else_=literal_column("0"),
        ).label("cantidad_finalizado"),
    )


def get_estado_cuenta_case_statement_new() -> Tuple:
    return (
        Movimiento.tipo_contraparte_id.label("tipo_contraparte_id"),
        TipoContraparte.descripcion.label("tipo_contraparte_descripcion"),
        Movimiento.gestor_carga_id.label("gestor_carga_id"),
        *get_cols_estado_cuenta_case_statement(),
    )


def get_estado_cuenta_chofer(db: Session) -> Query:
    return (
        db.query(
            Movimiento.chofer_id.label("contraparte_id"),
            Chofer.nombre.label("contraparte"),
            Chofer.numero_documento.label("contraparte_numero_documento"),
            *get_estado_cuenta_case_statement_new(),
        )
        .join(Movimiento.chofer)
        .join(Movimiento.tipo_contraparte)
        .outerjoin(Movimiento.liquidacion)
    )


def get_estado_cuenta_propietario(db: Session) -> Query:
    return (
        db.query(
            Movimiento.propietario_id.label("contraparte_id"),
            Propietario.nombre.label("contraparte"),
            Propietario.ruc.label("contraparte_numero_documento"),
            *get_estado_cuenta_case_statement_new(),
        )
        .join(Movimiento.propietario)
        .join(Movimiento.tipo_contraparte)
        .outerjoin(Movimiento.liquidacion)
    )


def get_estado_cuenta_proveedor(db: Session) -> Query:
    return (
        db.query(
            Movimiento.proveedor_id.label("contraparte_id"),
            Proveedor.nombre.label("contraparte"),
            Proveedor.numero_documento.label("contraparte_numero_documento"),
            *get_estado_cuenta_case_statement_new(),
        )
        .join(Movimiento.proveedor)
        .filter(~exists().where(PuntoVenta.proveedor_id == Proveedor.id))
        .join(Movimiento.tipo_contraparte)
        .outerjoin(Movimiento.liquidacion)
    )


def get_estado_cuenta_proveedor_pdv(db: Session) -> Query:
    return (
        db.query(
            PuntoVenta.id.label("contraparte_id"),
            PuntoVenta.nombre.label("contraparte"),
            PuntoVenta.numero_documento.label("contraparte_numero_documento"),
            *get_estado_cuenta_case_statement_new(),
        )
        .join(Movimiento.proveedor)
        .join(Movimiento.anticipo)
        .join(OrdenCargaAnticipoRetirado.punto_venta)
        .join(Movimiento.tipo_contraparte)
        .outerjoin(Movimiento.liquidacion)
    )


def get_estado_cuenta_remitente(db: Session) -> Query:
    return (
        db.query(
            Movimiento.remitente_id.label("contraparte_id"),
            Remitente.nombre.label("contraparte"),
            Remitente.numero_documento.label("contraparte_numero_documento"),
            *get_estado_cuenta_case_statement_new(),
        )
        .join(Movimiento.remitente)
        .join(Movimiento.tipo_contraparte)
        .outerjoin(Movimiento.liquidacion)
    )


def get_estado_cuenta_otro(db: Session) -> Query:
    return (
        db.query(
            Movimiento.tipo_contraparte_id.label("contraparte_id"),
            Movimiento.contraparte.label("contraparte"),
            Movimiento.contraparte_numero_documento.label(
                "contraparte_numero_documento"
            ),
            *get_estado_cuenta_case_statement_new(),
        )
        .join(Movimiento.tipo_contraparte)
        .outerjoin(Movimiento.liquidacion)
        .filter(TipoContraparte.descripcion == TipoContraparteEnum.OTRO.value)
    )


def get_estado_cuenta_subquery(db: Session) -> Query:
    chofer = get_estado_cuenta_chofer(db)
    propietario = get_estado_cuenta_propietario(db)
    proveedor = get_estado_cuenta_proveedor(db)
    proveedorPdv = get_estado_cuenta_proveedor_pdv(db)
    remitente = get_estado_cuenta_remitente(db)
    otro = get_estado_cuenta_otro(db)
    return chofer.union_all(propietario, proveedor, proveedorPdv, remitente, otro)


def get_estado_cuenta_group_by_query(db: Session, table: Query) -> Query:
    return (
        db.query(
            table.c.contraparte_id.label("contraparte_id"),
            table.c.contraparte.label("contraparte"),
            table.c.contraparte_numero_documento.label("contraparte_numero_documento"),
            table.c.tipo_contraparte_id.label("tipo_contraparte_id"),
            table.c.tipo_contraparte_descripcion.label("tipo_contraparte_descripcion"),
            table.c.gestor_carga_id.label("gestor_carga_id"),
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
            table.c.contraparte_id,
            table.c.contraparte,
            table.c.contraparte_numero_documento,
            table.c.tipo_contraparte_id,
            table.c.tipo_contraparte_descripcion,
            table.c.gestor_carga_id,
        )
        .order_by(
            table.c.tipo_contraparte_descripcion,
            table.c.contraparte
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


def get_estado_cuenta_by_contraparte_and_tipo(
    db: Session,
    contraparte_id: int,
    tipo_contraparte_id: int,
) -> Optional[Row]:
    subquery = get_estado_cuenta_subquery(db).subquery()
    table = (
        db.query(subquery)
        .filter(
            subquery.c.contraparte_id == contraparte_id,
            subquery.c.tipo_contraparte_id == tipo_contraparte_id,
        )
        .subquery()
    )
    return get_estado_cuenta_group_by_query(db, table).first()


def get_estado_cuenta_by_contraparte_tipo_otro(
    db: Session,
    contraparte: str,
    contraparte_numero_documento: str,
    tipo_contraparte_id: int,
) -> Optional[Row]:
    subquery = get_estado_cuenta_subquery(db).subquery()
    table = (
        db.query(subquery)
        .filter(
            subquery.c.contraparte == contraparte,
            subquery.c.contraparte_numero_documento == contraparte_numero_documento,
            subquery.c.tipo_contraparte_id == tipo_contraparte_id,
        )
        .subquery()
    )
    return get_estado_cuenta_group_by_query(db, table).first()


def get_cols_estado_cuenta_case_statement() -> Tuple:
    return (
        case(
            (
                and_(
                    Movimiento.liquidacion_id == null(),
                    Movimiento.estado == EstadoEnum.PENDIENTE.value,
                ),
                Movimiento.monto,
            ),
            else_=literal_column("0"),
        ).label("pendiente"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                    Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                ),
                Movimiento.monto,
            ),
            else_=literal_column("0"),
        ).label("en_proceso"),
        case(
            (
                or_(
                    and_(
                        Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                        Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                    ),
                    and_(
                        Liquidacion.etapa == EstadoEnum.PENDIENTE.value,
                        Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                    ),
                    and_(
                        Liquidacion.etapa == EstadoEnum.CONFIRMADO.value,
                        Movimiento.estado == EstadoEnum.CONFIRMADO.value,
                    )
                ),
                Movimiento.monto,
            ),
            else_=literal_column("0"),
        ).label("confirmado"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.FINALIZADO.value,
                    Movimiento.estado == EstadoEnum.FINALIZADO.value,
                ),
                Movimiento.monto,
            ),
            else_=literal_column("0"),
        ).label("finalizado"),
        case(
            (
                and_(
                    Movimiento.liquidacion_id == null(),
                    Movimiento.estado == EstadoEnum.PENDIENTE.value,
                ),
                literal_column("1"),
            ),
            else_=literal_column("0"),
        ).label("cantidad_pendiente"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                    Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                ),
                literal_column("1"),
            ),
            else_=literal_column("0"),
        ).label("cantidad_en_proceso"),
        case(
            (
                or_(
                    and_(
                        Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                        Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                    ),
                    and_(
                        Liquidacion.etapa == EstadoEnum.PENDIENTE.value,
                        Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                    ),
                    and_(
                        Liquidacion.etapa == EstadoEnum.CONFIRMADO.value,
                        Movimiento.estado == EstadoEnum.CONFIRMADO.value,
                    )
                ),
                literal_column("1"),
            ),
            else_=literal_column("0"),
        ).label("cantidad_confirmado"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.FINALIZADO.value,
                    Movimiento.estado == EstadoEnum.FINALIZADO.value,
                ),
                literal_column("1"),
            ),
            else_=literal_column("0"),
        ).label("cantidad_finalizado"),
    )


def get_estado_cuenta_movimiento() -> Tuple:
    return (
        case(
            (
                and_(
                    Movimiento.liquidacion_id == null(),
                    Movimiento.estado == EstadoEnum.PENDIENTE.value,
                ),
                Movimiento.monto,
            ),
            else_=literal_column("0"),
        ).label("pendiente"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                    Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                ),
                Movimiento.monto,
            ),
            else_=literal_column("0"),
        ).label("en_proceso"),
        case(
            (
                or_(
                    and_(
                        Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                        Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                    ),
                    and_(
                        Liquidacion.etapa == EstadoEnum.PENDIENTE.value,
                        Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                    ),
                    and_(
                        Liquidacion.etapa == EstadoEnum.CONFIRMADO.value,
                        Movimiento.estado == EstadoEnum.CONFIRMADO.value,
                    )
                ),
                Movimiento.monto,
            ),
            else_=literal_column("0"),
        ).label("confirmado"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.FINALIZADO.value,
                    Movimiento.estado == EstadoEnum.FINALIZADO.value,
                ),
                Movimiento.monto,
            ),
            else_=literal_column("0"),
        ).label("finalizado"),
    )
