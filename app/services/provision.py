
from datetime import datetime
from http import HTTPStatus
from typing import Optional
from fastapi import HTTPException  # type: ignore
from sqlalchemy.orm import Session  # type: ignore
from app import repositories
from app.config import REPORTS_FOLDER
from app.enums import (
    MovimientoEstadoEnum,
    TipoContraparteEnum,
    TipoCuentaEnum,
    TipoMovimientoEnum,
    TipoAnticipoEnum
)
from app.models import (
    OrdenCarga,
    OrdenCargaComplemento,
    OrdenCargaDescuento,
    Provision,
)
from app.models.moneda_cotizacion import MonedaCotizacion
from app.schemas.provision import ProvisionForm

from app.logger import logger

def create_provision_by_finalizar_oc(
    db: Session,
    orden_carga: OrdenCarga,
    gestor_carga_id: Optional[int],
    modified_by: str,
):
    for complemento in orden_carga.complementos:
        create_provision_by_complemento(db, complemento, gestor_carga_id, modified_by)
    for descuento in orden_carga.descuentos:
        create_provision_by_descuento(db, descuento, gestor_carga_id, modified_by)
    create_provision_by_flete(db, orden_carga, gestor_carga_id, modified_by)
    create_provision_by_merma(db, orden_carga, gestor_carga_id, modified_by)

def create_provision_by_complemento(
    db: Session,
    complemento: OrdenCargaComplemento,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Optional[Provision]:
    propietario_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.PROPIETARIO.value
    )
    remitente_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.REMITENTE.value
    )
    tipo_documento_relacionado = (
        repositories.get_tipo_documento_relacionado_by_descripcion(db, "OC")
    )
    tipo_cuenta = repositories.get_tipo_cuenta_by_descripcion(
        db, TipoCuentaEnum.VIAJES.value
    )
    tipo_movimiento = repositories.get_tipo_movimiento_by_descripcion(
        db, TipoMovimientoEnum.COMPLEMENTO.value
    )
    if (
        not propietario_contraparte
        or not remitente_contraparte
        or not tipo_documento_relacionado
        or not tipo_cuenta
        or not tipo_movimiento
    ):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Tipo de contraparte, doc relacionado, cuenta o movimiento no existe",
        )

    # Cotización de la moneda remitente
    cotizacion_moneda_origen = db.query(MonedaCotizacion.cotizacion_moneda).filter(
        MonedaCotizacion.moneda_origen_id == complemento.remitente_moneda_id
    ).order_by(MonedaCotizacion.fecha.desc()).first()

    tipo_cambio_moneda_remitente = cotizacion_moneda_origen[0] if cotizacion_moneda_origen else 1

     # Cotización de la moneda propietario
    cotizacion_moneda_origen_propietario = db.query(MonedaCotizacion.cotizacion_moneda).filter(
        MonedaCotizacion.moneda_origen_id == complemento.propietario_moneda_id
    ).order_by(MonedaCotizacion.fecha.desc()).first()

    tipo_cambio_moneda_propietario = cotizacion_moneda_origen_propietario[0] if cotizacion_moneda_origen_propietario else 1


    if complemento.habilitar_cobro_remitente:
        create_provision(
            db,
            ProvisionForm(
                orden_carga_id=complemento.orden_carga_id,
                tipo_contraparte_id=remitente_contraparte.id,
                contraparte=complemento.orden_carga.flete.remitente_nombre,
                contraparte_numero_documento=complemento.orden_carga.flete.remitente.numero_documento,  # noqa
                tipo_documento_relacionado_id=tipo_documento_relacionado.id,
                numero_documento_relacionado=complemento.orden_carga_id,
                cuenta_id=tipo_cuenta.id,
                tipo_movimiento_id=tipo_movimiento.id,
                estado=MovimientoEstadoEnum.PROVISION,
                detalle=complemento.remitente_detalle,
                monto=-complemento.remitente_monto,
                moneda_id=complemento.remitente_moneda_id,
                tipo_cambio_moneda=tipo_cambio_moneda_remitente,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en Complemento  # noqa
                fecha_cambio_moneda=datetime.now(),
                complemento_id=complemento.id,
                remitente_id=complemento.orden_carga.flete.remitente_id,
                tipo_movimiento_info=complemento.concepto_descripcion,
                linea_movimiento=TipoAnticipoEnum.EFECTIVO.value,
            ),
            gestor_carga_id,
            modified_by,
        )
    return create_provision(
        db,
        ProvisionForm(
            orden_carga_id=complemento.orden_carga_id,
            tipo_contraparte_id=propietario_contraparte.id,
            contraparte=complemento.orden_carga.propietario.nombre,
            contraparte_numero_documento=complemento.orden_carga.propietario.ruc,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            numero_documento_relacionado=complemento.orden_carga_id,
            cuenta_id=tipo_cuenta.id,
            tipo_movimiento_id=tipo_movimiento.id,
            estado=MovimientoEstadoEnum.PROVISION,
            detalle=complemento.propietario_detalle,
            monto=complemento.propietario_monto,
            moneda_id=complemento.propietario_moneda_id,
            tipo_cambio_moneda=tipo_cambio_moneda_propietario,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en Complemento  # noqa
            fecha_cambio_moneda=datetime.now(),
            complemento_id=complemento.id,
            propietario_id=complemento.orden_carga.propietario_id,
            tipo_movimiento_info=complemento.concepto_descripcion,
            linea_movimiento=TipoAnticipoEnum.EFECTIVO.value,
        ),
        gestor_carga_id,
        modified_by,
    )


def create_provision_by_descuento(
    db: Session,
    descuento: OrdenCargaDescuento,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Optional[Provision]:
    propietario_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.PROPIETARIO.value
    )
    proveedor_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.PROVEEDOR.value
    )
    tipo_documento_relacionado = (
        repositories.get_tipo_documento_relacionado_by_descripcion(db, "OC")
    )
    tipo_cuenta = repositories.get_tipo_cuenta_by_descripcion(
        db, TipoCuentaEnum.VIAJES.value
    )
    tipo_movimiento = repositories.get_tipo_movimiento_by_descripcion(
        db, TipoMovimientoEnum.DESCUENTO.value
    )
    if (
        not propietario_contraparte
        or not proveedor_contraparte
        or not tipo_documento_relacionado
        or not tipo_cuenta
        or not tipo_movimiento
    ):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Tipo de contraparte, doc relacionado, cuenta o movimiento no existe ooooo",
        )

    # Cotización de la moneda proveeodr
    cotizacion_moneda_origen_proveedor = db.query(MonedaCotizacion.cotizacion_moneda).filter(
        MonedaCotizacion.moneda_origen_id == descuento.proveedor_moneda_id
    ).order_by(MonedaCotizacion.fecha.desc()).first()

    tipo_cambio_moneda_proveedor = cotizacion_moneda_origen_proveedor[0] if cotizacion_moneda_origen_proveedor else 1

    # Cotización de la moneda propietario
    cotizacion_moneda_origen_propietario = db.query(MonedaCotizacion.cotizacion_moneda).filter(
        MonedaCotizacion.moneda_origen_id == descuento.propietario_moneda_id
    ).order_by(MonedaCotizacion.fecha.desc()).first()

    tipo_cambio_moneda_propietario = cotizacion_moneda_origen_propietario[0] if cotizacion_moneda_origen_propietario else 1

    if descuento.habilitar_pago_proveedor and descuento.proveedor:
        create_provision(
            db,
            ProvisionForm(
                orden_carga_id=descuento.orden_carga_id,
                tipo_contraparte_id=proveedor_contraparte.id,
                contraparte=descuento.proveedor_nombre,
                contraparte_numero_documento=descuento.proveedor.numero_documento,
                tipo_documento_relacionado_id=tipo_documento_relacionado.id,
                numero_documento_relacionado=descuento.orden_carga_id,
                cuenta_id=tipo_cuenta.id,
                tipo_movimiento_id=tipo_movimiento.id,
                estado=MovimientoEstadoEnum.PROVISION,
                detalle=descuento.proveedor_detalle,
                monto=descuento.proveedor_monto,
                moneda_id=descuento.proveedor_moneda_id,
                tipo_cambio_moneda=tipo_cambio_moneda_proveedor,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en Descuento  # noqa
                fecha_cambio_moneda=datetime.now(),
                descuento_id=descuento.id,
                proveedor_id=descuento.proveedor_id,
                tipo_movimiento_info=descuento.concepto_descripcion,
                linea_movimiento=TipoAnticipoEnum.EFECTIVO.value,
            ),
            gestor_carga_id,
            modified_by,
        )
    return create_provision(
        db,
        ProvisionForm(
            orden_carga_id=descuento.orden_carga_id,
            tipo_contraparte_id=propietario_contraparte.id,
            contraparte=descuento.orden_carga.propietario.nombre,
            contraparte_numero_documento=descuento.orden_carga.propietario.ruc,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            numero_documento_relacionado=descuento.orden_carga_id,
            cuenta_id=tipo_cuenta.id,
            tipo_movimiento_id=tipo_movimiento.id,
            estado=MovimientoEstadoEnum.PROVISION,
            detalle=descuento.propietario_detalle,
            monto=-descuento.propietario_monto,
            moneda_id=descuento.propietario_moneda_id,
            tipo_cambio_moneda=tipo_cambio_moneda_propietario,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en Descuento  # noqa
            fecha_cambio_moneda=datetime.now(),
            descuento_id=descuento.id,
            propietario_id=descuento.orden_carga.propietario_id,
            tipo_movimiento_info=descuento.concepto_descripcion,
            linea_movimiento=TipoAnticipoEnum.EFECTIVO.value,
        ),
        gestor_carga_id,
        modified_by,
    )


def create_provision_by_flete(
    db: Session,
    orden_carga: OrdenCarga,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Optional[Provision]:
    propietario_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.PROPIETARIO.value
    )
    remitente_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.REMITENTE.value
    )
    tipo_documento_relacionado = (
        repositories.get_tipo_documento_relacionado_by_descripcion(db, "OC")
    )
    tipo_cuenta = repositories.get_tipo_cuenta_by_descripcion(
        db, TipoCuentaEnum.VIAJES.value
    )
    tipo_movimiento = repositories.get_tipo_movimiento_by_descripcion(
        db, TipoMovimientoEnum.FLETE.value
    )
    if (
        not propietario_contraparte
        or not remitente_contraparte
        or not tipo_documento_relacionado
        or not tipo_cuenta
        or not tipo_movimiento
    ):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Tipo de contraparte, doc relacionado, cuenta o movimiento no existe",
        )

    # Cotización de la moneda gestor
    cotizacion_moneda_origen_gestor = db.query(MonedaCotizacion.cotizacion_moneda).filter(
        MonedaCotizacion.moneda_origen_id == orden_carga.flete.condicion_gestor_carga_moneda_id
    ).order_by(MonedaCotizacion.fecha.desc()).first()

    tipo_cambio_moneda_gestor = cotizacion_moneda_origen_gestor[0] if cotizacion_moneda_origen_gestor else 1

    # Cotización de la moneda propietario
    cotizacion_moneda_origen = db.query(MonedaCotizacion.cotizacion_moneda).filter(
        MonedaCotizacion.moneda_origen_id == orden_carga.flete.condicion_propietario_moneda_id
    ).order_by(MonedaCotizacion.fecha.desc()).first()

    tipo_cambio_moneda = cotizacion_moneda_origen[0] if cotizacion_moneda_origen else 1

    create_provision(
        db,
        ProvisionForm(
            orden_carga_id=orden_carga.id,
            tipo_contraparte_id=remitente_contraparte.id,
            contraparte=orden_carga.flete.remitente_nombre,
            contraparte_numero_documento=orden_carga.flete.remitente.numero_documento,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            numero_documento_relacionado=orden_carga.id,
            cuenta_id=tipo_cuenta.id,
            tipo_movimiento_id=tipo_movimiento.id,
            estado=MovimientoEstadoEnum.PROVISION,
            detalle=orden_carga.flete_gestor_carga_detalle,
            #monto=-orden_carga.resultado_gestor_carga_total_flete,
            monto=-orden_carga.resultado_gestor_carga_total_flete_oc / orden_carga.flete_tarifa_unidad_conversion_gestor,
            moneda_id=orden_carga.flete.condicion_gestor_cuenta_moneda_id,
            tipo_cambio_moneda=tipo_cambio_moneda_gestor,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en FLETE  # noqa
            fecha_cambio_moneda=datetime.now(),
            remitente_id=orden_carga.flete.remitente_id,
            tipo_movimiento_info=tipo_movimiento.descripcion,
            linea_movimiento=TipoAnticipoEnum.EFECTIVO.value,
        ),
        gestor_carga_id,
        modified_by,
    )
    return create_provision(
        db,
        ProvisionForm(
            orden_carga_id=orden_carga.id,
            tipo_contraparte_id=propietario_contraparte.id,
            contraparte=orden_carga.propietario.nombre,
            contraparte_numero_documento=orden_carga.propietario.ruc,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            numero_documento_relacionado=orden_carga.id,
            cuenta_id=tipo_cuenta.id,
            tipo_movimiento_id=tipo_movimiento.id,
            estado=MovimientoEstadoEnum.PROVISION,
            detalle=orden_carga.flete_propietario_detalle,
            monto=orden_carga.resultado_propietario_total_flete_oc / orden_carga.flete_tarifa_unidad_conversion_propietario,
            moneda_id=orden_carga.flete.condicion_propietario_moneda_id,
            tipo_cambio_moneda=tipo_cambio_moneda,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en FLETE  # noqa
            fecha_cambio_moneda=datetime.now(),
            propietario_id=orden_carga.propietario_id,
            tipo_movimiento_info=tipo_movimiento.descripcion,
            linea_movimiento=TipoAnticipoEnum.EFECTIVO.value,
        ),
        gestor_carga_id,
        modified_by,
    )


def create_provision_by_merma(
    db: Session,
    orden_carga: OrdenCarga,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Optional[Provision]:
    propietario_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.PROPIETARIO.value
    )
    remitente_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.REMITENTE.value
    )
    tipo_documento_relacionado = (
        repositories.get_tipo_documento_relacionado_by_descripcion(db, "OC")
    )
    tipo_cuenta = repositories.get_tipo_cuenta_by_descripcion(
        db, TipoCuentaEnum.VIAJES.value
    )
    tipo_movimiento = repositories.get_tipo_movimiento_by_descripcion(
        db, TipoMovimientoEnum.MERMA.value
    )
    if (
        not propietario_contraparte
        or not remitente_contraparte
        or not tipo_documento_relacionado
        or not tipo_cuenta
        or not tipo_movimiento
    ):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Tipo de contraparte, doc relacionado, cuenta o movimiento no existe",
        )

    # Cotización de la moneda gestor
    cotizacion_moneda_origen_gestor = db.query(MonedaCotizacion.cotizacion_moneda).filter(
        MonedaCotizacion.moneda_origen_id == orden_carga.flete.merma_gestor_cuenta_moneda_id
    ).order_by(MonedaCotizacion.fecha.desc()).first()

    tipo_cambio_moneda_gestor = cotizacion_moneda_origen_gestor[0] if cotizacion_moneda_origen_gestor else 1

        # Cotización de la moneda propietario
    cotizacion_moneda_origen_propietario = db.query(MonedaCotizacion.cotizacion_moneda).filter(
        MonedaCotizacion.moneda_origen_id == orden_carga.flete.merma_propietario_moneda_id
    ).order_by(MonedaCotizacion.fecha.desc()).first()

    tipo_cambio_moneda_propietario = cotizacion_moneda_origen_propietario[0] if cotizacion_moneda_origen_propietario else 1

    create_provision(
        db,
        ProvisionForm(
            orden_carga_id=orden_carga.id,
            tipo_contraparte_id=remitente_contraparte.id,
            contraparte=orden_carga.flete.remitente_nombre,
            contraparte_numero_documento=orden_carga.flete.remitente.numero_documento,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            numero_documento_relacionado=orden_carga.id,
            cuenta_id=tipo_cuenta.id,
            tipo_movimiento_id=tipo_movimiento.id,
            estado=MovimientoEstadoEnum.PROVISION,
            detalle=orden_carga.merma_gestor_carga_detalle,
            monto=orden_carga.resultado_gestor_carga_merma_valor_total_by_movimiento,
            moneda_id=orden_carga.flete.condicion_gestor_cuenta_moneda_id,
            tipo_cambio_moneda=tipo_cambio_moneda_gestor,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en FLETE  # noqa
            fecha_cambio_moneda=datetime.now(),
            remitente_id=orden_carga.flete.remitente_id,
            tipo_movimiento_info=tipo_movimiento.descripcion,
            linea_movimiento=TipoAnticipoEnum.EFECTIVO.value,
        ),
        gestor_carga_id,
        modified_by,
    )
    return create_provision(
        db,
        ProvisionForm(
            orden_carga_id=orden_carga.id,
            tipo_contraparte_id=propietario_contraparte.id,
            contraparte=orden_carga.propietario.nombre,
            contraparte_numero_documento=orden_carga.propietario.ruc,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            numero_documento_relacionado=orden_carga.id,
            cuenta_id=tipo_cuenta.id,
            tipo_movimiento_id=tipo_movimiento.id,
            estado=MovimientoEstadoEnum.PROVISION,
            detalle=orden_carga.merma_propietario_detalle,
            monto=-orden_carga.resultado_propietario_merma_valor_total_by_movimiento,
            moneda_id=orden_carga.flete.condicion_propietario_moneda_id,
            tipo_cambio_moneda=tipo_cambio_moneda_propietario,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en FLETE  # noqa
            fecha_cambio_moneda=datetime.now(),
            propietario_id=orden_carga.propietario_id,
            tipo_movimiento_info=tipo_movimiento.descripcion,
            linea_movimiento=TipoAnticipoEnum.EFECTIVO.value,
        ),
        gestor_carga_id,
        modified_by,
    )


def borrar_provisiones_by_conciliacion_oc(
    db: Session,
    orden_carga: OrdenCarga,
    gestor_carga_id: Optional[int],
    modified_by: str,
):
    db.query(Provision).filter(Provision.orden_carga_id == orden_carga.id).delete()
    db.commit()

def create_provision(
    db: Session,
    data: ProvisionForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Optional[Provision]:
    # Provision no puede tener monto 0
    logger.info("create_provision" + data.detalle)
    if int(data.monto) != 0:
        gestor_id = gestor_carga_id if gestor_carga_id else data.gestor_carga_id
        if not gestor_id:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Debe elegir un Gestor de carga"
            )
        return repositories.create_provision(db, data, gestor_id, modified_by)
    return None
