from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import func  # type: ignore
from sqlalchemy.orm import Query, Session  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore

from app.enums import EstadoEnum
from app.models import Movimiento, OrdenCarga, OrdenCargaAnticipoRetirado, Camion
from app.models.flete_anticipo import FleteAnticipo
from app.models.orden_carga_anticipo_saldo import OrdenCargaAnticipoSaldo
from app.schemas import OrdenCargaAnticipoRetiradoForm
from sqlalchemy import desc
from sqlalchemy.orm import joinedload


def get_orden_carga_anticipo_retirado_list(db: Session) -> List[OrdenCargaAnticipoRetirado]:
    return (
        db.query(OrdenCargaAnticipoRetirado)
        .filter(OrdenCargaAnticipoRetirado.estado_movimiento != EstadoEnum.ELIMINADO.value)
        .order_by(desc(OrdenCargaAnticipoRetirado.id))
        .all()
    )


def get_orden_carga_anticipo_retirado_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: Optional[int]
) -> List[OrdenCargaAnticipoRetirado]:
    return (
        db.query(OrdenCargaAnticipoRetirado)
        .join(OrdenCarga)  # Esto es necesario
        .filter(
            and_(
                OrdenCarga.gestor_carga_id == gestor_carga_id,
            )
        )
        .options(joinedload(OrdenCargaAnticipoRetirado.orden_carga))
        .order_by(desc(OrdenCargaAnticipoRetirado.id))
        .all()
    )


def get_orden_carga_anticipo_retirado_by(
    db: Session,
    flete_anticipo_id: int,
    orden_carga_id: int,
    punto_venta_id: int,
    tipo_comprobante_id: Optional[int] = None,
    numero_comprobante: Optional[str] = None,
) -> Optional[OrdenCargaAnticipoRetirado]:
    return (
        db.query(OrdenCargaAnticipoRetirado)
        .filter(
            OrdenCargaAnticipoRetirado.flete_anticipo_id == flete_anticipo_id,
            OrdenCargaAnticipoRetirado.orden_carga_id == orden_carga_id,
            OrdenCargaAnticipoRetirado.punto_venta_id == punto_venta_id,
            OrdenCargaAnticipoRetirado.tipo_comprobante_id == tipo_comprobante_id,
            OrdenCargaAnticipoRetirado.numero_comprobante == numero_comprobante,
        )
        .first()
    )


def get_orden_carga_anticipo_retirado_by_id(
    db: Session,
    id: int,
) -> Optional[OrdenCargaAnticipoRetirado]:
    return (
        db.query(OrdenCargaAnticipoRetirado)
        .filter(OrdenCargaAnticipoRetirado.id == id)
        .first()
    )


def create_orden_carga_anticipo_retirado(
    db: Session,
    data: OrdenCargaAnticipoRetiradoForm,
    modified_by: str,
) -> OrdenCargaAnticipoRetirado:
    obj = OrdenCargaAnticipoRetirado(
        flete_anticipo_id=data.flete_anticipo_id,
        orden_carga_id=data.orden_carga_id,
        orden_carga_anticipo_porcentaje_id=data.orden_carga_anticipo_porcentaje_id,
        punto_venta_id=data.punto_venta_id,
        tipo_comprobante_id=data.tipo_comprobante_id,
        numero_comprobante=data.numero_comprobante,
        moneda_id=data.moneda_id,
        monto_retirado=data.monto_retirado,
        monto_mon_local=data.monto_mon_local,
        observacion=data.observacion,
        insumo_punto_venta_precio_id=data.insumo_punto_venta_precio_id,
        unidad_id=data.unidad_id,
        cantidad_retirada=data.cantidad_retirada,
        precio_unitario=data.precio_unitario,
        created_by=modified_by,
        modified_by=modified_by,
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_orden_carga_anticipo_retirado(
    obj: OrdenCargaAnticipoRetirado,
    db: Session,
    data: OrdenCargaAnticipoRetiradoForm,
    modified_by: str,
) -> OrdenCargaAnticipoRetirado:
    obj.flete_anticipo_id = data.flete_anticipo_id
    obj.orden_carga_id = data.orden_carga_id
    obj.orden_carga_anticipo_porcentaje_id = data.orden_carga_anticipo_porcentaje_id
    obj.punto_venta_id = data.punto_venta_id
    obj.tipo_comprobante_id = data.tipo_comprobante_id
    obj.numero_comprobante = data.numero_comprobante
    obj.moneda_id = data.moneda_id
    obj.monto_retirado = data.monto_retirado
    obj.observacion = data.observacion
    obj.insumo_punto_venta_precio_id = data.insumo_punto_venta_precio_id
    obj.unidad_id = data.unidad_id
    obj.cantidad_retirada = data.cantidad_retirada
    obj.precio_unitario = data.precio_unitario
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_orden_carga_anticipo_retirado(db: Session, id: int, modified_by: str):
    obj = db.query(OrdenCargaAnticipoRetirado).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()


def change_anticipo_status(
    obj: OrdenCargaAnticipoRetirado,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> OrdenCargaAnticipoRetirado:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()

    db.commit()
    db.refresh(obj)

    return obj


def get_camion_by_orden_carga_id(db: Session, orden_carga_id: int):
    return (
        db.query(Camion)
        .join(OrdenCarga, Camion.id == OrdenCarga.camion_id)
        .filter(OrdenCarga.id == orden_carga_id)
        .first()
    )

def get_anticipo_by_id(db: Session, id: int) -> OrdenCargaAnticipoRetirado:
    return db.query(OrdenCargaAnticipoRetirado).filter(OrdenCargaAnticipoRetirado.id == id).first()


def get_movimiento_by_anticipo_id(db: Session, anticipo_id: int):
    return db.query(Movimiento).filter(Movimiento.anticipo_id == anticipo_id).all()


def get_movimiento_by_anticipo_id_and_id(db: Session, anticipo_id: int, id: int):
    """
    Obtiene el movimiento correspondiente al id de OrdenCargaAnticipoRetirado y su anticipo_id.
    """
    return db.query(Movimiento).filter(
        Movimiento.anticipo_id == anticipo_id,
        Movimiento.id == id  # Asegurándonos de que estamos buscando el movimiento específico
    ).first()


def get_saldo_by_flete_anticipo_id_and_orden_carga_id(
    db: Session, flete_anticipo_id: int, orden_carga_id: int
) -> OrdenCargaAnticipoSaldo:
    return db.query(OrdenCargaAnticipoSaldo).filter(
        OrdenCargaAnticipoSaldo.flete_anticipo_id == flete_anticipo_id,
        OrdenCargaAnticipoSaldo.orden_carga_id == orden_carga_id
    ).first()



def get_total_anticipo_retirado_by_camion_id(
    db: Session, camion_id: int
) -> Optional[Decimal]:
    subquery: Query = (
        db.query(
            OrdenCargaAnticipoRetirado.id.label("id"),
            OrdenCargaAnticipoRetirado.monto_mon_local.label("monto_mon_local"),
        )
        .distinct()
        # .select_from(Movimiento)
        .join(Movimiento.anticipo)
        .join(OrdenCargaAnticipoRetirado.orden_carga)
        .filter(
            and_(
                OrdenCarga.camion_id == camion_id,
                Movimiento.propietario_id.is_not(None),
                or_(
                    Movimiento.estado == EstadoEnum.PENDIENTE.value,
                    Movimiento.estado == EstadoEnum.EN_PROCESO.value,
                ),
            )
        )
        .subquery()
    )
    return db.query(
        func.sum(subquery.c.monto_mon_local).label("monto_mon_local")
    ).first()[0]


def get_flete_anticipo_anterior_con_retiro(
    db: Session,
    orden_carga_id: int,
    exclude_flete_anticipo_id: Optional[int] = None,
) -> Optional[FleteAnticipo]:
    """
    Busca un flete anticipo anterior que haya tenido retiros en esta orden de carga.
    Opcionalmente excluye un ID.
    """
    subquery = (
        db.query(OrdenCargaAnticipoRetirado.flete_anticipo_id)
        .filter(OrdenCargaAnticipoRetirado.orden_carga_id == orden_carga_id)
        .group_by(OrdenCargaAnticipoRetirado.flete_anticipo_id)
        .having(func.sum(OrdenCargaAnticipoRetirado.monto_retirado) > 0)
        .subquery()
    )

    query = db.query(FleteAnticipo).filter(FleteAnticipo.id.in_(subquery))
    if exclude_flete_anticipo_id:
        query = query.filter(FleteAnticipo.id != exclude_flete_anticipo_id)

    return query.first()
