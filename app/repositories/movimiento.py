from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore

from app.enums import MovimientoEstadoEnum
from app.models import Movimiento
from app.schemas import MovimientoForm


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
    contraparte: str,
    contraparte_numero_documento: str,
    estado: str,
) -> List[Movimiento]:
    return (
        db.query(Movimiento)
        .filter(
            and_(
                Movimiento.tipo_contraparte_id == tipo_contraparte_id,
                Movimiento.contraparte == contraparte,
                Movimiento.contraparte_numero_documento == contraparte_numero_documento,
                Movimiento.estado == estado,
            )
        )
        .order_by(Movimiento.contraparte, Movimiento.liquidacion_id)
        .all()
    )


def get_movimiento_list_by_contraparte_and_gestor_carga_id(
    db: Session,
    tipo_contraparte_id: int,
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
                Movimiento.contraparte == contraparte,
                Movimiento.contraparte_numero_documento == contraparte_numero_documento,
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
    moneda_id: Optional[int],
    gestor_carga_id: int,
    modified_by: str,
) -> Movimiento:
    obj.monto = monto
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
