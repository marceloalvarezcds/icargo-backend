from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore
from sqlalchemy.sql.expression import false, true  # type: ignore

from app.enums import EstadoEnum
from app.models import Flete
from app.schemas import FleteForm


def get_flete_list(db: Session) -> List[Flete]:
    return (
        db.query(Flete)
        .filter(
            and_(
                Flete.estado != EstadoEnum.ELIMINADO.value,
                Flete.es_subasta
                == false(),  # Filtro temporal hasta implementar subastas
            )
        )
        .order_by(
            Flete.created_at,
            Flete.remitente_id,
            Flete.producto_id,
            Flete.tipo_carga_id,
            Flete.numero_lote,
        )
        .all()
    )


def get_flete_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: Optional[int]
) -> List[Flete]:
    return (
        db.query(Flete)
        .filter(
            and_(
                Flete.gestor_carga_id == gestor_carga_id,
                Flete.estado != EstadoEnum.ELIMINADO.value,
                Flete.publicado == true(),
                Flete.es_subasta == false(),
            )
        )
        .order_by(Flete.created_at)
        .all()
    )


def get_flete_by_id(db: Session, id: int) -> Optional[Flete]:
    return db.query(Flete).filter(Flete.id == id).first()


def create_flete(
    db: Session,
    data: FleteForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Flete:
    obj = Flete(
        remitente_id=data.remitente_id,
        producto_id=data.producto_id,
        tipo_carga_id=data.tipo_carga_id,
        numero_lote=data.numero_lote,
        gestor_carga_id=gestor_carga_id,
        publicado=data.publicado,
        es_subasta=data.es_subasta,
        # INICIO Tramo de Fletes
        origen_id=data.origen_id,
        origen_indicacion=data.origen_indicacion,
        destino_id=data.destino_id,
        destino_indicacion=data.destino_indicacion,
        distancia=data.distancia,
        # FIN Tramo de Fletes
        # INICIO Cantidad y Flete
        condicion_cantidad=data.condicion_cantidad,
        # inicio - Condiciones para el Gestor de Carga
        condicion_gestor_cuenta_moneda_id=data.condicion_gestor_carga_moneda_id,
        condicion_gestor_cuenta_tarifa=data.condicion_gestor_carga_tarifa,
        condicion_gestor_cuenta_unidad_id=data.condicion_gestor_carga_unidad_id,
        # fin - Condiciones para el Gestor de Carga
        # inicio - Condiciones para el Propietario
        condicion_propietario_moneda_id=data.condicion_propietario_moneda_id,
        condicion_propietario_tarifa=data.condicion_propietario_tarifa,
        condicion_propietario_unidad_id=data.condicion_propietario_unidad_id,
        # fin - Condiciones para el Propietario
        # FIN Cantidad y Flete
        # INICIO Mermas de Fletes
        # inicio - Mermas para el Gestor de Carga
        merma_gestor_cuenta_valor=data.merma_gestor_carga_valor,
        merma_gestor_cuenta_moneda_id=data.merma_gestor_carga_moneda_id,
        merma_gestor_cuenta_unidad_id=data.merma_gestor_carga_unidad_id,
        merma_gestor_cuenta_es_porcentual=data.merma_gestor_carga_es_porcentual,
        merma_gestor_cuenta_tolerancia=data.merma_gestor_carga_tolerancia,
        # fin - Mermas para el Gestor de Carga
        # inicio - Mermas para el Propietario
        merma_propietario_valor=data.merma_propietario_valor,
        merma_propietario_moneda_id=data.merma_propietario_moneda_id,
        merma_propietario_unidad_id=data.merma_propietario_unidad_id,
        merma_propietario_es_porcentual=data.merma_propietario_es_porcentual,
        merma_propietario_tolerancia=data.merma_propietario_tolerancia,
        # fin - Mermas para el Propietario
        # FIN Mermas de Fletes
        # INICIO Emisión de Órdenes
        emision_orden_texto_legal=data.emision_orden_texto_legal,
        emision_orden_detalle=data.emision_orden_detalle,
        emision_orden_centro_operativo_destinatarios=[],
        emision_orden_remitente_destinatarios=[],
        emision_orden_user_destinatarios=[],
        # FIN Emisión de Órdenes
        vigencia_anticipos=data.vigencia_anticipos,
        estado=EstadoEnum.ACTIVO.value,
        modified_by=modified_by,
        created_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_flete(
    obj: Flete,
    db: Session,
    data: FleteForm,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Flete:
    if data.remitente_id and data.producto_id and data.tipo_carga_id:
        obj.remitente_id = data.remitente_id
        obj.producto_id = data.producto_id
        obj.tipo_carga_id = data.tipo_carga_id
        obj.numero_lote = data.numero_lote
        obj.gestor_carga_id = gestor_carga_id
        obj.publicado = data.publicado
        obj.es_subasta = data.es_subasta
        # INICIO Tramo de Fletes
        obj.origen_id = data.origen_id
        obj.origen_indicacion = data.origen_indicacion
        obj.destino_id = data.destino_id
        obj.destino_indicacion = data.destino_indicacion
        obj.distancia = data.distancia
        # FIN Tramo de Fletes
        # INICIO Cantidad y Flete
        obj.condicion_cantidad = data.condicion_cantidad
        # inicio - Condiciones para el Gestor de Carga
        obj.condicion_gestor_cuenta_moneda_id = data.condicion_gestor_carga_moneda_id
        obj.condicion_gestor_cuenta_tarifa = data.condicion_gestor_carga_tarifa
        obj.condicion_gestor_cuenta_unidad_id = data.condicion_gestor_carga_unidad_id
        # fin - Condiciones para el Gestor de Carga
        # inicio - Condiciones para el Propietario
        obj.condicion_propietario_moneda_id = data.condicion_propietario_moneda_id
        obj.condicion_propietario_tarifa = data.condicion_propietario_tarifa
        obj.condicion_propietario_unidad_id = data.condicion_propietario_unidad_id
        # fin - Condiciones para el Propietario
        # FIN Cantidad y Flete
        # INICIO Mermas de Fletes
        # inicio - Mermas para el Gestor de Carga
        obj.merma_gestor_cuenta_valor = data.merma_gestor_carga_valor
        obj.merma_gestor_cuenta_moneda_id = data.merma_gestor_carga_moneda_id
        obj.merma_gestor_cuenta_unidad_id = data.merma_gestor_carga_unidad_id
        obj.merma_gestor_cuenta_es_porcentual = data.merma_gestor_carga_es_porcentual
        obj.merma_gestor_cuenta_tolerancia = data.merma_gestor_carga_tolerancia
        # fin - Mermas para el Gestor de Carga
        # inicio - Mermas para el Propietario
        obj.merma_propietario_valor = data.merma_propietario_valor
        obj.merma_propietario_moneda_id = data.merma_propietario_moneda_id
        obj.merma_propietario_unidad_id = data.merma_propietario_unidad_id
        obj.merma_propietario_es_porcentual = data.merma_propietario_es_porcentual
        obj.merma_propietario_tolerancia = data.merma_propietario_tolerancia
        # fin - Mermas para el Propietario
        # FIN Mermas de Fletes
        # INICIO Emisión de Órdenes
        obj.emision_orden_texto_legal = data.emision_orden_texto_legal
        obj.emision_orden_detalle = data.emision_orden_detalle
        # FIN Emisión de Órdenes
        obj.vigencia_anticipos = data.vigencia_anticipos
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.refresh(obj)
    return obj


def change_flete_status(
    obj: Flete,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> Flete:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_flete(
    obj: Flete,
    db: Session,
    modified_by: str,
) -> Flete:
    return change_flete_status(obj, db, EstadoEnum.ELIMINADO, modified_by)


def change_flete_public_status(
    obj: Flete,
    db: Session,
    is_public: bool,
    modified_by: str,
) -> Flete:
    obj.publicado = is_public
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def update_flete_destinatarios(
    obj: Flete,
    db: Session,
    modified_by: str,
) -> Flete:
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj
