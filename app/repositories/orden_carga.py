from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Query, Session  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore
from sqlalchemy.sql.expression import true  # type: ignore

from app.enums import EstadoEnum, OrdenCargaEstadoEnum
from app.models import Camion, Flete, OrdenCarga
from app.schemas import OrdenCargaEditForm, OrdenCargaForm

from .orden_carga_estado_historial import create_orden_carga_estado_historial


def get_orden_carga_list(db: Session) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter(OrdenCarga.estado != EstadoEnum.ELIMINADO.value)
        .order_by(OrdenCarga.created_by)
        .all()
    )


def get_orden_carga_aceptada_count_by_camion_id(
    db: Session, camion_id: int
) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter(
            and_(
                OrdenCarga.camion_id == camion_id,
                or_(
                    OrdenCarga.estado == EstadoEnum.ACEPTADO.value,
                    OrdenCarga.estado == EstadoEnum.EN_PROCESO.value,
                    OrdenCarga.estado == EstadoEnum.FINALIZADO.value,
                ),
            )
        )
        .count()
    )


def get_orden_carga_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: Optional[int]
) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter(
            and_(
                OrdenCarga.gestor_carga_id == gestor_carga_id,
                OrdenCarga.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(OrdenCarga.created_by)
        .all()
    )


def get_orden_carga_by_id(db: Session, id: int) -> Optional[OrdenCarga]:
    return db.query(OrdenCarga).filter(OrdenCarga.id == id).first()


def get_orden_carga_with_anticipo_liberado_by_chofer_id_query(
    db: Session, chofer_id: int
) -> Query:
    return (
        db.query(OrdenCarga)
        .join(OrdenCarga.camion)
        .filter(
            and_(
                Camion.chofer_id == chofer_id,
                OrdenCarga.anticipos_liberados == true(),
                or_(
                    OrdenCarga.estado == EstadoEnum.ACEPTADO.value,
                    OrdenCarga.estado == EstadoEnum.EN_PROCESO.value,
                    OrdenCarga.estado == EstadoEnum.FINALIZADO.value,
                ),
            )
        )
        .order_by(OrdenCarga.created_by)
    )


def get_orden_carga_with_anticipo_liberado_count_by_chofer_id(
    db: Session, chofer_id: int
) -> int:
    return get_orden_carga_with_anticipo_liberado_by_chofer_id_query(
        db, chofer_id
    ).count()


def get_orden_carga_with_anticipo_liberado_list_by_chofer_id(
    db: Session, chofer_id: int
) -> List[OrdenCarga]:
    return get_orden_carga_with_anticipo_liberado_by_chofer_id_query(
        db, chofer_id
    ).all()


def get_orden_carga_with_anticipo_liberado_by_propietario_id_query(
    db: Session, propietario_id: int
) -> Query:
    return (
        db.query(OrdenCarga)
        .join(OrdenCarga.camion)
        .filter(
            and_(
                Camion.propietario_id == propietario_id,
                OrdenCarga.anticipos_liberados == true(),
                or_(
                    OrdenCarga.estado == EstadoEnum.ACEPTADO.value,
                    OrdenCarga.estado == EstadoEnum.EN_PROCESO.value,
                    OrdenCarga.estado == EstadoEnum.FINALIZADO.value,
                ),
            )
        )
        .order_by(OrdenCarga.created_by)
    )


def get_orden_carga_with_anticipo_liberado_count_by_propietario_id(
    db: Session, propietario_id: int
) -> int:
    return get_orden_carga_with_anticipo_liberado_by_propietario_id_query(
        db, propietario_id
    ).count()


def get_orden_carga_with_anticipo_liberado_list_by_propietario_id(
    db: Session, propietario_id: int
) -> List[OrdenCarga]:
    return get_orden_carga_with_anticipo_liberado_by_propietario_id_query(
        db, propietario_id
    ).all()


def create_orden_carga(
    db: Session,
    data: OrdenCargaForm,
    flete: Flete,
    gestor_carga_id: Optional[int],
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
        # INICIO Cantidad y Flete
        # inicio - Condiciones para el Gestor de Carga
        condicion_gestor_carga_moneda_id=flete.condicion_gestor_carga_moneda_id,
        condicion_gestor_carga_tarifa=flete.condicion_gestor_carga_tarifa,
        # fin - Condiciones para el Gestor de Cuenta
        # inicio - Condiciones para el Propietario
        condicion_propietario_moneda_id=flete.condicion_propietario_moneda_id,
        condicion_propietario_tarifa=flete.condicion_propietario_tarifa,
        # fin - Condiciones para el Gestor de Carga
        # inicio - Condiciones para el Propietario
        # INICIO Mermas de Fletes
        # inicio - Mermas para el Gestor de Carga
        merma_gestor_carga_valor=flete.merma_gestor_carga_valor,
        merma_gestor_carga_moneda_id=flete.merma_gestor_carga_moneda_id,
        merma_gestor_carga_es_porcentual=flete.merma_gestor_carga_es_porcentual,
        merma_gestor_carga_tolerancia=flete.merma_gestor_carga_tolerancia,
        # fin - Mermas para el Gestor de Carga
        # inicio - Mermas para el Propietario
        merma_propietario_valor=flete.merma_propietario_valor,
        merma_propietario_moneda_id=flete.merma_propietario_moneda_id,
        merma_propietario_es_porcentual=flete.merma_propietario_es_porcentual,
        merma_propietario_tolerancia=flete.merma_propietario_tolerancia,
        # fin - Mermas para el Propietario
        # FIN Mermas de Fletes
        gestor_carga_id=gestor_carga_id,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    create_orden_carga_estado_historial(db, obj.id, EstadoEnum.NUEVO, modified_by)
    return obj


def edit_orden_carga(
    obj: OrdenCarga,
    db: Session,
    data: OrdenCargaEditForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> OrdenCarga:
    if data.camion_id:
        obj.camion_id = data.camion_id
    if data.semi_id:
        obj.semi_id = data.semi_id
    if data.flete_id:
        obj.flete_id = data.flete_id
    if data.cantidad_nominada:
        obj.cantidad_nominada = data.cantidad_nominada
    if data.origen_id:
        obj.origen_id = data.origen_id
    if data.destino_id:
        obj.destino_id = data.destino_id
    if data.comentarios:
        obj.comentarios = data.comentarios
    obj.anticipos_liberados = data.anticipos_liberados
    obj.gestor_carga_id = gestor_carga_id
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def edit_orden_carga_by_movimiento(
    obj: OrdenCarga,
    db: Session,
    data: OrdenCargaEditForm,
    gestor_carga_id: int,
    modified_by: str,
) -> OrdenCarga:
    for prop, value in data.dict().items():
        if hasattr(obj, prop) and value:
            setattr(obj, prop, value)
    obj.modify_by_movimiento = True
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
    obj.anticipos_liberados = True
    create_orden_carga_estado_historial(db, obj.id, EstadoEnum.ACEPTADO, modified_by)
    return change_orden_carga_status(obj, db, EstadoEnum.ACEPTADO, modified_by)


def cancelar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    create_orden_carga_estado_historial(db, obj.id, EstadoEnum.CANCELADO, modified_by)
    return change_orden_carga_status(obj, db, EstadoEnum.CANCELADO, modified_by)


def conciliar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    create_orden_carga_estado_historial(db, obj.id, EstadoEnum.CONCILIADO, modified_by)
    return change_orden_carga_status(obj, db, EstadoEnum.CONCILIADO, modified_by)


def contabilizar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    create_orden_carga_estado_historial(
        db, obj.id, EstadoEnum.CONTABILIZADO, modified_by
    )
    return change_orden_carga_status(obj, db, EstadoEnum.CONTABILIZADO, modified_by)


def arribado_a_cargar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    obj.orden_carga_estado = OrdenCargaEstadoEnum.ARRIBADO_A_CARGAR
    create_orden_carga_estado_historial(
        db, obj.id, OrdenCargaEstadoEnum.ARRIBADO_A_CARGAR, modified_by
    )
    return change_orden_carga_status(obj, db, EstadoEnum.EN_PROCESO, modified_by)


def arribado_a_descargar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    obj.estado = EstadoEnum.EN_PROCESO
    obj.orden_carga_estado = OrdenCargaEstadoEnum.ARRIBADO_A_DESCARGAR
    create_orden_carga_estado_historial(
        db, obj.id, OrdenCargaEstadoEnum.ARRIBADO_A_DESCARGAR, modified_by
    )
    return change_orden_carga_status(obj, db, EstadoEnum.EN_PROCESO, modified_by)


def cargar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    obj.estado = EstadoEnum.EN_PROCESO
    obj.orden_carga_estado = OrdenCargaEstadoEnum.CARGADO
    create_orden_carga_estado_historial(
        db, obj.id, OrdenCargaEstadoEnum.CARGADO, modified_by
    )
    return change_orden_carga_status(obj, db, EstadoEnum.EN_PROCESO, modified_by)


def descargar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    obj.estado = EstadoEnum.EN_PROCESO
    obj.orden_carga_estado = OrdenCargaEstadoEnum.DESCARGADO
    create_orden_carga_estado_historial(
        db, obj.id, OrdenCargaEstadoEnum.DESCARGADO, modified_by
    )
    return change_orden_carga_status(obj, db, EstadoEnum.EN_PROCESO, modified_by)


def finalizar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    create_orden_carga_estado_historial(db, obj.id, EstadoEnum.FINALIZADO, modified_by)
    return change_orden_carga_status(obj, db, EstadoEnum.FINALIZADO, modified_by)


def liquidar_orden_carga(
    obj: OrdenCarga,
    db: Session,
    modified_by: str,
) -> OrdenCarga:
    create_orden_carga_estado_historial(db, obj.id, EstadoEnum.LIQUIDADO, modified_by)
    return change_orden_carga_status(obj, db, EstadoEnum.LIQUIDADO, modified_by)
