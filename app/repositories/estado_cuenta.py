from typing import List, Optional, Tuple

from sqlalchemy import case, exists, func, literal_column, null, desc, nullsfirst
from sqlalchemy.sql.functions import concat  # type: ignore
from sqlalchemy.engine.row import Row  # type: ignore
from sqlalchemy.orm import Query, Session, aliased  # type: ignore
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
    Factura,
    Provision,
    InstrumentoVia,
    MonedaCotizacion,
    Moneda
)
from app.repositories.movimiento import get_query_movimientos_by_contraparte_and_gestor_carga_id
from app.repositories.provision import get_query_provisiones_by_contraparte_and_gestor_carga_id
from app.logger import logger

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


def get_estado_cuenta_case_statement_new(mon_local_id:int) -> Tuple:
    return (
        literal_column('0').label('punto_venta_id'),
        null().label('contraparte_pdv'),
        null().label('contraparte_numero_documento_pdv'),
        Movimiento.tipo_contraparte_id.label("tipo_contraparte_id"),
        TipoContraparte.descripcion.label("tipo_contraparte_descripcion"),
        Movimiento.gestor_carga_id.label("gestor_carga_id"),
        Movimiento.linea_movimiento.label("tipo_flujo"),
        *get_cols_estado_cuenta_case_statement(mon_local_id),
    )


def get_estado_cuenta_liquidacion_case_statement_new() -> Tuple:
    return (
        literal_column('0').label('punto_venta_id'),
        null().label('contraparte_pdv'),
        null().label('contraparte_numero_documento_pdv'),
        Liquidacion.tipo_contraparte_id.label("tipo_contraparte_id"),
        TipoContraparte.descripcion.label("tipo_contraparte_descripcion"),
        Liquidacion.gestor_carga_id.label("gestor_carga_id"),
        Liquidacion.tipo_mov_liquidacion.label("tipo_flujo"),
        *get_cols_estado_cuenta_liquidacion_case_statement(),
    )


def get_max_date_cotizacion(db: Session,mon_local_id:int):
    aliasCotizacion = aliased(MonedaCotizacion)

    return (
        db.query(func.max(aliasCotizacion.fecha))
        .filter(
            aliasCotizacion.moneda_origen_id == mon_local_id,
            aliasCotizacion.moneda_destino_id == Movimiento.moneda_id,  # Filtrar por gestor de carga específico
            aliasCotizacion.estado == EstadoEnum.ACTIVO.value,
            aliasCotizacion.gestor_carga_id == Movimiento.gestor_carga_id,
        )
    )


def get_estado_cuenta_chofer(db: Session, mon_local_id:int) -> Query:
    return (
        db.query(
            Movimiento.chofer_id.label("contraparte_id"),
            Chofer.nombre.label("contraparte"),
            null().label("contraparte_alias"),
            Chofer.numero_documento.label("contraparte_numero_documento"),
            literal_column('false').label("es_pdv"),
            *get_estado_cuenta_case_statement_new(mon_local_id),
        )
        .join(Movimiento.chofer)
        .join(Movimiento.tipo_contraparte)
        # .outerjoin(
        #     MonedaCotizacion,
        #     and_(
        #         MonedaCotizacion.moneda_origen_id == 1,
        #         MonedaCotizacion.moneda_destino_id == Movimiento.moneda_id,  # Filtrar por gestor de carga específico
        #         MonedaCotizacion.estado == EstadoEnum.ACTIVO.value,
        #         MonedaCotizacion.gestor_carga_id == Movimiento.gestor_carga_id,
        #         MonedaCotizacion.fecha == (
        #             get_max_date_cotizacion(db, 1).subquery()
        #         )
        #     )
        # )
    )


def get_estado_cuenta_chofer_liquidacion(db: Session) -> Query:
    return (
        db.query(
            Liquidacion.chofer_id.label("contraparte_id"),
            Chofer.nombre.label("contraparte"),
            null().label("contraparte_alias"),
            Chofer.numero_documento.label("contraparte_numero_documento"),
            literal_column('false').label("es_pdv"),
            *get_estado_cuenta_liquidacion_case_statement_new(),
        )
        .join(Liquidacion.chofer)
        .join(Liquidacion.tipo_contraparte)
        .filter(Liquidacion.estado != 'Cancelado')
    )


def get_estado_cuenta_propietario(db: Session, mon_local_id:int) -> Query:
    return (
        db.query(
            Movimiento.propietario_id.label("contraparte_id"),
            Propietario.nombre.label("contraparte"),
            null().label("contraparte_alias"),
            Propietario.ruc.label("contraparte_numero_documento"),
            literal_column('false').label("es_pdv"),
            *get_estado_cuenta_case_statement_new(mon_local_id),
        )
        .join(Movimiento.propietario)
        .join(Movimiento.tipo_contraparte)
        # .outerjoin(
        #     MonedaCotizacion,
        #     and_(
        #         MonedaCotizacion.moneda_origen_id == mon_local_id,
        #         MonedaCotizacion.moneda_destino_id == Movimiento.moneda_id,  # Filtrar por gestor de carga específico
        #         MonedaCotizacion.estado == EstadoEnum.ACTIVO.value,
        #         MonedaCotizacion.gestor_carga_id == Movimiento.gestor_carga_id,
        #         MonedaCotizacion.fecha == (
        #             get_max_date_cotizacion(db, mon_local_id).subquery()
        #         )
        #     )
        # )
    )


def get_estado_cuenta_propietario_liquidacion(db: Session) -> Query:
    return (
        db.query(
            Liquidacion.propietario_id.label("contraparte_id"),
            Propietario.nombre.label("contraparte"),
            null().label("contraparte_alias"),
            Propietario.ruc.label("contraparte_numero_documento"),
            literal_column('false').label("es_pdv"),
            *get_estado_cuenta_liquidacion_case_statement_new(),
        )
        .join(Liquidacion.propietario)
        .join(Liquidacion.tipo_contraparte)
        .filter(Liquidacion.estado != 'Cancelado')
    )


def get_estado_cuenta_proveedor(db: Session, mon_local_id:int) -> Query:
    return (
        db.query(
            Movimiento.proveedor_id.label("contraparte_id"),
            concat(Proveedor.nombre).label("contraparte"),
            concat(Proveedor.nombre_corto).label("contraparte_alias"),
            Proveedor.numero_documento.label("contraparte_numero_documento"),
            exists().where(PuntoVenta.proveedor_id == Proveedor.id).label("es_pdv"),
            *get_estado_cuenta_case_statement_new(mon_local_id),
        )
        .join(Movimiento.proveedor)
        #.filter(~exists().where(PuntoVenta.proveedor_id == Proveedor.id))
        .join(Movimiento.tipo_contraparte)
        # .outerjoin(
        #     MonedaCotizacion,
        #     and_(
        #         MonedaCotizacion.moneda_origen_id == mon_local_id,
        #         MonedaCotizacion.moneda_destino_id == Movimiento.moneda_id,  # Filtrar por gestor de carga específico
        #         MonedaCotizacion.estado == EstadoEnum.ACTIVO.value,
        #         MonedaCotizacion.gestor_carga_id == Movimiento.gestor_carga_id,
        #         MonedaCotizacion.fecha == (
        #             get_max_date_cotizacion(db, mon_local_id).subquery()
        #         )
        #     )
        # )
    )


def get_estado_cuenta_proveedor_liquidacion(db: Session) -> Query:
    return (
        db.query(
            Liquidacion.proveedor_id.label("contraparte_id"),
            concat(Proveedor.nombre).label("contraparte"),
            concat(Proveedor.nombre_corto).label("contraparte_alias"),
            Proveedor.numero_documento.label("contraparte_numero_documento"),
            exists().where(PuntoVenta.proveedor_id == Proveedor.id).label("es_pdv"),
            *get_estado_cuenta_liquidacion_case_statement_new(),
        )
        .join(Liquidacion.proveedor)
        #.filter(~exists().where(PuntoVenta.proveedor_id == Proveedor.id))
        .join(Liquidacion.tipo_contraparte)
        .filter(Liquidacion.estado != 'Cancelado')
    )


def get_estado_cuenta_remitente(db: Session, mon_local_id:int) -> Query:
    return (
        db.query(
            Movimiento.remitente_id.label("contraparte_id"),
            concat(Remitente.nombre).label("contraparte"),
            null().label("contraparte_alias"),
            Remitente.numero_documento.label("contraparte_numero_documento"),
            literal_column('false').label("es_pdv"),
            *get_estado_cuenta_case_statement_new(mon_local_id),
        )
        .join(Movimiento.remitente)
        .join(Movimiento.tipo_contraparte)
        # .outerjoin(
        #     MonedaCotizacion,
        #     and_(
        #         MonedaCotizacion.moneda_origen_id == mon_local_id,
        #         MonedaCotizacion.moneda_destino_id == Movimiento.moneda_id,  # Filtrar por gestor de carga específico
        #         MonedaCotizacion.estado == EstadoEnum.ACTIVO.value,
        #         MonedaCotizacion.gestor_carga_id == Movimiento.gestor_carga_id,
        #         MonedaCotizacion.fecha == (
        #             get_max_date_cotizacion(db, mon_local_id).subquery()
        #         )
        #     )
        # )
    )


def get_estado_cuenta_remitente_liquidacion(db: Session) -> Query:
    return (
        db.query(
            Liquidacion.remitente_id.label("contraparte_id"),
            concat(Remitente.nombre).label("contraparte"),
            null().label("contraparte_alias"),
            Remitente.numero_documento.label("contraparte_numero_documento"),
            literal_column('false').label("es_pdv"),
            *get_estado_cuenta_liquidacion_case_statement_new(),
        )
        .join(Liquidacion.remitente)
        .join(Liquidacion.tipo_contraparte)
        .filter(Liquidacion.estado != 'Cancelado')
    )


def get_estado_cuenta_otro(db: Session, mon_local_id:int) -> Query:
    return (
        db.query(
            Movimiento.tipo_contraparte_id.label("contraparte_id"),
            Movimiento.contraparte.label("contraparte"),
            null().label("contraparte_alias"),
            Movimiento.contraparte_numero_documento.label(
                "contraparte_numero_documento"
            ),
            literal_column('false').label("es_pdv"),
            *get_estado_cuenta_case_statement_new(mon_local_id),
        )
        .join(Movimiento.tipo_contraparte)
        # .outerjoin(Movimiento.liquidacion)
        .filter(TipoContraparte.descripcion == TipoContraparteEnum.OTRO.value)
    )


def get_estado_cuenta_otro_liquidacion(db: Session) -> Query:
    return (
        db.query(
            Liquidacion.tipo_contraparte_id.label("contraparte_id"),
            Liquidacion.contraparte.label("contraparte"),
            null().label("contraparte_alias"),
            Liquidacion.contraparte_numero_documento.label("contraparte_numero_documento"),
            literal_column('false').label("es_pdv"),
            *get_estado_cuenta_liquidacion_case_statement_new(),
        )
        .join(Liquidacion.tipo_contraparte)
        .filter(TipoContraparte.descripcion == TipoContraparteEnum.OTRO.value)
        .filter(Liquidacion.estado != 'Cancelado')
    )


def get_estado_cuenta_proveedor_pdv(db: Session) -> Query:
    return (
        db.query(
            Movimiento.proveedor_id.label("contraparte_id"),
            Proveedor.nombre.label("contraparte"),
            Proveedor.nombre_corto.label("contraparte_alias"),
            Proveedor.numero_documento.label("contraparte_numero_documento"),
            PuntoVenta.id.label("punto_venta_id"),
            concat(PuntoVenta.nombre_corto).label("contraparte_pdv"),
            PuntoVenta.numero_documento.label("contraparte_numero_documento_pdv"),
            Movimiento.tipo_contraparte_id.label("tipo_contraparte_id"),
            #TipoContraparte.descripcion.label("tipo_contraparte_descripcion") + " - PDV",
            literal_column("'PUNTO DE VENTA'").label("tipo_contraparte_descripcion"),
            Movimiento.gestor_carga_id.label("gestor_carga_id"),
            Movimiento.linea_movimiento.label("tipo_flujo"),
            *get_cols_estado_cuenta_case_statement(),
        )
        .join(Movimiento.proveedor)
        .join(Movimiento.tipo_contraparte)
        .outerjoin(Movimiento.anticipo)
        .outerjoin(PuntoVenta, or_(
            OrdenCargaAnticipoRetirado.punto_venta_id == PuntoVenta.id,
            PuntoVenta.id == case(
                (

                    Movimiento.punto_venta_id == null(),
                    OrdenCargaAnticipoRetirado.punto_venta_id,
                ),
                    else_=Movimiento.punto_venta_id,
            )
            )
        )
        .filter(
            or_(
                Movimiento.anticipo_id != None,
                Movimiento.punto_venta_id != None
            )
        )
    )


def get_estado_cuenta_proveedor_pdv_liquidacion(db: Session) -> Query:
    return (
        db.query(
            Liquidacion.proveedor_id.label("contraparte_id"),
            Proveedor.nombre.label("contraparte"),
            Proveedor.nombre_corto.label("contraparte_alias"),
            Proveedor.numero_documento.label("contraparte_numero_documento"),
            Liquidacion.punto_venta_id.label("punto_venta_id"),
            concat(PuntoVenta.nombre_corto).label("contraparte_pdv"),
            Liquidacion.contraparte_numero_documento.label("contraparte_numero_documento_pdv"),
            Liquidacion.tipo_contraparte_id.label("tipo_contraparte_id"),
            #TipoContraparte.descripcion.label("tipo_contraparte_descripcion") + " - PDV",
            literal_column("'PUNTO DE VENTA'").label("tipo_contraparte_descripcion"),
            Liquidacion.gestor_carga_id.label("gestor_carga_id"),
            Liquidacion.tipo_mov_liquidacion.label("tipo_flujo"),
            *get_cols_estado_cuenta_liquidacion_case_statement(),
        )
        .join(Liquidacion.proveedor)
        .join(Liquidacion.tipo_contraparte)
        .join(PuntoVenta,
            PuntoVenta.id == Liquidacion.punto_venta_id
        )
        .filter(Liquidacion.punto_venta_id != null())
        .filter(Liquidacion.estado != 'Cancelado')
    )


def get_estado_cuenta_pdv_subquery(db: Session) -> Query:
    proveedorPdv = get_estado_cuenta_proveedor_pdv(db)
    proveedorPdvProvision = get_provision_proveedor_pdv(db)
    proveedorPdvLiquidacion = get_estado_cuenta_proveedor_pdv_liquidacion(db)

    return proveedorPdv.union_all(proveedorPdvProvision, proveedorPdvLiquidacion)


def get_estado_cuenta_subquery(db: Session, mon_local_id:int) -> Query:

    chofer = get_estado_cuenta_chofer(db, mon_local_id)
    propietario = get_estado_cuenta_propietario(db, mon_local_id)
    proveedor = get_estado_cuenta_proveedor(db, mon_local_id)
    #proveedorPdv = get_estado_cuenta_proveedor_pdv(db)
    remitente = get_estado_cuenta_remitente(db, mon_local_id)
    otro = get_estado_cuenta_otro(db, mon_local_id)

    choferProvision = get_provision_chofer(db)
    propietarioProvision = get_provision_propietario(db)
    proveedorProvision = get_provision_proveedor(db)
    #proveedorPdvProvision = get_provision_proveedor_pdv(db)
    remitenteProvision = get_provision_remitente(db)
    #otroProvision = get_provision_otro(db)

    choferLiquidacion = get_estado_cuenta_chofer_liquidacion(db)
    propietarioLiquidacion = get_estado_cuenta_propietario_liquidacion(db)
    proveedorLiquidacion = get_estado_cuenta_proveedor_liquidacion(db)
    #proveedorPdvLiquidacion = get_estado_cuenta_proveedor_pdv_liquidacion(db)
    remitenteLiquidacion = get_estado_cuenta_remitente_liquidacion(db)
    otroLiquidacion = get_estado_cuenta_otro_liquidacion(db)

    return chofer.union_all(choferLiquidacion, choferProvision, propietario, propietarioLiquidacion,
        propietarioProvision, proveedor, proveedorLiquidacion, proveedorProvision, # proveedorPdv, proveedorPdvLiquidacion, proveedorPdvProvision
        remitente, remitenteLiquidacion, remitenteProvision, otro, otroLiquidacion)
    #return chofer.union_all(proveedor, proveedorLiquidacion)


def get_estado_cuenta_group_by_query(db: Session, table: Query) -> Query:
    return (
        db.query(
            table.c.contraparte_id.label("contraparte_id"),
            table.c.contraparte.label("contraparte"),
            table.c.contraparte_alias.label("contraparte_alias"),
            table.c.contraparte_numero_documento.label("contraparte_numero_documento"),
            table.c.punto_venta_id.label("punto_venta_id"),
            table.c.contraparte_pdv.label("contraparte_pdv"),
            table.c.contraparte_numero_documento_pdv.label("contraparte_numero_documento_pdv"),
            table.c.tipo_contraparte_id.label("tipo_contraparte_id"),
            table.c.tipo_contraparte_descripcion.label("tipo_contraparte_descripcion"),
            table.c.es_pdv.label("es_pdv"),
            table.c.gestor_carga_id.label("gestor_carga_id"),
            func.sum(table.c.provision).label("provision"),
            func.sum(table.c.pendiente).label("pendiente"),
            func.sum(table.c.confirmado).label("confirmado"),
            func.sum(table.c.finalizado).label("finalizado"),
            func.sum(table.c.cantidad_pendiente).label("cantidad_pendiente"),
            func.sum(table.c.cantidad_confirmado).label("cantidad_confirmado"),
            func.sum(table.c.cantidad_finalizado).label("cantidad_finalizado"),
        )
        .group_by(
            table.c.contraparte_id,
            table.c.contraparte,
            table.c.contraparte_alias,
            table.c.contraparte_numero_documento,
            table.c.punto_venta_id,
            table.c.contraparte_pdv,
            table.c.contraparte_numero_documento_pdv,
            table.c.tipo_contraparte_id,
            table.c.tipo_contraparte_descripcion,
            table.c.gestor_carga_id,
            table.c.es_pdv,
        )
        .order_by(
            table.c.tipo_contraparte_descripcion,
            table.c.contraparte
        )
    )


def get_estado_cuenta_pdv_group_by_query(db: Session, table: Query) -> Query:
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
            table.c.tipo_flujo.label("tipo_flujo"),
            func.sum(table.c.provision).label("provision"),
            func.sum(table.c.pendiente).label("pendiente"),
            func.sum(table.c.confirmado).label("confirmado"),
            func.sum(table.c.finalizado).label("finalizado"),
            func.sum(table.c.cantidad_pendiente).label("cantidad_pendiente"),
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
            table.c.gestor_carga_id,
            table.c.tipo_flujo,
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
    db: Session, gestor_carga_id: int, mon_local_id:int
) -> List[Row]:
    table = (
        get_estado_cuenta_subquery(db, mon_local_id)
        .filter(Movimiento.gestor_carga_id == gestor_carga_id)
        .subquery()
    )
    return get_estado_cuenta_group_by_query(db, table).all()


def get_estado_cuenta_by_contraparte_and_tipo(
    db: Session,
    contraparte_id: int,
    mon_local:int,
    tipo_contraparte_id: Optional[int],
    punto_venta_id: int = None
) -> Optional[Row]:
    subquery = get_estado_cuenta_subquery(db, mon_local).subquery()
    table = (
        db.query(subquery)
        .filter(
            subquery.c.contraparte_id == contraparte_id,
            #subquery.c.tipo_contraparte_id == tipo_contraparte_id,
            or_(
                subquery.c.tipo_contraparte_id == tipo_contraparte_id,
                tipo_contraparte_id == None
            ),
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


def get_estado_cuenta_pdv_list(
    db: Session,
    tipo_flujo: Optional[str],
    contraparte_id: Optional[int],
    contraparte: Optional[str],
    contraparte_numero_documento: Optional[str],
    punto_venta_id: Optional[int],
) -> List[Row]:
    # get_estado_cuenta_subquery(db)
    subquery = get_estado_cuenta_pdv_subquery(db)\
        .filter(PuntoVenta.id > 0).subquery()
    table = (
        db.query(subquery)
        .filter(
            or_(
                subquery.c.tipo_flujo == tipo_flujo,
                tipo_flujo == None
            ),
            or_(
                subquery.c.contraparte == contraparte,
                contraparte == None
            ),
            or_(
                subquery.c.contraparte_numero_documento == contraparte_numero_documento,
                contraparte_numero_documento == None
            )
            # add filtro solo pdv
        )
        .subquery()
    )
    return get_estado_cuenta_pdv_group_by_query(db, table).all()


def get_estado_cuenta_pdv(
    db: Session,
    tipo_flujo: Optional[str],
    contraparte_id: Optional[int],
    contraparte: Optional[str],
    contraparte_numero_documento: Optional[str],
    punto_venta_id: Optional[int],
) -> Optional[Row]:

    logger.info(tipo_flujo)
    logger.info(contraparte)
    logger.info(contraparte_numero_documento)
    logger.info(punto_venta_id)

    subquery = get_estado_cuenta_pdv_subquery(db).subquery()
        #.filter(PuntoVenta.id > 0).subquery()
    table = (
        db.query(subquery)
        .filter(
            subquery.c.punto_venta_id == punto_venta_id,
            or_(
                subquery.c.tipo_flujo == tipo_flujo,
                tipo_flujo == None
            ),
            or_(
                subquery.c.contraparte_pdv == contraparte,
                contraparte == None
            ),
            or_(
                subquery.c.contraparte_numero_documento_pdv == contraparte_numero_documento,
                contraparte_numero_documento == None
            )
            # add filtro solo pdv
        )
        .subquery()
    )
    return get_estado_cuenta_pdv_group_by_query(db, table).first()



def get_cols_estado_cuenta_case_statement(mon_local_id:int) -> Tuple:
    return (
        literal_column("0").label("provision"),
        case(
            (
                and_(
                    Movimiento.liquidacion_id == null(),
                    Movimiento.estado == EstadoEnum.PENDIENTE.value,
                ),
                case(
                    (
                        Movimiento.moneda_id == mon_local_id,
                        Movimiento.monto,
                    ),
                    #else_= Movimiento.monto*MonedaCotizacion.cotizacion_moneda,
                    else_= Movimiento.monto_mon_local,
                )
            ),
            else_=literal_column("0"),
        ).label("pendiente"),
        case(
            (
                or_(
                    Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                    Movimiento.estado == EstadoEnum.CONFIRMADO.value,
                    Movimiento.estado == EstadoEnum.FINALIZADO.value,
                ),
                #Movimiento.monto,
                Movimiento.monto_mon_local,
            ),
            else_=literal_column("0"),
        ).label("confirmado"),
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
                or_(
                   Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                   Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                   Movimiento.estado == EstadoEnum.FINALIZADO.value,
                ),
                literal_column("1"),
            ),
            else_=literal_column("0"),
        ).label("cantidad_confirmado"),
        literal_column("0").label("cantidad_finalizado"),
    )


def get_cols_estado_cuenta_liquidacion_case_statement() -> Tuple:
    return (
        literal_column("0").label("provision"),
        literal_column("0").label("pendiente"),
        literal_column("0").label("confirmado"),
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
    punto_venta_id: Optional[int],
    tipo_movimiento: Optional[str],
) -> Query:

    query = db.query(
            literal_column("2").label("orden"),
            null().label("movimiento_id"),
            case(
                (
                    InstrumentoVia.descripcion == 'Caja',
                    Instrumento.caja_id,
                ),
                else_= Instrumento.banco_id
            ).label("instrumento_id"),
            Liquidacion.id,
            literal_column("' '").label("contraparte_alias"),
            Liquidacion.created_at,
            concat(InstrumentoVia.descripcion, ' | ', TipoInstrumento.descripcion).label("tipo_cuenta_descripcion"),
            literal_column("'Pago/Cobro'").label("tipo_movimiento_concepto"),
            Liquidacion.es_pago_cobro.label("detalle"),
            Liquidacion.id.label("nro_documento_relacionado"),
            Factura.numero_factura,
            Instrumento.operacion_estado,
            literal_column("''").label("estado_liquidacion"),
            literal_column("false").label("es_editable"),
            literal_column("false").label("can_edit_oc"),
            literal_column("false").label("documento_fisico"),
            Moneda.simbolo.label("moneda"),
            literal_column("1").label("tipo_cambio_moneda"),
            literal_column("0"),
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
        .join(Instrumento.via)\
        .join(Liquidacion.moneda)\
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
                or_(
                    Liquidacion.tipo_mov_liquidacion == tipo_movimiento,
                    tipo_movimiento == None
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
    punto_venta_id: Optional[int],
    linea_movimiento: Optional[str],
    ) -> List[Row]:

    #obtenemos la moneda local de la gestora
    mon_local_id=1

    query_provisiones = get_query_provisiones_by_contraparte_and_gestor_carga_id(
        db, tipo_contraparte_id, contraparte_id, contraparte, contraparte_numero_documento,
        gestor_carga_id, punto_venta_id
    )

    query_movimientos = get_query_movimientos_by_contraparte_and_gestor_carga_id(
        db, tipo_contraparte_id, contraparte_id, contraparte, contraparte_numero_documento,
        gestor_carga_id, mon_local_id, punto_venta_id, linea_movimiento
    )

    query_instrumentos = get_query_instrumentos_by_contraparte_and_gestor_carga_id(
        db, tipo_contraparte_id, contraparte_id, contraparte, contraparte_numero_documento,
        gestor_carga_id, punto_venta_id, linea_movimiento
    )

    table = query_movimientos.union_all(query_provisiones, query_instrumentos).subquery()

    # columnas que se retorna
    query = db.query(
        table.c.movimiento_id.label("movimiento_id"),
        table.c.liquidacion_id.label("liquidacion_id"),
        table.c.instrumento_id.label("instrumento_id"),
        table.c.contraparte_alias.label("contraparte_alias"),
        table.c.fecha.label("fecha"),
        table.c.tipo_cuenta_descripcion.label("tipo_cuenta_descripcion"),
        table.c.tipo_movimiento_concepto.label("tipo_movimiento_concepto"),
        table.c.nro_documento_relacionado.label("nro_documento_relacionado"),
        table.c.detalle.label("detalle"),
        table.c.info.label("info"),
        table.c.estado.label("estado"),
        table.c.estado_liquidacion.label("estado_liquidacion"),
        table.c.es_editable.label("es_editable"),
        table.c.can_edit_oc.label("can_edit_oc"),
        table.c.documento_fisico.label("documento_fisico"),
        table.c.moneda.label("moneda"),
        table.c.tipo_cambio_moneda.label("tipo_cambio_moneda"),
        table.c.provision.label("provision"),
        table.c.pendiente.label("pendiente"),
        table.c.en_proceso.label("en_proceso"),
        table.c.confirmado.label("confirmado"),
        table.c.finalizado.label("finalizado"),
        ).order_by(table.c.orden, nullsfirst(desc(table.c.liquidacion_id)), desc(table.c.movimiento_id))

    return query.all()


def get_estado_cuenta_provision() -> Tuple:
    return (
        literal_column('0').label('punto_venta_id'),
        null().label('contraparte_pdv'),
        null().label('contraparte_numero_documento_pdv'),
        Provision.tipo_contraparte_id.label("tipo_contraparte_id"),
        TipoContraparte.descripcion.label("tipo_contraparte_descripcion"),
        Provision.gestor_carga_id.label("gestor_carga_id"),
        #Movimiento.linea_movimiento.label("tipo_flujo"),
        null().label("tipo_flujo"),
        *get_cols_estado_cuenta_provision(),
    )


def get_cols_estado_cuenta_provision() -> Tuple:
    return (
        Provision.monto.label("provision"),
        literal_column("0").label("pendiente"),
        literal_column("0").label("confirmado"),
        literal_column("0").label("finalizado"),
        literal_column("0").label("cantidad_pendiente"),
        literal_column("0").label("cantidad_confirmado"),
        literal_column("0").label("cantidad_finalizado"),
    )


def get_provision_chofer(db: Session) -> Query:
    return (
        db.query(
            Provision.chofer_id.label("contraparte_id"),
            Chofer.nombre.label("contraparte"),
            null().label("contraparte_alias"),
            Chofer.numero_documento.label("contraparte_numero_documento"),
            literal_column('false').label("es_pdv"),
            *get_estado_cuenta_provision(),
        )
        .join(Provision.chofer)
        .join(Provision.tipo_contraparte)
    )


def get_provision_propietario(db: Session) -> Query:
    return (
        db.query(
            Provision.propietario_id.label("contraparte_id"),
            Propietario.nombre.label("contraparte"),
            null().label("contraparte_alias"),
            Propietario.ruc.label("contraparte_numero_documento"),
            literal_column('false').label("es_pdv"),
            *get_estado_cuenta_provision(),
        )
        .join(Provision.propietario)
        .join(Provision.tipo_contraparte)
    )


def get_provision_proveedor(db: Session) -> Query:
    #queryPDV = db.query(PuntoVenta).subquery()
    return (
        db.query(
            Provision.proveedor_id.label("contraparte_id"),
            concat(Proveedor.nombre).label("contraparte"),
            concat(Proveedor.nombre_corto).label("contraparte_alias"),
            Proveedor.numero_documento.label("contraparte_numero_documento"),
            exists().where(PuntoVenta.proveedor_id == Proveedor.id).label("es_pdv"),
            *get_estado_cuenta_provision(),
        )
        .join(Provision.proveedor)
        #.filter(~exists().where(PuntoVenta.proveedor_id == Proveedor.id))
        .join(Provision.tipo_contraparte)
    )


def get_provision_remitente(db: Session) -> Query:
    return (
        db.query(
            Provision.remitente_id.label("contraparte_id"),
            concat(Remitente.nombre).label("contraparte"),
            null().label("contraparte_alias"),
            Remitente.numero_documento.label("contraparte_numero_documento"),
            literal_column('false').label("es_pdv"),
            *get_estado_cuenta_provision(),
        )
        .join(Provision.remitente)
        .join(Provision.tipo_contraparte)
    )


def get_provision_proveedor_pdv(db: Session) -> Query:
    return (
        db.query(
            Provision.proveedor_id.label("contraparte_id"),
            Proveedor.nombre.label("contraparte"),
            Proveedor.nombre_corto.label("contraparte_alias"),
            Proveedor.numero_documento.label("contraparte_numero_documento"),
            PuntoVenta.id.label("punto_venta_id"),
            concat(PuntoVenta.nombre_corto).label("contraparte_pdv"),
            PuntoVenta.numero_documento.label("contraparte_numero_documento_pdv"),
            Provision.tipo_contraparte_id.label("tipo_contraparte_id"),
            #TipoContraparte.descripcion.label("tipo_contraparte_descripcion") + " - PDV",
            literal_column("'PUNTO DE VENTA'").label("tipo_contraparte_descripcion"),
            Provision.gestor_carga_id.label("gestor_carga_id"),
            Provision.linea_movimiento.label("tipo_flujo"),
            *get_cols_estado_cuenta_provision(),
        )
        .join(Provision.proveedor)
        .join(Provision.tipo_contraparte)
        .outerjoin(Provision.anticipo)
        .outerjoin(PuntoVenta, or_(
            OrdenCargaAnticipoRetirado.punto_venta_id == PuntoVenta.id,
            PuntoVenta.id == case(
                (

                    Provision.punto_venta_id == null(),
                    OrdenCargaAnticipoRetirado.punto_venta_id,
                ),
                    else_=Provision.punto_venta_id,
            )
            )
        )
        .filter(
            or_(
                Provision.anticipo_id != None,
                Provision.punto_venta_id != None
            )
        )
    )


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

