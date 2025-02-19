from datetime import datetime
from typing import List, Optional

from app.models.combinacion import Combinacion
from app.models.permiso import Permiso
from app.models.rol import Rol
from sqlalchemy.orm import Query, Session  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore
from sqlalchemy.sql.expression import true  # type: ignore
from sqlalchemy import desc

from app.enums import EstadoEnum, OrdenCargaEstadoEnum
from app.models import Camion, Flete, OrdenCarga
from app.schemas import OrdenCargaEditForm, OrdenCargaForm
from app.schemas.orden_carga import OrdenCargaUpdateFecha

from .orden_carga_estado_historial import create_orden_carga_estado_historial
from .orden_carga_comentarios_historial import create_orden_carga_comentarios_historial
from sqlalchemy import func


def get_orden_carga_list(db: Session) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter(OrdenCarga.estado != EstadoEnum.ELIMINADO.value)
        .order_by(desc(OrdenCarga.id))
        .all()
    )

def get_orden_carga_en_proceso_list(db: Session) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter(
            and_(
                OrdenCarga.estado != EstadoEnum.ELIMINADO.value,
                OrdenCarga.estado.in_([EstadoEnum.NUEVO.value, EstadoEnum.ACEPTADO.value]),
            )
        )
        .order_by(desc(OrdenCarga.id))
        .all()
    )


def get_orden_carga_cerradas_list(db: Session) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter(
            and_(
                OrdenCarga.estado != EstadoEnum.ELIMINADO.value,
                OrdenCarga.estado.in_([EstadoEnum.NUEVO.value, EstadoEnum.ACEPTADO.value]),
            )
        )
        .order_by(desc(OrdenCarga.id))
        .all()
    )


def get_orden_carga_aceptadas_list(db: Session) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter(
            OrdenCarga.estado == EstadoEnum.ACEPTADO.value
        )
        .order_by(desc(OrdenCarga.id))
        .all()
    )


def get_orden_carga_finalizadas_list(db: Session) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter(
            OrdenCarga.estado == EstadoEnum.FINALIZADO.value
        )
        .order_by(desc(OrdenCarga.id))
        .all()
    )


def get_orden_carga_by_combinacion_id(
    db: Session, combinacion_id: int
) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter_by(combinacion_id=combinacion_id)
        .all()
    )


# def get_orden_carga_aceptada_count_by_camion_id(
#     db: Session, camion_id: int
# ) -> List[OrdenCarga]:
#     return (
#         db.query(OrdenCarga)
#         .filter(
#             and_(
#                 OrdenCarga.camion_id == camion_id,
#                 or_(
#                     OrdenCarga.estado == EstadoEnum.ACEPTADO.value,
#                     # OrdenCarga.estado == EstadoEnum.EN_PROCESO.value,
#                     # OrdenCarga.estado == EstadoEnum.FINALIZADO.value,
#                 ),
#             )
#         )
#         .count()
#     )

def get_orden_carga_aceptada_count_by_camion_id(db, camion_id):
    return db.query(OrdenCarga).filter(
        OrdenCarga.camion_id == camion_id,
        OrdenCarga.estado == EstadoEnum.ACEPTADO.value,  # Convertimos el enum a su valor
        OrdenCarga.estado != EstadoEnum.FINALIZADO.value  # Convertimos el enum a su valor
    ).count()

def get_orden_carga_finalizada_count_by_camion_id(db: Session, camion_id: int) -> int:
    return (
        db.query(func.count(OrdenCarga.id))
        .filter(
            OrdenCarga.camion_id == camion_id,
            OrdenCarga.estado == EstadoEnum.FINALIZADO.value   # Asegúrate de que este sea el estado correcto
        )
        .scalar()
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
        .order_by(desc(OrdenCarga.id))
        .all()
    )


def get_orden_carga_en_proceso_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: Optional[int]
) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter(
            and_(
                OrdenCarga.gestor_carga_id == gestor_carga_id,
                OrdenCarga.estado != EstadoEnum.ELIMINADO.value,
                OrdenCarga.estado.in_([EstadoEnum.NUEVO.value, EstadoEnum.ACEPTADO.value]),
            )
        )
        .order_by(desc(OrdenCarga.id))
        .all()
    )


def get_orden_carga_cerradas_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: Optional[int]
) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter(
            and_(
                OrdenCarga.gestor_carga_id == gestor_carga_id,
                OrdenCarga.estado != EstadoEnum.ELIMINADO.value,
                OrdenCarga.estado.in_([EstadoEnum.CANCELADO.value, EstadoEnum.FINALIZADO.value]),
            )
        )
        .order_by(desc(OrdenCarga.id))
        .all()
    )


def get_orden_carga_aceptadas_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: Optional[int]
) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter(
            and_(
                OrdenCarga.gestor_carga_id == gestor_carga_id,
                OrdenCarga.estado != EstadoEnum.ELIMINADO.value,
                OrdenCarga.estado == EstadoEnum.ACEPTADO.value,  # Filtro agregado
            )
        )
        .order_by(desc(OrdenCarga.id))
        .all()
    )

def get_orden_carga_finalizadas_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: Optional[int]
) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter(
            and_(
                OrdenCarga.gestor_carga_id == gestor_carga_id,
                OrdenCarga.estado != EstadoEnum.ELIMINADO.value,
                OrdenCarga.estado == EstadoEnum.FINALIZADO.value,  # Filtro agregado
            )
        )
        .order_by(desc(OrdenCarga.id))
        .all()
    )


def get_orden_de_carga_by_combinacion_id(
    db: Session, combinacion_id: int, gestor_carga_id: Optional[int]
) -> List[OrdenCarga]:
    return (
        db.query(OrdenCarga)
        .filter(
            and_(
                OrdenCarga.combinacion_id == combinacion_id,
                OrdenCarga.gestor_carga_id == gestor_carga_id,
            )
        )
        .order_by(
            OrdenCarga.id
        )
        .all()
    )


def get_orden_carga_by_id(db: Session, id: int) -> Optional[OrdenCarga]:
    return db.query(OrdenCarga).filter(OrdenCarga.id == id).first()


def get_combinacion_by_orden_carga(db: Session, id: int) -> Optional[OrdenCarga]:
    return db.query(OrdenCarga).filter(OrdenCarga.combinacion_id == id).first()


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


def rol_tiene_permiso(rol_id: int, permiso_descripcion: str, db: Session) -> bool:
    rol = db.query(Rol).filter_by(id=rol_id).first()
    if not rol:
        return False

    permiso = db.query(Permiso).filter_by(descripcion=permiso_descripcion).first()

    if permiso and permiso in rol.permisos:
        return True
    return False


def get_rol_id_by_gestor_carga_id(db: Session, gestor_carga_id: int) -> Optional[int]:
    rol = db.query(Rol).filter_by(gestor_carga_id=gestor_carga_id).first()
    return rol.id if rol else None


def create_orden_carga(
    db: Session,
    data: OrdenCargaForm,
    flete: Flete,
    gestor_carga_id: Optional[int],
    modified_by: str,
    estado_inicial: EstadoEnum,
) -> OrdenCarga:

    obj = OrdenCarga(
        camion_id=data.camion_id,
        camion_semi_neto_id=data.camion_semi_neto_id,
        semi_id=data.semi_id,
        chofer_id = data.chofer_id,
        propietario_id=data.propietario_id,
        flete_id=data.flete_id,
        combinacion_id=data.combinacion_id,
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
    if estado_inicial == EstadoEnum.ACEPTADO:
        obj.anticipos_liberados = True
    db.add(obj)
    db.commit()
    db.refresh(obj)
    create_orden_carga_estado_historial(db, obj.id, estado_inicial, modified_by)

    # Solo crear el historial de comentarios si hay un comentario
    comentario = data.comentarios
    if comentario:  # Si el comentario no es vacío ni None
        create_orden_carga_comentarios_historial(
            db=db,
            orden_carga_id=obj.id,
            comentario=comentario,
            created_by=modified_by,
            modified_by=modified_by,
        )

    return change_orden_carga_status(obj, db, estado_inicial, modified_by)


def edit_remitir_fecha(
    db: Session,
    obj: OrdenCarga,
    data: OrdenCargaUpdateFecha,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> OrdenCarga:

    obj.created_at = data.created_at
    obj.gestor_carga_id = gestor_carga_id
    obj.modified_by = modified_by
    db.commit()
    db.refresh(obj)
    return obj



def edit_model_orden_carga(
    db: Session,
    obj: OrdenCarga,
    modified_by: str,
) -> OrdenCarga:
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
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
    if data.condicion_gestor_carga_tarifa:
        obj.condicion_gestor_carga_tarifa = data.condicion_gestor_carga_tarifa
    if data.condicion_propietario_tarifa:
        obj.condicion_propietario_tarifa = data.condicion_propietario_tarifa
    if data.merma_gestor_carga_tolerancia:
        obj.merma_gestor_carga_tolerancia = data.merma_gestor_carga_tolerancia
    if data.merma_propietario_tolerancia:
        obj.merma_propietario_tolerancia = data.merma_propietario_tolerancia
    if data.merma_gestor_carga_valor:
        obj.merma_gestor_carga_valor = data.merma_gestor_carga_valor
    if data.merma_propietario_valor:
        obj.merma_propietario_valor = data.merma_propietario_valor
    obj.documento_fisico = data.documento_fisico
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
    # Crear historial de estados
    create_orden_carga_estado_historial(db, obj.id, EstadoEnum.CANCELADO, modified_by)
    # Verificar si la orden tiene un flete asociado
    flete = obj.flete

    # Revertir el saldo del flete
    flete.saldo += obj.cantidad_nominada
    db.add(flete)

    # Cambiar el estado de la orden
    updated_obj = change_orden_carga_status(obj, db, EstadoEnum.CANCELADO, modified_by)

    # Confirmar los cambios
    db.commit()
    db.refresh(updated_obj)

    return updated_obj



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
