from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum, OrdenCargaEstadoEnum
from app.models import Flete, OrdenCarga
from app.schemas import OrdenCargaForm
from app.schemas.orden_carga import OrdenCargaEditForm


def get_orden_carga_list(db: Session) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter(OrdenCarga.estado != EstadoEnum.ELIMINADO.value)
        .order_by(OrdenCarga.created_by)
        .all()
    )


def get_orden_carga_by_id(db: Session, id: int) -> Optional[OrdenCarga]:
    return db.query(OrdenCarga).filter(OrdenCarga.id == id).first()


def create_orden_carga(
    db: Session,
    data: OrdenCargaForm,
    flete: Flete,
    gestor_carga_id: int,
    modified_by: str,
) -> OrdenCarga:
    obj = OrdenCarga(
        camion_id=data.camion_id,
        semi_id=data.semi_id,
        flete_id=data.flete_id,
        cantidad_nominada=data.cantidad_nominada,
        comentarios=data.comentarios,
        origen_id=flete.origen_id,
        destino_id=flete.destino_id,
        gestor_carga_id=gestor_carga_id,
        fecha_nuevo=datetime.now(),
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_orden_carga(
    obj: OrdenCarga,
    db: Session,
    data: OrdenCargaEditForm,
    gestor_carga_id: int,
    modified_by: str,
) -> OrdenCarga:
    if data.camion_id and data.semi_id and data.flete_id:
        obj.camion_id = data.camion_id
        obj.semi_id = data.semi_id
        obj.flete_id = data.flete_id
        obj.cantidad_nominada = data.cantidad_nominada
        obj.comentarios = data.comentarios
        obj.origen_id = data.origen_id
        obj.destino_id = data.destino_id
        obj.gestor_carga_id = gestor_carga_id
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.refresh(obj)
    return obj


def change_orden_carga_status(
    obj: OrdenCarga,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> OrdenCarga:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    return change_orden_carga_status(obj, db, EstadoEnum.ELIMINADO, modified_by)


def change_orden_carga_anticipos_liberados(
    obj: OrdenCarga,
    db: Session,
    anticipos_liberados: bool,
    modified_by: str,
) -> OrdenCarga:
    obj.anticipos_liberados = anticipos_liberados
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def aceptar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    obj.fecha_aceptado = datetime.now()
    return change_orden_carga_status(obj, db, EstadoEnum.ACEPTADO, modified_by)


def cancelar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    obj.fecha_cancelado = datetime.now()
    return change_orden_carga_status(obj, db, EstadoEnum.CANCELADO, modified_by)


def conciliar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    obj.fecha_conciliado = datetime.now()
    return change_orden_carga_status(obj, db, EstadoEnum.CONCILIADO, modified_by)


def contabilizar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    obj.fecha_contabilizado = datetime.now()
    return change_orden_carga_status(obj, db, EstadoEnum.CONTABILIZADO, modified_by)


def arribado_a_cargar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    obj.orden_carga_estado = OrdenCargaEstadoEnum.ARRIBADO_A_CARGAR
    obj.fecha_arribado_a_cargar = datetime.now()
    return change_orden_carga_status(obj, db, EstadoEnum.EN_PROCESO, modified_by)


def arribado_a_descargar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    obj.estado = EstadoEnum.EN_PROCESO
    obj.orden_carga_estado = OrdenCargaEstadoEnum.ARRIBADO_A_DESCARGAR
    obj.fecha_arribado_a_descargar = datetime.now()
    return change_orden_carga_status(obj, db, EstadoEnum.EN_PROCESO, modified_by)


def cargar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    obj.estado = EstadoEnum.EN_PROCESO
    obj.orden_carga_estado = OrdenCargaEstadoEnum.CARGADO
    obj.fecha_cargado = datetime.now()
    return change_orden_carga_status(obj, db, EstadoEnum.EN_PROCESO, modified_by)


def descargar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    obj.estado = EstadoEnum.EN_PROCESO
    obj.orden_carga_estado = OrdenCargaEstadoEnum.DESCARGADO
    obj.fecha_descargado = datetime.now()
    return change_orden_carga_status(obj, db, EstadoEnum.EN_PROCESO, modified_by)


def finalizar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    obj.fecha_finalizado = datetime.now()
    return change_orden_carga_status(obj, db, EstadoEnum.FINALIZADO, modified_by)


def liquidar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    obj.fecha_liquidado = datetime.now()
    return change_orden_carga_status(obj, db, EstadoEnum.LIQUIDADO, modified_by)
