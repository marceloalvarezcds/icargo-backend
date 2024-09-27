from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Query, Session # type: ignore
from sqlalchemy import case, null
from sqlalchemy.sql.elements import and_, or_, literal_column # type: ignore
from app.enums import MovimientoEstadoEnum, EstadoEnum
from app.enums.tipo_movimiento import TipoMovimientoEnum
from app.models import Movimiento, OrdenCargaAnticipoRetirado, Liquidacion, TipoCuenta
from app.models.tipo_movimiento import TipoMovimiento
from app.schemas import MovimientoForm
from app.schemas import MovimientoEstadoCuenta
from app.schemas import Movimiento as MovimientoSchema


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
    punto_venta_id: Optional[int]
) -> List[Movimiento]:
    return (
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
                    punto_venta_id == None
                ),
                Movimiento.estado == estado,
                Movimiento.gestor_carga_id == gestor_carga_id,
            )
        )
        .order_by(Movimiento.contraparte, Movimiento.liquidacion_id)
        .all()
    )


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
        .order_by(Movimiento.contraparte, Movimiento.liquidacion_id)
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
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_monto_movimiento(
    obj: Movimiento,
    db: Session,
    monto: Decimal,
    detalle: str,
    moneda_id: Optional[int],
    gestor_carga_id: int,
    modified_by: str,
) -> Movimiento:
    obj.monto = monto
    obj.detalle = detalle
    if moneda_id:
        obj.moneda_id = moneda_id
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
    punto_venta_id: Optional[int]
    ) -> Query:
    # columnas especificas
    query = db.query(
                Movimiento.id.label("movimiento_id"),
                Movimiento.liquidacion_id.label("liquidacion_id"),
                Movimiento.created_at.label("fecha"),
                TipoCuenta.descripcion.label("tipo_cuenta_descripcion"),
                TipoMovimiento.descripcion.label("tipo_movimiento_concepto"),
                literal_column("'pendiente-detalle'").label("detalle"),
                Movimiento.orden_carga_id.label("nro_documento_relacionado"),
                Movimiento.detalle.label("info"),
                Movimiento.estado.label("estado"),
                *get_cols_estado_cuenta_case_statement(),
                )\
                .join(Movimiento.tipo_movimiento)\
                .join(Movimiento.cuenta)\
                .outerjoin(Movimiento.liquidacion)\
                .outerjoin(Movimiento.anticipo)
    # query = query.add_columns(
    #     *get_cols_estado_cuenta_case_statement()
    # )
    query = query.filter(
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
                    punto_venta_id == None
                ),
                Movimiento.gestor_carga_id == gestor_carga_id,
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

    query = get_query_movimientos_by_contraparte_and_gestor_carga_id(
        db, tipo_contraparte_id, contraparte_id, contraparte, contraparte_numero_documento,
        gestor_carga_id, punto_venta_id)

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


def get_cols_estado_cuenta_case_statement() -> tuple:
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
        ).label("finalizado")
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
