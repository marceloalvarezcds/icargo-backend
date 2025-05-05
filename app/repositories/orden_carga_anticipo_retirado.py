from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import func  # type: ignore
from sqlalchemy.orm import Query, Session  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore

from app.enums import EstadoEnum
from app.models import Movimiento, OrdenCarga, OrdenCargaAnticipoRetirado, Camion
from app.models.orden_carga_anticipo_saldo import OrdenCargaAnticipoSaldo
from app.schemas import OrdenCargaAnticipoRetiradoForm


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
    #     # Imprimir los valores que se van a guardar en la base de datos
    # print("Guardando los siguientes datos en la base de datos:")
    # print(f"flete_anticipo_id: {data.flete_anticipo_id}")
    # print(f"orden_carga_id: {data.orden_carga_id}")
    # print(f"orden_carga_anticipo_porcentaje_id: {data.orden_carga_anticipo_porcentaje_id}")
    # print(f"punto_venta_id: {data.punto_venta_id}")
    # print(f"tipo_comprobante_id: {data.tipo_comprobante_id}")
    # print(f"numero_comprobante: {data.numero_comprobante}")
    # print(f"moneda_id: {data.moneda_id}")
    # print(f"monto_retirado: {data.monto_retirado}")
    # print(f"monto_retirado_ml: {data.monto_mon_local}")
    # print(f"observacion: {data.observacion}")
    # print(f"insumo_punto_venta_precio_id: {data.insumo_punto_venta_precio_id}")
    # print(f"unidad_id: {data.unidad_id}")
    # print(f"cantidad_retirada: {data.cantidad_retirada}")
    # print(f"precio_unitario: {data.precio_unitario}")
    # print(f"created_by: {modified_by}")
    # print(f"modified_by: {modified_by}")

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

    movimiento = get_movimiento_by_anticipo_id(db, obj.id)
    if movimiento:

        movimiento.estado = status.value
        movimiento.modified_by = modified_by
        movimiento.modified_at = datetime.now()

        db.commit()
        db.refresh(movimiento)  

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
    return db.query(Movimiento).filter(Movimiento.anticipo_id == anticipo_id).first()


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
