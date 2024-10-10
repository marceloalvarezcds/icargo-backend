from typing import List, Optional, Tuple

from sqlalchemy import case, exists, func, literal_column, null, desc, nullsfirst  # type: ignore
from sqlalchemy.engine.row import Row  # type: ignore
from sqlalchemy.orm import Query, Session  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore

from app.enums import EstadoEnum, TipoContraparteEnum
from app.models import (
    Chofer,
    Instrumento,
    Liquidacion,
    Movimiento,
    Propietario,
    Proveedor,
    Remitente,
    TipoContraparte,
    PuntoVenta,
    OrdenCargaAnticipoRetirado,
    TipoInstrumento,
    Factura
)
from app.schemas import MovimientoEstadoCuenta
from app.repositories.movimiento import get_query_movimientos_by_contraparte_and_gestor_carga_id

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
        literal_column('0').label('punto_venta_id'),
        null().label('contraparte_pdv'),
        null().label('contraparte_numero_documento_pdv'),
        Movimiento.tipo_contraparte_id.label("tipo_contraparte_id"),
        TipoContraparte.descripcion.label("tipo_contraparte_descripcion"),
        Movimiento.gestor_carga_id.label("gestor_carga_id"),
        *get_cols_estado_cuenta_case_statement(),
    )


def get_estado_cuenta_liquidacion_case_statement_new() -> Tuple:
    return (
        literal_column('0').label('punto_venta_id'),
        null().label('contraparte_pdv'),
        null().label('contraparte_numero_documento_pdv'),
        Liquidacion.tipo_contraparte_id.label("tipo_contraparte_id"),
        TipoContraparte.descripcion.label("tipo_contraparte_descripcion"),
        Liquidacion.gestor_carga_id.label("gestor_carga_id"),
        *get_cols_estado_cuenta_liquidacion_case_statement(),
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
    )


def get_estado_cuenta_chofer_liquidacion(db: Session) -> Query:
    return (
        db.query(
            Liquidacion.chofer_id.label("contraparte_id"),
            Chofer.nombre.label("contraparte"),
            Chofer.numero_documento.label("contraparte_numero_documento"),
            *get_estado_cuenta_liquidacion_case_statement_new(),
        )
        .join(Liquidacion.chofer)
        .join(Liquidacion.tipo_contraparte)
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
    )


def get_estado_cuenta_propietario_liquidacion(db: Session) -> Query:
    return (
        db.query(
            Liquidacion.propietario_id.label("contraparte_id"),
            Propietario.nombre.label("contraparte"),
            Propietario.ruc.label("contraparte_numero_documento"),
            *get_estado_cuenta_liquidacion_case_statement_new(),
        )
        .join(Liquidacion.propietario)
        .join(Liquidacion.tipo_contraparte)
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
    )


def get_estado_cuenta_proveedor_liquidacion(db: Session) -> Query:
    return (
        db.query(
            Liquidacion.proveedor_id.label("contraparte_id"),
            Proveedor.nombre.label("contraparte"),
            Proveedor.numero_documento.label("contraparte_numero_documento"),
            *get_estado_cuenta_liquidacion_case_statement_new(),
        )
        .join(Liquidacion.proveedor)
        .filter(~exists().where(PuntoVenta.proveedor_id == Proveedor.id))
        .join(Liquidacion.tipo_contraparte)
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
    )


def get_estado_cuenta_remitente_liquidacion(db: Session) -> Query:
    return (
        db.query(
            Liquidacion.remitente_id.label("contraparte_id"),
            Remitente.nombre.label("contraparte"),
            Remitente.numero_documento.label("contraparte_numero_documento"),
            *get_estado_cuenta_liquidacion_case_statement_new(),
        )
        .join(Liquidacion.remitente)
        .join(Liquidacion.tipo_contraparte)
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


def get_estado_cuenta_proveedor_pdv(db: Session) -> Query:
    return (
        db.query(
            Movimiento.proveedor_id.label("contraparte_id"),
            Proveedor.nombre.label("contraparte"),
            Proveedor.numero_documento.label("contraparte_numero_documento"),
            PuntoVenta.id.label("punto_venta_id"),
            PuntoVenta.nombre.label("contraparte_pdv"),
            PuntoVenta.numero_documento.label("contraparte_numero_documento_pdv"),
            Movimiento.tipo_contraparte_id.label("tipo_contraparte_id"),
            TipoContraparte.descripcion.label("tipo_contraparte_descripcion") + " - PDV",
            Movimiento.gestor_carga_id.label("gestor_carga_id"),
            *get_cols_estado_cuenta_case_statement(),
        )
        .join(Movimiento.proveedor)
        .join(Movimiento.anticipo)
        .join(OrdenCargaAnticipoRetirado.punto_venta)
        .join(Movimiento.tipo_contraparte)
    )


def get_estado_cuenta_proveedor_pdv_liquidacion(db: Session) -> Query:
    return (
        db.query(
            Liquidacion.proveedor_id.label("contraparte_id"),
            Proveedor.nombre.label("contraparte"),
            Proveedor.numero_documento.label("contraparte_numero_documento"),
            Liquidacion.punto_venta_id.label("punto_venta_id"),
            Liquidacion.contraparte.label("contraparte_pdv"),
            Liquidacion.contraparte_numero_documento.label("contraparte_numero_documento_pdv"),
            Liquidacion.tipo_contraparte_id.label("tipo_contraparte_id"),
            TipoContraparte.descripcion.label("tipo_contraparte_descripcion") + " - PDV",
            Liquidacion.gestor_carga_id.label("gestor_carga_id"),
            *get_cols_estado_cuenta_liquidacion_case_statement(),
        )
        .join(Liquidacion.proveedor)
        .join(Liquidacion.tipo_contraparte)
        .filter(Liquidacion.punto_venta_id != null())
    )


def get_estado_cuenta_subquery(db: Session) -> Query:
    chofer = get_estado_cuenta_chofer(db)
    choferLiquidacion = get_estado_cuenta_chofer_liquidacion(db)
    propietario = get_estado_cuenta_propietario(db)
    propietarioLiquidacion = get_estado_cuenta_propietario_liquidacion(db)
    proveedor = get_estado_cuenta_proveedor(db)
    proveedorLiquidacion = get_estado_cuenta_proveedor_liquidacion(db)
    proveedorPdv = get_estado_cuenta_proveedor_pdv(db)
    proveedorPdvLiquidacion = get_estado_cuenta_proveedor_pdv_liquidacion(db)
    remitente = get_estado_cuenta_remitente(db)
    remitenteLiquidacion = get_estado_cuenta_remitente_liquidacion(db)
    #otro = get_estado_cuenta_otro(db)
    return chofer.union_all(choferLiquidacion, propietario, propietarioLiquidacion,
            proveedor, proveedorLiquidacion, proveedorPdv, proveedorPdvLiquidacion, remitente, remitenteLiquidacion)
    # return proveedorPdv.union_all( chofer, proveedor, remitente)
    # return chofer.union_all(proveedor, proveedorPdv)


def get_estado_cuenta_group_by_query(db: Session, table: Query) -> Query:
    return (
        db.query(
            table.c.contraparte_id.label("contraparte_id"),
            table.c.contraparte.label("contraparte"),
            table.c.contraparte_numero_documento.label("contraparte_numero_documento"),
            table.c.punto_venta_id.label("punto_venta_id"),
            table.c.contraparte_pdv.label("contraparte_pdv"),
            table.c.contraparte_numero_documento_pdv.label("contraparte_numero_documento_pdv"),
            table.c.tipo_contraparte_id.label("tipo_contraparte_id"),
            table.c.tipo_contraparte_descripcion.label("tipo_contraparte_descripcion"),
            table.c.gestor_carga_id.label("gestor_carga_id"),
            func.sum(table.c.pendiente).label("pendiente"),
            func.sum(table.c.en_proceso).label("en_proceso"),
            func.sum(table.c.confirmado).label("confirmado"),
            func.sum(table.c.saldo_pendiente).label("saldo_pendiente"),
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
            table.c.punto_venta_id,
            table.c.contraparte_pdv,
            table.c.contraparte_numero_documento_pdv,
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
    punto_venta_id: int = None
) -> Optional[Row]:
    subquery = get_estado_cuenta_subquery(db).subquery()
    table = (
        db.query(subquery)
        .filter(
            subquery.c.contraparte_id == contraparte_id,
            subquery.c.tipo_contraparte_id == tipo_contraparte_id,
            or_(
                subquery.c.punto_venta_id == punto_venta_id,
                punto_venta_id == None
            )
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
                #and_(
                    # Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                    Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                #),
                Movimiento.monto,
            ),
            else_=literal_column("0"),
        ).label("en_proceso"),
        case(
            (
                or_(
                    #and_(
                        #Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                        Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                    #),
                    #and_(
                        #Liquidacion.etapa == EstadoEnum.PENDIENTE.value,
                    #    Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                    #),
                    #and_(
                        #Liquidacion.etapa == EstadoEnum.CONFIRMADO.value,
                        Movimiento.estado == EstadoEnum.CONFIRMADO.value,
                        Movimiento.estado == EstadoEnum.FINALIZADO.value,
                    #)
                ),
                Movimiento.monto,
            ),
            else_=literal_column("0"),
        ).label("confirmado"),
         case(
             (
                 Movimiento.estado == EstadoEnum.FINALIZADO.value,
                 Movimiento.monto,
             ),
             else_=literal_column("0"),
         ).label("saldo_pendiente"),
        #Movimiento.monto.label("saldo_pendiente"),
        literal_column("0").label("finalizado"),
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
                #and_(
                #    Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                    Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                #),
                literal_column("1"),
            ),
            else_=literal_column("0"),
        ).label("cantidad_en_proceso"),
        case(
            (
                or_(
                    #and_(
                    #    Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                        Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                    #),
                    #and_(
                    #    Liquidacion.etapa == EstadoEnum.PENDIENTE.value,
                    #    Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                    #),
                    #and_(
                    #    Liquidacion.etapa == EstadoEnum.CONFIRMADO.value,
                        Movimiento.estado == EstadoEnum.CONFIRMADO.value,
                    #)
                ),
                literal_column("1"),
            ),
            else_=literal_column("0"),
        ).label("cantidad_confirmado"),
        literal_column("0").label("cantidad_finalizado"),
    )


def get_cols_estado_cuenta_liquidacion_case_statement() -> Tuple:
    return (
        literal_column("0").label("pendiente"),
        literal_column("0").label("en_proceso"),
        literal_column("0").label("confirmado"),
        literal_column("0").label("saldo_pendiente"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.FINALIZADO.value,
                ),
                Liquidacion.pago_cobro*-1,
            ),
            else_=literal_column("0"),
        ).label("finalizado"),
        literal_column("0").label("cantidad_pendiente"),
        literal_column("0").label("cantidad_en_proceso"),
        literal_column("0").label("cantidad_confirmado"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.FINALIZADO.value,
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


def get_query_instrumentos_by_contraparte_and_gestor_carga_id(
    db: Session,
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    gestor_carga_id: int,
    punto_venta_id: Optional[int]
) -> Query:

    query = db.query(
            null().label('movimiento_id'),
            Liquidacion.id,
            Liquidacion.created_at,
            TipoInstrumento.descripcion,
            literal_column("'Pago/Cobro'").label("tipo_movimiento_concepto"),
            Liquidacion.es_pago_cobro.label("detalle"),
            Liquidacion.id.label("nro_documento_relacionado"),
            Factura.numero_factura,
            Instrumento.estado,
            literal_column("''").label("estado_liquidacion"),
            literal_column("0"),
            literal_column("0"),
            literal_column("0"),
            case(
                (
                    Instrumento.credito == 0,
                    ((Instrumento.debito*-1) + Instrumento.provision),
                ),
                else_= (Instrumento.credito + Instrumento.provision)
            ).label("finalizado"),
        )\
        .join(Liquidacion.instrumentos)\
        .join(Instrumento.tipo_instrumento)\
        .outerjoin(Liquidacion.facturas)\
        .filter(
            and_(
                Liquidacion.tipo_contraparte_id == tipo_contraparte_id,
                or_(
                    Liquidacion.propietario_id == contraparte_id,
                    Liquidacion.remitente_id == contraparte_id,
                    Liquidacion.proveedor_id == contraparte_id,
                    and_(
                        Liquidacion.contraparte == contraparte,
                        Liquidacion.contraparte_numero_documento
                        == contraparte_numero_documento,
                    ),
                    Liquidacion.chofer_id == contraparte_id,
                ),
                or_(
                    Liquidacion.punto_venta_id == punto_venta_id,
                    punto_venta_id == None
                ),
                Liquidacion.gestor_carga_id == gestor_carga_id,
            )
        )

    return query


def nuevo_endpint(
    db: Session,
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    gestor_carga_id: int,
    punto_venta_id: Optional[int]
    ) -> List[Row]:

    query_movimientos = get_query_movimientos_by_contraparte_and_gestor_carga_id(
        db, tipo_contraparte_id, contraparte_id, contraparte, contraparte_numero_documento,
        gestor_carga_id, punto_venta_id
    )
    query_instrumentos = get_query_instrumentos_by_contraparte_and_gestor_carga_id(
        db, tipo_contraparte_id, contraparte_id, contraparte, contraparte_numero_documento,
        gestor_carga_id, punto_venta_id
    )

    table = query_movimientos.union_all(query_instrumentos).subquery()

    # columnas que se retorna
    query = db.query(
        table.c.movimiento_id.label("movimiento_id"),
        table.c.liquidacion_id.label("liquidacion_id"),
        table.c.fecha.label("fecha"),
        table.c.tipo_cuenta_descripcion.label("tipo_cuenta_descripcion"),
        table.c.tipo_movimiento_concepto.label("tipo_movimiento_concepto"),
        table.c.nro_documento_relacionado.label("nro_documento_relacionado"),
        table.c.detalle.label("detalle"),
        table.c.info.label("info"),
        table.c.estado.label("estado"),
        table.c.estado_liquidacion.label("estado_liquidacion"),
        table.c.pendiente.label("pendiente"),
        table.c.en_proceso.label("en_proceso"),
        table.c.confirmado.label("confirmado"),
        table.c.finalizado.label("finalizado"),
        ).order_by(nullsfirst(desc(table.c.liquidacion_id)), desc(table.c.movimiento_id))

    return query.all()


# saldo = confirmados - pagos cobros
# suma de liquidaciones - suma de instrumentos
def get_saldo_cuenta_contraparte(
    db: Session,
    gestor_carga_id: int,
    tipo_contraparte_id: int,
    contraparte_id: int,
    punto_venta_id: Optional[int]
    ) -> List[Row]:

    #  obtenemos la contraparte id por tipo contraparte
    tipo_contraparte = db.query(TipoContraparte)\
                    .filter(TipoContraparte.id == tipo_contraparte_id)\
                    .first()

    # segun tipo contraparte filtramos
    query = db.query(
                func.sum(
                    case(
                        (
                            #and_(
                                Liquidacion.etapa != EstadoEnum.FINALIZADO.value,
                            #),
                            Liquidacion.pago_cobro,
                        ),
                        else_=literal_column("0"),
                    )
                ).label("confirmado"),
                func.sum(
                    case(
                        (
                            #and_(
                                # Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                                Liquidacion.etapa == EstadoEnum.FINALIZADO.value,
                            #),
                            Liquidacion.pago_cobro,
                        ),
                        else_=literal_column("0"),
                    )
                ).label("finalizado"),
            )\
            .filter(
                Liquidacion.tipo_contraparte_id == tipo_contraparte_id
            )

    if TipoContraparteEnum.PROVEEDOR.value == tipo_contraparte.descripcion:
        query = query.filter(
            Liquidacion.proveedor_id == contraparte_id
        )
        if punto_venta_id is not None:
            query = query.filter(
               Liquidacion.punto_venta_id == punto_venta_id
            )

    if TipoContraparteEnum.REMITENTE.value == tipo_contraparte.descripcion:
        query = query.filter(
            Liquidacion.remitente_id == contraparte_id
        )

    if TipoContraparteEnum.PROPIETARIO.value == tipo_contraparte.descripcion:
        query = query.filter(
            Liquidacion.propietario_id == contraparte_id
        )

    if TipoContraparteEnum.CHOFER.value == tipo_contraparte.descripcion:
        query = query.filter(
            Liquidacion.chofer_id == contraparte_id
        )

    return query.first()

