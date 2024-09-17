from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore

from app.enums import LiquidacionEstadoEnum, LiquidacionEtapaEnum
from app.models import Liquidacion
from app.schemas import LiquidacionForm


def get_liquidacion_list(db: Session, gestor_carga_id: Optional[int] = None) -> List[Liquidacion]:
    if gestor_carga_id:
        return get_liquidacion_list_by_gestor_carga_id(db, gestor_carga_id)
    else:
        return (
            db.query(Liquidacion)
            .filter(Liquidacion.estado != LiquidacionEstadoEnum.ELIMINADO.value)
            .order_by(Liquidacion.created_at.desc(), Liquidacion.contraparte)
            .all()
        )


def get_liquidacion_list_by_contraparte(
    db: Session,
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    etapa: str,
) -> List[Liquidacion]:
    return (
        db.query(Liquidacion)
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
                Liquidacion.etapa == etapa,
                Liquidacion.estado != LiquidacionEstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(Liquidacion.contraparte, Liquidacion.created_at)
        .all()
    )


def get_liquidacion_list_by_contraparte_and_gestor_carga_id(
    db: Session,
    tipo_contraparte_id: int,
    contraparte_id: int,
    contraparte: str,
    contraparte_numero_documento: str,
    etapa: str,
    gestor_carga_id: int,
) -> List[Liquidacion]:
    return (
        db.query(Liquidacion)
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
                Liquidacion.etapa == etapa,
                Liquidacion.gestor_carga_id == gestor_carga_id,
                Liquidacion.estado != LiquidacionEstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(Liquidacion.contraparte, Liquidacion.created_at)
        .all()
    )


def get_liquidacion_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: int
) -> List[Liquidacion]:
    return (
        db.query(Liquidacion)
        .filter(
            and_(
                Liquidacion.gestor_carga_id == gestor_carga_id,
                Liquidacion.estado != LiquidacionEstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(Liquidacion.created_at.desc(), Liquidacion.contraparte )
        .all()
    )


def get_liquidacion_by_id(db: Session, id: int) -> Optional[Liquidacion]:
    return db.query(Liquidacion).get(id)


def create_liquidacion(
    db: Session,
    data: LiquidacionForm,
    gestor_carga_id: int,
    modified_by: str,
) -> Liquidacion:
    obj = Liquidacion(
        tipo_contraparte_id=data.tipo_contraparte_id,
        contraparte=data.contraparte,
        contraparte_numero_documento=data.contraparte_numero_documento,
        moneda_id=data.moneda_id,
        # IDs para referencia a las tablas de las contraparte
        chofer_id=data.chofer_id,
        gestor_carga_id=gestor_carga_id,
        propietario_id=data.propietario_id,
        proveedor_id=data.proveedor_id,
        remitente_id=data.remitente_id,
        estado=LiquidacionEstadoEnum.EN_REVISION.value,
        etapa=LiquidacionEtapaEnum.EN_PROCESO.value,
        created_by=modified_by,
        modified_by=modified_by,
        pago_cobro=data.monto,
        #es_pago_cobro=data.es_pago_cobro
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_liquidacion(
    obj: Liquidacion,
    db: Session,
    data: LiquidacionForm,
    gestor_carga_id: int,
    modified_by: str,
) -> Liquidacion:
    obj.tipo_contraparte_id = data.tipo_contraparte_id
    obj.contraparte = data.contraparte
    obj.contraparte_numero_documento = data.contraparte_numero_documento
    obj.moneda_id = data.moneda_id
    # IDs para referencia a las tablas de las contraparte
    obj.chofer_id = data.chofer_id
    obj.propietario_id = data.propietario_id
    obj.proveedor_id = data.proveedor_id
    obj.remitente_id = data.remitente_id
    obj.gestor_carga_id = gestor_carga_id
    obj.pago_cobro = data.monto
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def change_liquidacion_status(
    obj: Liquidacion,
    db: Session,
    status: LiquidacionEstadoEnum,
    modified_by: str,
) -> Liquidacion:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_liquidacion(
    obj: Liquidacion,
    db: Session,
    modified_by: str,
) -> Liquidacion:
    return change_liquidacion_status(
        obj, db, LiquidacionEstadoEnum.ELIMINADO, modified_by
    )
