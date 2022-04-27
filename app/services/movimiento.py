import os
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, cast

from fastapi import HTTPException  # type: ignore
from openpyxl import Workbook  # type: ignore
from openpyxl.styles import Font  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.config import REPORTS_FOLDER
from app.enums import MovimientoEstadoEnum, TipoContraparteEnum, TipoMovimientoEnum
from app.models import (
    Movimiento,
    OrdenCarga,
    OrdenCargaAnticipoRetirado,
    OrdenCargaComplemento,
    OrdenCargaDescuento,
)
from app.schemas import MovimientoForm
from app.schemas.date_model import Date


def get_movimiento_list(
    db: Session, gestor_carga_id: Optional[int]
) -> List[Movimiento]:
    if gestor_carga_id:
        return repositories.get_movimiento_list_by_gestor_carga_id(db, gestor_carga_id)
    return repositories.get_movimiento_list(db)


def get_movimiento_list_by_estado_cuenta(
    db: Session,
    tipo_contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    estado: str,
    gestor_carga_id: Optional[int],
) -> List[Movimiento]:
    if gestor_carga_id:
        return repositories.get_movimiento_list_by_contraparte_and_gestor_carga_id(
            db,
            tipo_contraparte_id,
            contraparte,
            contraparte_numero_documento,
            estado,
            gestor_carga_id,
        )
    return repositories.get_movimiento_list_by_contraparte(
        db, tipo_contraparte_id, contraparte, contraparte_numero_documento, estado
    )


def get_movimiento_list_by_liquidacion(
    db: Session,
    liquidacion_id: int,
    estado: str,
    gestor_carga_id: Optional[int],
) -> List[Movimiento]:
    if gestor_carga_id:
        return repositories.get_movimiento_list_by_liquidacion_and_gestor_carga_id(
            db,
            liquidacion_id,
            estado,
            gestor_carga_id,
        )
    return repositories.get_movimiento_list_by_liquidacion(db, liquidacion_id, estado)


def create_movimiento(
    db: Session,
    data: MovimientoForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Optional[Movimiento]:
    # Movimiento no puede tener monto 0
    if int(data.monto) != 0:
        gestor_id = gestor_carga_id if gestor_carga_id else data.gestor_carga_id
        if not gestor_id:
            raise HTTPException(
                status_code=409, detail="Debe elegir un Gestor de carga"
            )
        return repositories.create_movimiento(db, data, gestor_id, modified_by)
    return None


def create_movimiento_by_anticipo(
    db: Session,
    anticipo: OrdenCargaAnticipoRetirado,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Optional[Movimiento]:
    propietario_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.PROPIETARIO.value
    )
    proveedor_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.PROVEEDOR.value
    )
    tipo_documento_relacionado = (
        repositories.get_tipo_documento_relacionado_by_descripcion(db, "OC")
    )
    tipo_cuenta = repositories.get_tipo_cuenta_by_descripcion(db, "Viajes")
    tipo_movimiento = repositories.get_tipo_movimiento_by_descripcion(
        db, TipoMovimientoEnum.ANTICIPO.value
    )
    if (
        not propietario_contraparte
        or not proveedor_contraparte
        or not tipo_documento_relacionado
        or not tipo_cuenta
        or not tipo_movimiento
    ):
        raise HTTPException(
            status_code=404,
            detail="Tipo de contraparte, doc relacionado, cuenta o movimiento no existe",
        )
    create_movimiento(
        db,
        MovimientoForm(
            orden_carga_id=anticipo.orden_carga_id,
            tipo_contraparte_id=proveedor_contraparte.id,
            contraparte=anticipo.proveedor_nombre,
            contraparte_numero_documento=anticipo.punto_venta.proveedor.numero_documento,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            numero_documento_relacionado=anticipo.orden_carga_id,
            cuenta_id=tipo_cuenta.id,
            tipo_movimiento_id=tipo_movimiento.id,
            estado=MovimientoEstadoEnum.PENDIENTE,
            detalle=anticipo.detalle,
            monto=anticipo.monto_retirado,
            moneda_id=anticipo.moneda_id,
            tipo_cambio_moneda=1,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en Descuento  # noqa
            fecha_cambio_moneda=datetime.now(),
            anticipo_id=anticipo.id,
            proveedor_id=anticipo.punto_venta.proveedor_id,
        ),
        gestor_carga_id,
        modified_by,
    )
    return create_movimiento(
        db,
        MovimientoForm(
            orden_carga_id=anticipo.orden_carga_id,
            tipo_contraparte_id=propietario_contraparte.id,
            contraparte=anticipo.orden_carga.camion_propietario_nombre,
            contraparte_numero_documento=anticipo.orden_carga.camion.propietario_ruc,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            numero_documento_relacionado=anticipo.orden_carga_id,
            cuenta_id=tipo_cuenta.id,
            tipo_movimiento_id=tipo_movimiento.id,
            estado=MovimientoEstadoEnum.PENDIENTE,
            detalle=anticipo.detalle,
            monto=-anticipo.monto_retirado,
            moneda_id=anticipo.moneda_id,
            tipo_cambio_moneda=1,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en anticipos  # noqa
            fecha_cambio_moneda=datetime.now(),
            anticipo_id=anticipo.id,
            propietario_id=anticipo.orden_carga.camion.propietario_id,
        ),
        gestor_carga_id,
        modified_by,
    )


def create_movimiento_by_flete(
    db: Session,
    orden_carga: OrdenCarga,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Optional[Movimiento]:
    propietario_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.PROPIETARIO.value
    )
    remitente_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.REMITENTE.value
    )
    tipo_documento_relacionado = (
        repositories.get_tipo_documento_relacionado_by_descripcion(db, "OC")
    )
    tipo_cuenta = repositories.get_tipo_cuenta_by_descripcion(db, "Viajes")
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
            status_code=404,
            detail="Tipo de contraparte, doc relacionado, cuenta o movimiento no existe",
        )
    create_movimiento(
        db,
        MovimientoForm(
            orden_carga_id=orden_carga.id,
            tipo_contraparte_id=remitente_contraparte.id,
            contraparte=orden_carga.flete.remitente_nombre,
            contraparte_numero_documento=orden_carga.flete.remitente.numero_documento,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            numero_documento_relacionado=orden_carga.id,
            cuenta_id=tipo_cuenta.id,
            tipo_movimiento_id=tipo_movimiento.id,
            estado=MovimientoEstadoEnum.PENDIENTE,
            detalle=orden_carga.flete_gestor_carga_detalle,
            monto=-orden_carga.resultado_gestor_carga_total_flete,
            moneda_id=orden_carga.flete.condicion_gestor_cuenta_moneda_id,
            tipo_cambio_moneda=1,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en FLETE  # noqa
            fecha_cambio_moneda=datetime.now(),
            remitente_id=orden_carga.flete.remitente_id,
        ),
        gestor_carga_id,
        modified_by,
    )
    return create_movimiento(
        db,
        MovimientoForm(
            orden_carga_id=orden_carga.id,
            tipo_contraparte_id=propietario_contraparte.id,
            contraparte=orden_carga.camion_propietario_nombre,
            contraparte_numero_documento=orden_carga.camion.propietario_ruc,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            numero_documento_relacionado=orden_carga.id,
            cuenta_id=tipo_cuenta.id,
            tipo_movimiento_id=tipo_movimiento.id,
            estado=MovimientoEstadoEnum.PENDIENTE,
            detalle=orden_carga.flete_propietario_detalle,
            monto=orden_carga.resultado_propietario_total_flete,
            moneda_id=orden_carga.flete.condicion_propietario_moneda_id,
            tipo_cambio_moneda=1,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en FLETE  # noqa
            fecha_cambio_moneda=datetime.now(),
            propietario_id=orden_carga.camion.propietario_id,
        ),
        gestor_carga_id,
        modified_by,
    )


def create_movimiento_by_complemento(
    db: Session,
    complemento: OrdenCargaComplemento,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Optional[Movimiento]:
    propietario_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.PROPIETARIO.value
    )
    remitente_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.REMITENTE.value
    )
    tipo_documento_relacionado = (
        repositories.get_tipo_documento_relacionado_by_descripcion(db, "OC")
    )
    tipo_cuenta = repositories.get_tipo_cuenta_by_descripcion(db, "Viajes")
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
            status_code=404,
            detail="Tipo de contraparte, doc relacionado, cuenta o movimiento no existe",
        )
    if complemento.habilitar_cobro_remitente:
        create_movimiento(
            db,
            MovimientoForm(
                orden_carga_id=complemento.orden_carga_id,
                tipo_contraparte_id=remitente_contraparte.id,
                contraparte=complemento.orden_carga.flete.remitente_nombre,
                contraparte_numero_documento=complemento.orden_carga.flete.remitente.numero_documento,  # noqa
                tipo_documento_relacionado_id=tipo_documento_relacionado.id,
                numero_documento_relacionado=complemento.orden_carga_id,
                cuenta_id=tipo_cuenta.id,
                tipo_movimiento_id=tipo_movimiento.id,
                estado=MovimientoEstadoEnum.PENDIENTE,
                detalle=complemento.remitente_detalle,
                monto=-complemento.remitente_monto,
                moneda_id=complemento.remitente_moneda_id,
                tipo_cambio_moneda=1,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en Complemento  # noqa
                fecha_cambio_moneda=datetime.now(),
                complemento_id=complemento.id,
                remitente_id=complemento.orden_carga.flete.remitente_id,
            ),
            gestor_carga_id,
            modified_by,
        )
    return create_movimiento(
        db,
        MovimientoForm(
            orden_carga_id=complemento.orden_carga_id,
            tipo_contraparte_id=propietario_contraparte.id,
            contraparte=complemento.orden_carga.camion_propietario_nombre,
            contraparte_numero_documento=complemento.orden_carga.camion.propietario_ruc,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            numero_documento_relacionado=complemento.orden_carga_id,
            cuenta_id=tipo_cuenta.id,
            tipo_movimiento_id=tipo_movimiento.id,
            estado=MovimientoEstadoEnum.PENDIENTE,
            detalle=complemento.propietario_detalle,
            monto=complemento.propietario_monto,
            moneda_id=complemento.propietario_moneda_id,
            tipo_cambio_moneda=1,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en Complemento  # noqa
            fecha_cambio_moneda=datetime.now(),
            complemento_id=complemento.id,
            propietario_id=complemento.orden_carga.camion.propietario_id,
        ),
        gestor_carga_id,
        modified_by,
    )


def create_movimiento_by_descuento(
    db: Session,
    descuento: OrdenCargaDescuento,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Optional[Movimiento]:
    propietario_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.PROPIETARIO.value
    )
    proveedor_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.PROVEEDOR.value
    )
    tipo_documento_relacionado = (
        repositories.get_tipo_documento_relacionado_by_descripcion(db, "OC")
    )
    tipo_cuenta = repositories.get_tipo_cuenta_by_descripcion(db, "Viajes")
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
            status_code=404,
            detail="Tipo de contraparte, doc relacionado, cuenta o movimiento no existe",
        )
    if descuento.habilitar_pago_proveedor and descuento.proveedor:
        create_movimiento(
            db,
            MovimientoForm(
                orden_carga_id=descuento.orden_carga_id,
                tipo_contraparte_id=proveedor_contraparte.id,
                contraparte=descuento.proveedor_nombre,
                contraparte_numero_documento=descuento.proveedor.numero_documento,
                tipo_documento_relacionado_id=tipo_documento_relacionado.id,
                numero_documento_relacionado=descuento.orden_carga_id,
                cuenta_id=tipo_cuenta.id,
                tipo_movimiento_id=tipo_movimiento.id,
                estado=MovimientoEstadoEnum.PENDIENTE,
                detalle=descuento.proveedor_detalle,
                monto=descuento.proveedor_monto,
                moneda_id=descuento.proveedor_moneda_id,
                tipo_cambio_moneda=1,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en Descuento  # noqa
                fecha_cambio_moneda=datetime.now(),
                descuento_id=descuento.id,
                proveedor_id=descuento.proveedor_id,
            ),
            gestor_carga_id,
            modified_by,
        )
    return create_movimiento(
        db,
        MovimientoForm(
            orden_carga_id=descuento.orden_carga_id,
            tipo_contraparte_id=propietario_contraparte.id,
            contraparte=descuento.orden_carga.camion_propietario_nombre,
            contraparte_numero_documento=descuento.orden_carga.camion.propietario_ruc,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            numero_documento_relacionado=descuento.orden_carga_id,
            cuenta_id=tipo_cuenta.id,
            tipo_movimiento_id=tipo_movimiento.id,
            estado=MovimientoEstadoEnum.PENDIENTE,
            detalle=descuento.propietario_detalle,
            monto=-descuento.propietario_monto,
            moneda_id=descuento.propietario_moneda_id,
            tipo_cambio_moneda=1,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en Descuento  # noqa
            fecha_cambio_moneda=datetime.now(),
            descuento_id=descuento.id,
            propietario_id=descuento.orden_carga.camion.propietario_id,
        ),
        gestor_carga_id,
        modified_by,
    )


def create_movimiento_by_merma(
    db: Session,
    orden_carga: OrdenCarga,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Optional[Movimiento]:
    propietario_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.PROPIETARIO.value
    )
    remitente_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.REMITENTE.value
    )
    tipo_documento_relacionado = (
        repositories.get_tipo_documento_relacionado_by_descripcion(db, "OC")
    )
    tipo_cuenta = repositories.get_tipo_cuenta_by_descripcion(db, "Viajes")
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
            status_code=404,
            detail="Tipo de contraparte, doc relacionado, cuenta o movimiento no existe",
        )
    create_movimiento(
        db,
        MovimientoForm(
            orden_carga_id=orden_carga.id,
            tipo_contraparte_id=remitente_contraparte.id,
            contraparte=orden_carga.flete.remitente_nombre,
            contraparte_numero_documento=orden_carga.flete.remitente.numero_documento,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            numero_documento_relacionado=orden_carga.id,
            cuenta_id=tipo_cuenta.id,
            tipo_movimiento_id=tipo_movimiento.id,
            estado=MovimientoEstadoEnum.PENDIENTE,
            detalle=orden_carga.merma_gestor_carga_detalle,
            monto=orden_carga.resultado_gestor_carga_merma_valor_total,
            moneda_id=orden_carga.flete.condicion_gestor_cuenta_moneda_id,
            tipo_cambio_moneda=1,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en FLETE  # noqa
            fecha_cambio_moneda=datetime.now(),
            remitente_id=orden_carga.flete.remitente_id,
        ),
        gestor_carga_id,
        modified_by,
    )
    return create_movimiento(
        db,
        MovimientoForm(
            orden_carga_id=orden_carga.id,
            tipo_contraparte_id=propietario_contraparte.id,
            contraparte=orden_carga.camion_propietario_nombre,
            contraparte_numero_documento=orden_carga.camion.propietario_ruc,
            tipo_documento_relacionado_id=tipo_documento_relacionado.id,
            numero_documento_relacionado=orden_carga.id,
            cuenta_id=tipo_cuenta.id,
            tipo_movimiento_id=tipo_movimiento.id,
            estado=MovimientoEstadoEnum.PENDIENTE,
            detalle=orden_carga.merma_propietario_detalle,
            monto=-orden_carga.resultado_propietario_merma_valor_total,
            moneda_id=orden_carga.flete.condicion_propietario_moneda_id,
            tipo_cambio_moneda=1,  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en FLETE  # noqa
            fecha_cambio_moneda=datetime.now(),
            propietario_id=orden_carga.camion.propietario_id,
        ),
        gestor_carga_id,
        modified_by,
    )


def create_movimiento_by_tipo_documento_relacionado_otro(
    db: Session,
    data: MovimientoForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Optional[Movimiento]:
    tipo_contraparte = repositories.get_tipo_contraparte_by_descripcion(
        db, TipoContraparteEnum.OTRO.value
    )
    tipo_documento_relacionado = (
        repositories.get_tipo_documento_relacionado_by_descripcion(db, "Otro")
    )
    tipo_cuenta = repositories.get_tipo_cuenta_by_descripcion(db, "Viajes")
    tipo_movimiento = repositories.get_tipo_movimiento_by_descripcion(
        db, TipoMovimientoEnum.OTRO.value
    )
    if (
        not tipo_contraparte
        or not tipo_documento_relacionado
        or not tipo_cuenta
        or not tipo_movimiento
    ):
        raise HTTPException(
            status_code=404,
            detail="Tipo de contraparte, doc relacionado, cuenta o movimiento no existe",
        )
    exists = None
    if data.es_creacion_contraparte:
        exists = repositories.get_contraparte_by_contraparte_and_tipo_contraparte_id(
            db, data.contraparte, tipo_contraparte.id
        )
    if exists:
        raise HTTPException(
            status_code=409,
            detail=f"La contraparte {data.contraparte} ya existe",
        )
    numero_documento_relacionado = (
        repositories.get_movimiento_count_by_tipo_documento_relacionado_id(
            db, tipo_documento_relacionado.id
        )
        + 1
    )
    fecha = cast(Date, datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    data.tipo_documento_relacionado_id = tipo_documento_relacionado.id
    data.numero_documento_relacionado = numero_documento_relacionado
    data.cuenta_id = tipo_cuenta.id
    data.tipo_movimiento_id = tipo_movimiento.id
    data.es_editable = True
    data.tipo_cambio_moneda = Decimal(
        1
    )  # TODO: poner el tipo de cambio correcto en cuando se maneje tipo de cambio en Descuento  # noqa
    data.fecha_cambio_moneda = fecha
    if not data.fecha:
        data.fecha = fecha
    return create_movimiento(
        db,
        data,
        gestor_carga_id,
        modified_by,
    )


def create_movimiento_by_conciliacion_oc(
    db: Session,
    orden_carga: OrdenCarga,
    gestor_carga_id: Optional[int],
    modified_by: str,
):
    for complemento in orden_carga.complementos:
        create_movimiento_by_complemento(db, complemento, gestor_carga_id, modified_by)
    for descuento in orden_carga.descuentos:
        create_movimiento_by_descuento(db, descuento, gestor_carga_id, modified_by)
    create_movimiento_by_flete(db, orden_carga, gestor_carga_id, modified_by)
    create_movimiento_by_merma(db, orden_carga, gestor_carga_id, modified_by)


def get_movimiento_by_id(db: Session, id: int) -> Movimiento:
    obj = repositories.get_movimiento_by_id(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return obj


def edit_movimiento(
    id: int,
    db: Session,
    data: MovimientoForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Movimiento:
    gestor_id = gestor_carga_id if gestor_carga_id else data.gestor_carga_id
    if not gestor_id:
        raise HTTPException(status_code=409, detail="Debe elegir un Gestor de carga")
    to_edit_obj = get_movimiento_by_id(db, id)
    return repositories.edit_movimiento(to_edit_obj, db, data, gestor_id, modified_by)


def delete_movimiento(db: Session, id: int, modified_by: str) -> Movimiento:
    co = get_movimiento_by_id(db, id)
    return repositories.delete_movimiento(co, db, modified_by)


def get_movimiento_reports(db: Session) -> str:
    datalist = repositories.get_movimiento_list(db)
    wb = Workbook()
    ws = wb.active

    title_cell = ws.cell(row=1, column=1)
    title_cell.value = "ID"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=2)
    title_cell.value = "Nombre de Cuenta"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=3)
    title_cell.value = "Titular"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=4)
    title_cell.value = "Movimiento"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=5)
    title_cell.value = "Crédito"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=6)
    title_cell.value = "Débito"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=7)
    title_cell.value = "Saldo"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=8)
    title_cell.value = "Pendiente"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=9)
    title_cell.value = "Usuario creación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=10)
    title_cell.value = "Fecha creación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=11)
    title_cell.value = "Usuario modificación"
    title_cell.font = Font(bold=True)

    title_cell = ws.cell(row=1, column=12)
    title_cell.value = "Fecha modificación"
    title_cell.font = Font(bold=True)

    for row, item in enumerate(datalist):
        value_cell = ws.cell(row=row + 2, column=1)
        value_cell.value = item.id

        value_cell = ws.cell(row=row + 2, column=2)
        value_cell.value = item.numero_cuenta

        value_cell = ws.cell(row=row + 2, column=3)
        value_cell.value = item.titular

        value_cell = ws.cell(row=row + 2, column=4)
        value_cell.value = item.nombre

        value_cell = ws.cell(row=row + 2, column=5)
        value_cell.value = item.credito

        value_cell = ws.cell(row=row + 2, column=6)
        value_cell.value = item.debito

        value_cell = ws.cell(row=row + 2, column=7)
        value_cell.value = item.saldo_confirmado

        value_cell = ws.cell(row=row + 2, column=8)
        value_cell.value = item.saldo_provisional

        value_cell = ws.cell(row=row + 2, column=9)
        value_cell.value = item.created_by

        value_cell = ws.cell(row=row + 2, column=10)
        value_cell.value = item.created_at

        value_cell = ws.cell(row=row + 2, column=11)
        value_cell.value = item.modified_by

        value_cell = ws.cell(row=row + 2, column=12)
        value_cell.value = item.modified_at

    ws.auto_filter.ref = ws.dimensions
    filename = "movimiento_reports.xls"
    # Save the file
    wb.save(os.path.join(REPORTS_FOLDER, filename))
    return filename
