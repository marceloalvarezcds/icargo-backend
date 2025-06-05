from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Query, Session, aliased # type: ignore
from sqlalchemy import case, null, desc, func
from sqlalchemy.sql.elements import and_, or_, literal_column # type: ignore
from app.enums import MovimientoEstadoEnum, EstadoEnum, TipoAnticipoEnum
from app.enums.tipo_movimiento import TipoMovimientoEnum
from app.models import (
    Movimiento, OrdenCargaAnticipoRetirado, Liquidacion, TipoCuenta, TipoMovimiento,
    OrdenCargaAnticipoRetirado, Moneda, OrdenCarga, Proveedor, PuntoVenta, MonedaCotizacion
)
from app.schemas import MovimientoForm
from app.schemas import MovimientoEstadoCuenta
from app.schemas import Movimiento as MovimientoSchema
from app.repositories.moneda import get_moneda_by_gestor_carga


def get_movimiento_list(db: Session) -> List[Movimiento]:
    return (
        db.query(Movimiento)
        .filter(Movimiento.estado != MovimientoEstadoEnum.ELIMINADO.value)
        .order_by(Movimiento.contraparte, Movimiento.liquidacion_id)
        .all()
    )


def get_movimiento_list_by_contraparte(
    db: Session,
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    estado: str,
) -> List[Movimiento]:
    return (
        db.query(Movimiento)
        .filter(
            and_(
                Movimiento.tipo_contraparte_id == tipo_contraparte_id,
                or_(
                    Movimiento.propietario_id == contraparte_id,
                    Movimiento.remitente_id == contraparte_id,
                    Movimiento.proveedor_id == contraparte_id,
                    and_(
                        Movimiento.contraparte == contraparte,
                        Movimiento.contraparte_numero_documento
                        == contraparte_numero_documento,
                    ),
                    Movimiento.chofer_id == contraparte_id,
                ),
                Movimiento.contraparte == contraparte,
                Movimiento.contraparte_numero_documento == contraparte_numero_documento,
                Movimiento.estado == estado,
            )
        )
        .order_by(Movimiento.contraparte, Movimiento.liquidacion_id)
        .all()
    )


def get_movimiento_list_for_reports_by_contraparte(
    db: Session,
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    estado: str,
) -> List[Movimiento]:
    return (
        db.query(Movimiento)
        .filter(
            and_(
                Movimiento.tipo_contraparte_id == tipo_contraparte_id,
                or_(
                    Movimiento.propietario_id == contraparte_id,
                    Movimiento.remitente_id == contraparte_id,
                    Movimiento.proveedor_id == contraparte_id,
                    and_(
                        Movimiento.contraparte == contraparte,
                        Movimiento.contraparte_numero_documento
                        == contraparte_numero_documento,
                    ),
                    Movimiento.chofer_id == contraparte_id,
                ),
                Movimiento.estado == estado,
            )
        )
        .order_by(
            Movimiento.numero_documento_relacionado,
            Movimiento.contraparte,
            Movimiento.liquidacion_id,
        )
        .all()
    )


def get_movimiento_list_for_reports_by_contraparte_and_gestor_carga_id(
    db: Session,
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    estado: str,
    gestor_carga_id: int,
) -> List[Movimiento]:
    return (
        db.query(Movimiento)
        .filter(
            and_(
                Movimiento.tipo_contraparte_id == tipo_contraparte_id,
                or_(
                    Movimiento.propietario_id == contraparte_id,
                    Movimiento.remitente_id == contraparte_id,
                    Movimiento.proveedor_id == contraparte_id,
                    and_(
                        Movimiento.contraparte == contraparte,
                        Movimiento.contraparte_numero_documento
                        == contraparte_numero_documento,
                    ),
                    Movimiento.chofer_id == contraparte_id,
                ),
                Movimiento.estado == estado,
                Movimiento.gestor_carga_id == gestor_carga_id,
            )
        )
        .order_by(
            Movimiento.numero_documento_relacionado,
            Movimiento.contraparte,
            Movimiento.liquidacion_id,
        )
        .all()
    )


def get_movimiento_list_for_reports_by_liquidacion_id(
    db: Session,
    liquidacion_id: int,
    estado: str,
) -> List[Movimiento]:
    return (
        db.query(Movimiento)
        .filter(
            and_(
                Movimiento.estado == estado,
                Movimiento.liquidacion_id == liquidacion_id,
            )
        )
        .order_by(
            Movimiento.numero_documento_relacionado,
            Movimiento.contraparte,
            Movimiento.liquidacion_id,
        )
        .all()
    )


def get_movimiento_list_for_flete_pdf_reports_by_liquidacion_id(
    db: Session,
    liquidacion_id: int,
    estado: str,
) -> List[Movimiento]:
    return (
        db.query(Movimiento)
        .join(Movimiento.tipo_movimiento)
        .filter(
            and_(
                Movimiento.estado == estado,
                Movimiento.liquidacion_id == liquidacion_id,
                TipoMovimiento.descripcion != TipoMovimientoEnum.OTRO.value,
            )
        )
        .order_by(
            Movimiento.numero_documento_relacionado,
            Movimiento.contraparte,
            Movimiento.liquidacion_id,
        )
        .all()
    )


def get_movimiento_list_for_otro_pdf_reports_by_liquidacion_id(
    db: Session,
    liquidacion_id: int,
    estado: str,
) -> List[Movimiento]:
    return (
        db.query(Movimiento)
        .join(Movimiento.tipo_movimiento)
        .filter(
            and_(
                Movimiento.estado == estado,
                Movimiento.liquidacion_id == liquidacion_id,
                TipoMovimiento.descripcion == TipoMovimientoEnum.OTRO.value,
            )
        )
        .order_by(
            Movimiento.numero_documento_relacionado,
            Movimiento.contraparte,
            Movimiento.liquidacion_id,
        )
        .all()
    )


def get_movimiento_list_by_contraparte_and_gestor_carga_id(
    db: Session,
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    estado: str,
    gestor_carga_id: int,
    punto_venta_id: Optional[int],
    listar_efectivo: Optional[str]
) -> List[Movimiento]:
    query = (
        db.query(Movimiento)
        .outerjoin(Movimiento.anticipo)
        .filter(
            and_(
                Movimiento.tipo_contraparte_id == tipo_contraparte_id,
                or_(
                    Movimiento.propietario_id == contraparte_id,
                    Movimiento.remitente_id == contraparte_id,
                    Movimiento.proveedor_id == contraparte_id,
                    and_(
                        Movimiento.contraparte == contraparte,
                        Movimiento.contraparte_numero_documento
                        == contraparte_numero_documento,
                    ),
                    Movimiento.chofer_id == contraparte_id,
                ),
                or_(
                    OrdenCargaAnticipoRetirado.punto_venta_id == punto_venta_id,
                    Movimiento.punto_venta_id == punto_venta_id,
                    punto_venta_id == None
                ),
                Movimiento.estado == estado,
                Movimiento.gestor_carga_id == gestor_carga_id,

            )
        ).order_by(Movimiento.contraparte, Movimiento.id.desc())
    )

    if listar_efectivo:
        #if listar_efectivo == TipoLiquidacion.INSUMO.value:
        query = query.filter(Movimiento.linea_movimiento == listar_efectivo)
        #elif listar_efectivo == TipoLiquidacion.EFECTIVO.value:
        #    query = query.filter(OrdenCargaAnticipoRetirado.insumo_punto_venta_precio_id == null())

    return query.all()


def get_movimiento_list_by_liquidacion(
    db: Session,
    liquidacion_id: int,
    estado: str,
) -> List[Movimiento]:
    return (
        db.query(Movimiento)
        .filter(
            and_(
                Movimiento.liquidacion_id == liquidacion_id,
                Movimiento.estado == estado,
            )
        )
        .order_by(Movimiento.contraparte, Movimiento.liquidacion_id)
        .all()
    )


def get_movimiento_list_by_liquidacion_id(
    db: Session,
    liquidacion_id: int,
) -> List[Movimiento]:
    return (
        db.query(Movimiento)
        .filter(
            and_(
                Movimiento.liquidacion_id == liquidacion_id,
                Movimiento.estado != MovimientoEstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(Movimiento.contraparte, Movimiento.liquidacion_id)
        .all()
    )


def get_movimiento_list_by_liquidacion_and_gestor_carga_id(
    db: Session,
    liquidacion_id: int,
    estado: str,
    gestor_carga_id: int,
) -> List[Movimiento]:
    return (
        db.query(Movimiento)
        .filter(
            and_(
                Movimiento.liquidacion_id == liquidacion_id,
                Movimiento.estado == estado,
                Movimiento.gestor_carga_id == gestor_carga_id,
            )
        )
        .order_by(Movimiento.contraparte, desc(Movimiento.id))
        .all()
    )


def get_movimiento_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: int
) -> List[Movimiento]:
    return (
        db.query(Movimiento)
        .filter(
            and_(
                Movimiento.gestor_carga_id == gestor_carga_id,
                Movimiento.estado != MovimientoEstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(Movimiento.contraparte, Movimiento.liquidacion_id)
        .all()
    )


def get_movimiento_list_by_orden_carga_id(
    db: Session, orden_carga_id: int
) -> List[Movimiento]:
    return (
        db.query(Movimiento)
        .filter(
            and_(
                Movimiento.orden_carga_id == orden_carga_id,
                Movimiento.estado != MovimientoEstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(Movimiento.contraparte, Movimiento.liquidacion_id)
        .all()
    )


def get_movimiento_count_by_tipo_documento_relacionado_id(
    db: Session, tipo_documento_relacionado_id: int
) -> int:
    return (
        db.query(Movimiento)
        .filter(
            and_(
                Movimiento.tipo_documento_relacionado_id
                == tipo_documento_relacionado_id,
                Movimiento.estado != MovimientoEstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(Movimiento.contraparte, Movimiento.liquidacion_id)
        .count()
    )


def get_movimiento_by_id(db: Session, id: int) -> Optional[Movimiento]:
    return db.query(Movimiento).get(id)


def create_movimiento(
    db: Session,
    data: MovimientoForm,
    gestor_carga_id: int,
    modified_by: str,
) -> Movimiento:

    obj = Movimiento(
        gestor_carga_id=gestor_carga_id,
        liquidacion_id=data.liquidacion_id,
        orden_carga_id=data.orden_carga_id,
        tipo_contraparte_id=data.tipo_contraparte_id,
        contraparte=data.contraparte,
        contraparte_numero_documento=data.contraparte_numero_documento,
        tipo_documento_relacionado_id=data.tipo_documento_relacionado_id,
        numero_documento_relacionado=data.numero_documento_relacionado,
        cuenta_id=data.cuenta_id,
        tipo_movimiento_id=data.tipo_movimiento_id,
        es_editable=data.es_editable,
        estado=data.estado.value,
        fecha=data.fecha,
        detalle=data.detalle,
        monto=data.monto,
        monto_mon_local= data.monto_mon_local if data.monto_mon_local else data.monto*data.tipo_cambio_moneda,
        moneda_id=data.moneda_id,
        tipo_cambio_moneda=data.tipo_cambio_moneda,
        fecha_cambio_moneda=data.fecha_cambio_moneda,
        # En caso de ser movimiento de anticipo
        anticipo_id=data.anticipo_id,
        # En caso de ser movimiento de complemento o descuento
        complemento_id=data.complemento_id,
        descuento_id=data.descuento_id,
        # IDs para referencia a las tablas de las contraparte
        chofer_id=data.chofer_id,
        propietario_id=data.propietario_id,
        proveedor_id=data.proveedor_id,
        remitente_id=data.remitente_id,
        created_by=modified_by,
        modified_by=modified_by,
        tipo_movimiento_info=data.tipo_movimiento_info,
        punto_venta_id=data.punto_venta_id,
        linea_movimiento=data.linea_movimiento if data.linea_movimiento else TipoAnticipoEnum.EFECTIVO.value,
        # monto_mon_local=data.monto*data.tipo_cambio_moneda
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_monto_movimiento(
    obj: Movimiento,
    db: Session,
    monto: Decimal,
    monto_ml: Decimal,
    detalle: str,
    moneda_id: Optional[int],
    tipo_cambio_moneda: Optional[Decimal],
    gestor_carga_id: int,
    modified_by: str,
) -> Movimiento:
    obj.monto = monto
    obj.monto_mon_local = monto_ml
    obj.detalle = detalle
    if moneda_id:
        obj.moneda_id = moneda_id
    obj.tipo_cambio_moneda = tipo_cambio_moneda if tipo_cambio_moneda else 1
    obj.fecha_cambio_moneda = datetime.now() if tipo_cambio_moneda else obj.fecha_cambio_moneda
    obj.gestor_carga_id = gestor_carga_id
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def edit_movimiento(
    obj: Movimiento,
    db: Session,
    data: MovimientoForm,
    gestor_carga_id: int,
    modified_by: str,
) -> Movimiento:
    obj.liquidacion_id = data.liquidacion_id
    obj.orden_carga_id = data.orden_carga_id
    obj.tipo_contraparte_id = data.tipo_contraparte_id
    obj.contraparte = data.contraparte
    obj.contraparte_numero_documento = data.contraparte_numero_documento
    obj.tipo_documento_relacionado_id = data.tipo_documento_relacionado_id
    obj.numero_documento_relacionado = data.numero_documento_relacionado
    obj.cuenta_id = data.cuenta_id
    obj.tipo_movimiento_id = data.tipo_movimiento_id
    obj.detalle = data.detalle
    obj.monto = data.monto
    obj.monto_mon_local= data.monto_mon_local if data.monto_mon_local else data.monto*data.tipo_cambio_moneda,
    obj.moneda_id = data.moneda_id
    obj.tipo_cambio_moneda = data.tipo_cambio_moneda
    obj.fecha_cambio_moneda = data.fecha_cambio_moneda
    # En caso de ser movimiento de anticipo
    obj.anticipo_id = data.anticipo_id
    # En caso de ser movimiento de complemento o descuento
    obj.complemento_id = data.complemento_id
    obj.descuento_id = data.descuento_id
    # IDs para referencia a las tablas de las contraparte
    obj.chofer_id = data.chofer_id
    obj.propietario_id = data.propietario_id
    obj.proveedor_id = data.proveedor_id
    obj.remitente_id = data.remitente_id
    obj.gestor_carga_id = gestor_carga_id
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def change_movimiento_status(
    obj: Movimiento,
    db: Session,
    status: MovimientoEstadoEnum,
    modified_by: str,
) -> Movimiento:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_movimiento(
    obj: Movimiento,
    db: Session,
    modified_by: str,
) -> Movimiento:
    return change_movimiento_status(
        obj, db, MovimientoEstadoEnum.ELIMINADO, modified_by
    )


def get_query_movimientos_by_contraparte_and_gestor_carga_id(
    db: Session,
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    gestor_carga_id: int,
    mon_local_id:int,
    punto_venta_id: Optional[int],
    tipo_movimiento: Optional[str],
    ) -> Query:

    # columnas especificas
    queryProveedor = db.query(Proveedor.nombre)\
            .filter(Proveedor.id == Movimiento.proveedor_id)\
            .label('contraparte_alias')

    queryPDV = db.query(PuntoVenta.nombre_corto)\
            .filter(PuntoVenta.id == Movimiento.punto_venta_id)\
            .label('contraparte_alias')

    # agregar case para contraparte nombre
    # si es C buscar en tabla C y de ultima usar el nombre del movimiento - caso otros

    query = db.query(
                literal_column("2").label("orden"),
                Movimiento.id.label("movimiento_id"),
                literal_column("0").label("instrumento_id"),
                Movimiento.liquidacion_id.label("liquidacion_id"),
                case(
                    (
                        Movimiento.punto_venta_id != null(),
                        queryPDV,
                    ),
                    (
                        Movimiento.proveedor_id != null(),
                        queryProveedor
                    ),
                    else_=literal_column("'OTROS'"),
                ).label("contraparte_alias"),
                Movimiento.created_at.label("fecha"),
                TipoCuenta.descripcion.label("tipo_cuenta_descripcion"),
                TipoMovimiento.descripcion.label("tipo_movimiento_concepto"),
                Movimiento.tipo_movimiento_info.label("detalle"),
                Movimiento.orden_carga_id.label("nro_documento_relacionado"),
                Movimiento.detalle.label("info"),
                Movimiento.estado.label("estado"),
                Liquidacion.estado.label("estado_liquidacion"),
                Movimiento.es_editable.label("es_editable"),
                case(
                    (
                        and_(
                            Movimiento.estado != MovimientoEstadoEnum.FINALIZADO.value,
                            Movimiento.orden_carga_id != null(),
                            or_(
                                TipoMovimiento.descripcion == TipoMovimientoEnum.FLETE.value,
                                TipoMovimiento.descripcion == TipoMovimientoEnum.MERMA.value,
                            )
                        ),
                        True,
                    ),
                    else_=literal_column("false"),
                ).label("can_edit_oc"),
                OrdenCarga.documento_fisico.label("documento_fisico"),
                Moneda.simbolo.label("moneda"),
                Movimiento.tipo_cambio_moneda.label("tipo_cambio_moneda"),
                *get_cols_estado_cuenta_case_statement(mon_local_id),
                )\
                .join(Movimiento.tipo_movimiento)\
                .join(Movimiento.cuenta)\
                .join(Movimiento.moneda)\
                .outerjoin(Movimiento.orden_carga)\
                .outerjoin(Movimiento.liquidacion)\
                .outerjoin(Movimiento.anticipo)\
                .outerjoin(OrdenCargaAnticipoRetirado.flete_anticipo)\
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

    query = query.filter(
            and_(
                Movimiento.tipo_contraparte_id == tipo_contraparte_id,
                or_(
                    Movimiento.propietario_id == contraparte_id,
                    Movimiento.remitente_id == contraparte_id,
                    Movimiento.proveedor_id == contraparte_id,
                    Movimiento.chofer_id == contraparte_id,
                    and_(
                        Movimiento.contraparte == contraparte,
                        Movimiento.contraparte_numero_documento
                        == contraparte_numero_documento,
                    ),
                ),
                or_(
                    OrdenCargaAnticipoRetirado.punto_venta_id == punto_venta_id,
                    Movimiento.punto_venta_id == punto_venta_id,
                    punto_venta_id == None
                ),
                or_(
                    Movimiento.linea_movimiento == tipo_movimiento,
                    tipo_movimiento == None
                ),
                Movimiento.gestor_carga_id == gestor_carga_id,
                Movimiento.estado != MovimientoEstadoEnum.ELIMINADO.value
            )
        )
    return query


def get_all_movimiento_list_by_contraparte_and_gestor_carga_id(
    db: Session,
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    gestor_carga_id: int,
    punto_venta_id: Optional[int]
) -> List[MovimientoEstadoCuenta]:

    moneda_local= get_moneda_by_gestor_carga(db, gestor_carga_id)
    moneda_local_id = moneda_local.id if moneda_local else 1

    query = get_query_movimientos_by_contraparte_and_gestor_carga_id(
        db, tipo_contraparte_id, contraparte_id, contraparte, contraparte_numero_documento,
        gestor_carga_id, moneda_local_id, punto_venta_id )

    results = query.order_by(Movimiento.id.desc(), Movimiento.contraparte).all()

    # respuesta = []

    # for row in results:
    #     obj = MovimientoSchema.from_orm(row[0])
    #     obj2 = MovimientoEstadoCuenta(**obj.__dict__)
    #     obj2.pendiente = row[1]
    #     obj2.confirmado = row[3]
    #     obj2.finalizado = row[4]

    #     respuesta.append(obj2)

    return results


def get_all_movimiento_estado_cuenta_list_by_contraparte(
    db: Session,
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    punto_venta_id: Optional[int]
) -> List[MovimientoEstadoCuenta]:

    results = db.query(Movimiento)\
            .outerjoin(Movimiento.liquidacion)\
            .outerjoin(Movimiento.anticipo)\
            .add_columns(*get_cols_estado_cuenta_case_statement())\
            .filter(
                and_(
                    Movimiento.tipo_contraparte_id == tipo_contraparte_id,
                    or_(
                        Movimiento.propietario_id == contraparte_id,
                        Movimiento.remitente_id == contraparte_id,
                        Movimiento.proveedor_id == contraparte_id,
                        and_(
                            Movimiento.contraparte == contraparte,
                            Movimiento.contraparte_numero_documento
                            == contraparte_numero_documento,
                        ),
                        Movimiento.chofer_id == contraparte_id,
                    ),
                    Movimiento.contraparte == contraparte,
                    Movimiento.contraparte_numero_documento == contraparte_numero_documento,
                    or_(
                        OrdenCargaAnticipoRetirado.punto_venta_id == punto_venta_id,
                        punto_venta_id == None
                    ),
                )
            )\
            .order_by(Movimiento.id.desc(), Movimiento.contraparte)\
            .all()

    respuesta = []

    for row in results:
        obj = MovimientoSchema.from_orm(row[0])
        obj2 = MovimientoEstadoCuenta(**obj.__dict__)
        obj2.pendiente = row[1]
        obj2.confirmado = row[3]
        obj2.finalizado = row[4]
        respuesta.append(obj2)

    return respuesta


def get_all_movimiento_instrumento_estado_cuenta_list(

) -> List[MovimientoEstadoCuenta]:

    return []


def get_cols_estado_cuenta_case_statement(mon_local_id:int) -> tuple:
    return (
        Movimiento.monto.label("monto"),
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
                    else_= Movimiento.monto_mon_local,
                )
            ),
            else_=literal_column("0"),
        ).label("pendiente"),
        case(
            (
                and_(
                    Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
                    Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                ),
                case(
                    (
                        Movimiento.moneda_id == mon_local_id,
                        Movimiento.monto,
                    ),
                    else_= Movimiento.monto_mon_local,
                )
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
                    ),
                    and_(
                        Liquidacion.etapa == EstadoEnum.FINALIZADO.value,
                        Movimiento.estado == EstadoEnum.FINALIZADO.value,
                    ),
                ),
                case(
                    (
                        Movimiento.moneda_id == mon_local_id,
                        Movimiento.monto,
                    ),
                    else_= Movimiento.monto_mon_local,
                )
            ),
            else_=literal_column("0"),
        ).label("confirmado"),
        literal_column("0").label("finalizado"),
        # case(
        #     (
        #         and_(
        #             Liquidacion.etapa == EstadoEnum.FINALIZADO.value,
        #             Movimiento.estado == EstadoEnum.FINALIZADO.value,
        #         ),
        #         Movimiento.monto,
        #     ),
        #     else_=literal_column("0"),
        # ).label("finalizado")
        # case(
        #     (
        #         and_(
        #             Movimiento.liquidacion_id == null(),
        #             Movimiento.estado == EstadoEnum.PENDIENTE.value,
        #         ),
        #         literal_column("1"),
        #     ),
        #     else_=literal_column("0"),
        # ).label("cantidad_pendiente"),
        # case(
        #     (
        #         and_(
        #             Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
        #             Movimiento.estado == EstadoEnum.EN_PROCESO.value,
        #         ),
        #         literal_column("1"),
        #     ),
        #     else_=literal_column("0"),
        # ).label("cantidad_en_proceso"),
        # case(
        #     (
        #         or_(
        #             and_(
        #                 Liquidacion.etapa == EstadoEnum.EN_PROCESO.value,
        #                 Movimiento.estado == EstadoEnum.EN_PROCESO.value,
        #             ),
        #             and_(
        #                 Liquidacion.etapa == EstadoEnum.PENDIENTE.value,
        #                 Movimiento.estado == EstadoEnum.EN_PROCESO.value,
        #             ),
        #             and_(
        #                 Liquidacion.etapa == EstadoEnum.CONFIRMADO.value,
        #                 Movimiento.estado == EstadoEnum.CONFIRMADO.value,
        #             )
        #         ),
        #         literal_column("1"),
        #     ),
        #     else_=literal_column("0"),
        # ).label("cantidad_confirmado"),
        # case(
        #     (
        #         and_(
        #             Liquidacion.etapa == EstadoEnum.FINALIZADO.value,
        #             Movimiento.estado == EstadoEnum.FINALIZADO.value,
        #         ),
        #         literal_column("1"),
        #     ),
        #     else_=literal_column("0"),
        # ).label("cantidad_finalizado"),
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
