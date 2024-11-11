from datetime import datetime,  time
from typing import List, Optional

from sqlalchemy.orm import Query, Session  # type: ignore
from sqlalchemy.sql import func  # type: ignore
from sqlalchemy.sql.elements import and_, or_  # type: ignore
from sqlalchemy.sql.expression import null  # type: ignore
from sqlalchemy.exc import IntegrityError

from app.enums import EstadoEnum
from app.models import (
    FleteAnticipo,
    Insumo,
    InsumoPuntoVenta,
    InsumoPuntoVentaPrecio,
    PuntoVenta,
)
from app.schemas import InsumoPuntoVentaPrecioForm, InsumoPuntoVentaPrecioUpdate



def get_insumo_venta_precio_list(db: Session) -> List[InsumoPuntoVentaPrecio]:
    return (
        db.query(InsumoPuntoVentaPrecio)
        .filter(InsumoPuntoVentaPrecio.estado != EstadoEnum.ELIMINADO.value)
        .order_by(InsumoPuntoVentaPrecio.id)
        .all()
    )


def get_last_insumo_punto_venta_precio_by_insumo_punto_venta_id(
    db: Session,
    insumo_punto_venta_id: int,
) -> Optional[InsumoPuntoVentaPrecio]:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        db.query(InsumoPuntoVentaPrecio)
        .filter(
            and_(
                InsumoPuntoVentaPrecio.estado != EstadoEnum.ELIMINADO.value,
                InsumoPuntoVentaPrecio.insumo_punto_venta_id == insumo_punto_venta_id,
                InsumoPuntoVentaPrecio.fecha_inicio <= now,
                or_(
                    InsumoPuntoVentaPrecio.fecha_fin == null(),
                    InsumoPuntoVentaPrecio.fecha_fin >= now,
                ),
            ),
        )
        .order_by(
            InsumoPuntoVentaPrecio.fecha_inicio.desc(),
            InsumoPuntoVentaPrecio.fecha_fin.desc(),
        )
        .first()
    )


def get_insumo_punto_venta_precio_max_fecha_query(
    db: Session, flete_id: int, gestor_carga_id: Optional[int]
) -> Query:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (
        db.query(
            InsumoPuntoVenta.punto_venta_id,
            InsumoPuntoVenta.insumo_id,
            func.max(InsumoPuntoVentaPrecio.fecha_inicio).label("max_fecha_inicio"),
        )
        .select_from(InsumoPuntoVentaPrecio)
        .join(InsumoPuntoVentaPrecio.insumo_punto_venta)
        .join(InsumoPuntoVenta.insumo)
        .join(InsumoPuntoVenta.punto_venta)
        .join(FleteAnticipo, Insumo.tipo_id == FleteAnticipo.tipo_insumo_id)
        .filter(
            and_(
                FleteAnticipo.flete_id == flete_id,
                InsumoPuntoVenta.gestor_carga_id == gestor_carga_id,
                InsumoPuntoVenta.estado != EstadoEnum.ELIMINADO.value,
                InsumoPuntoVentaPrecio.estado != EstadoEnum.ELIMINADO.value,
                PuntoVenta.estado != EstadoEnum.ELIMINADO.value,
                or_(
                    InsumoPuntoVentaPrecio.fecha_fin >= now,
                    InsumoPuntoVentaPrecio.fecha_fin == null(),
                ),
            )
        )
        .group_by(InsumoPuntoVenta.punto_venta_id, InsumoPuntoVenta.insumo_id)
    ).subquery()


def get_insumo_punto_venta_precio_list_by_id(
    db: Session, punto_venta_id: int, gestor_carga_id: Optional[int]
) -> List[InsumoPuntoVentaPrecio]:
    return (
        db.query(InsumoPuntoVentaPrecio)
        .join(InsumoPuntoVentaPrecio.insumo_punto_venta)
        .filter(InsumoPuntoVentaPrecio.punto_venta_id == punto_venta_id)  # Filtra por el ID de punto de venta
        .order_by(
            InsumoPuntoVentaPrecio.fecha_inicio,
            InsumoPuntoVentaPrecio.fecha_fin,
            InsumoPuntoVentaPrecio.modified_by,
        )
        .all()
    )


def get_insumo_punto_venta_precio_list_by_gestor_carga_id(
    db: Session, flete_id: int, gestor_carga_id: Optional[int]
) -> List[InsumoPuntoVentaPrecio]:
    # Subconsulta para obtener el máximo de fecha de inicio
    sub_query = (
        db.query(
            InsumoPuntoVenta.punto_venta_id,
            InsumoPuntoVenta.insumo_id,
            func.max(InsumoPuntoVentaPrecio.fecha_inicio).label("max_fecha_inicio"),
        )
        .join(InsumoPuntoVentaPrecio.insumo_punto_venta)
        .join(InsumoPuntoVenta.insumo)
        .join(InsumoPuntoVenta.punto_venta)
        .join(FleteAnticipo, Insumo.tipo_id == FleteAnticipo.tipo_insumo_id)
        .filter(
            and_(
                FleteAnticipo.flete_id == flete_id,
                InsumoPuntoVenta.gestor_carga_id == gestor_carga_id,
                InsumoPuntoVenta.estado != EstadoEnum.ELIMINADO.value,
                InsumoPuntoVentaPrecio.estado != EstadoEnum.ELIMINADO.value,
                PuntoVenta.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .group_by(InsumoPuntoVenta.punto_venta_id, InsumoPuntoVenta.insumo_id)
    ).subquery()

    return (
        db.query(InsumoPuntoVentaPrecio)
        .join(InsumoPuntoVentaPrecio.insumo_punto_venta)
        .join(
            sub_query,
            and_(
                sub_query.c.punto_venta_id == InsumoPuntoVenta.punto_venta_id,
                sub_query.c.insumo_id == InsumoPuntoVenta.insumo_id,
                sub_query.c.max_fecha_inicio == InsumoPuntoVentaPrecio.fecha_inicio,
            ),
        )
        .filter(InsumoPuntoVentaPrecio.estado == EstadoEnum.ACTIVO.value)  # Filtro para precios activos
        .order_by(
            InsumoPuntoVentaPrecio.fecha_inicio,
            InsumoPuntoVentaPrecio.fecha_fin,
            InsumoPuntoVentaPrecio.modified_by,
        )
        .all()
    )




def get_insumo_punto_venta_precio_list_by_id_and_gestor_carga_id(
    db: Session, id: int, gestor_carga_id: Optional[int]
) -> List[InsumoPuntoVentaPrecio]:
    query = (
        db.query(InsumoPuntoVentaPrecio)
        .join(InsumoPuntoVentaPrecio.insumo_punto_venta)
        .filter(InsumoPuntoVentaPrecio.id == id)  # Filtro por ID específico
        .filter(InsumoPuntoVenta.gestor_carga_id == gestor_carga_id)
        .order_by(
            InsumoPuntoVentaPrecio.fecha_inicio,
            InsumoPuntoVentaPrecio.fecha_fin,
            InsumoPuntoVentaPrecio.modified_by,
        )
    )

    return query.all()



def get_insumo_punto_venta_precio_by_id(db: Session, id: int) -> Optional[InsumoPuntoVentaPrecio]:
    return db.query(InsumoPuntoVentaPrecio).get(id)


def create_insumo_punto_venta_precio_by_insumo_punto_venta(
    db: Session,
    data: InsumoPuntoVentaPrecioForm,
    modified_by: str,
) -> InsumoPuntoVentaPrecio:
    try:
        # Inhabilitar precios activos previos
        db.query(InsumoPuntoVentaPrecio).filter(
            InsumoPuntoVentaPrecio.insumo_punto_venta_id == data.insumo_punto_venta_id,
            InsumoPuntoVentaPrecio.estado == EstadoEnum.ACTIVO.value
        ).update({"estado": EstadoEnum.INACTIVO.value}, synchronize_session=False)

        # Verificar si hora_inicio es de tipo time (sin fecha)
        if isinstance(data.hora_inicio, time):
            # Convertir hora_inicio a un objeto datetime usando una fecha ficticia
            hora_inicio_obj = datetime.combine(datetime.today(), data.hora_inicio)
            # Reemplazar solo la hora de fecha_inicio
            fecha_inicio_obj = data.fecha_inicio.replace(
                hour=hora_inicio_obj.hour,
                minute=hora_inicio_obj.minute,
                second=hora_inicio_obj.second
            )
        else:
            # Si no se pasa hora_inicio, mantener la fecha de inicio sin cambios
            fecha_inicio_obj = data.fecha_inicio

        # Crear el nuevo precio con la fecha modificada
        new_price = InsumoPuntoVentaPrecio(
            insumo_punto_venta_id=data.insumo_punto_venta_id,
            precio=data.precio,
            fecha_inicio=fecha_inicio_obj,  # Usar la fecha con la hora modificada
            fecha_fin=data.fecha_fin,
            observacion=data.observacion,
            estado=EstadoEnum.ACTIVO.value,  # El nuevo precio es activo
            created_by=modified_by,
            modified_by=modified_by,
        )
        db.add(new_price)
        db.commit()
        db.refresh(new_price)
        return new_price

    except IntegrityError as e:
        # Verificar si el error es por duplicado de clave
        if "Key (insumo_punto_venta_id, precio)" in str(e.orig):
            raise ValueError(f"Ya existe un precio activo para el insumo {data.insumo_id} en el punto de venta {data.punto_venta_id} con el precio {data.precio}. No se puede insertar un precio duplicado.")
        else:
            # Re-lanzar el error si no es por clave duplicada
            raise e



def edit_insumo_punto_venta_precio(
    obj: InsumoPuntoVentaPrecio,
    db: Session,
    data: InsumoPuntoVentaPrecioUpdate,
    modified_by: str,
) -> InsumoPuntoVentaPrecio:
   
    precio_changed = data.precio != obj.precio
    fecha_inicio_changed = data.fecha_inicio and data.fecha_inicio != obj.fecha_inicio
    fecha_fin_changed = data.fecha_fin and data.fecha_fin != obj.fecha_fin
    hora_inicio_changed = data.hora_inicio and data.hora_inicio != obj.hora_inicio
    observacion_changed = data.observacion and data.observacion != obj.observacion

    if precio_changed or fecha_inicio_changed or fecha_fin_changed or hora_inicio_changed:
        if precio_changed:
            obj.precio = data.precio

        if fecha_inicio_changed:
            obj.fecha_inicio = data.fecha_inicio

        if fecha_fin_changed:
            obj.fecha_fin = data.fecha_fin

        if hora_inicio_changed:
    
            if isinstance(data.hora_inicio, str):
                obj.hora_inicio = data.hora_inicio  
            else:
                obj.hora_inicio = data.hora_inicio.strftime("%H:%M") 
        if observacion_changed:
            obj.observacion = data.observacion

        obj.modified_by = modified_by
        obj.modified_at = datetime.now()

        db.commit()
        db.refresh(obj)  

    return obj




def get_insumo_punto_venta_precio_by_ids(
    db: Session, insumo_punto_venta_id: int, moneda_id: int
) -> InsumoPuntoVentaPrecio:
    return (
        db.query(InsumoPuntoVentaPrecio)
        .filter_by(insumo_punto_venta_id=insumo_punto_venta_id, moneda_id=moneda_id)
        .first()
    )


def create_new_insumo_punto_venta_precio(
    db: Session,
    current_price_obj: InsumoPuntoVentaPrecio,
    data: InsumoPuntoVentaPrecioUpdate,
    modified_by: str,
) -> InsumoPuntoVentaPrecio:
    # Cerrar el registro actual estableciendo `fecha_fin`
    current_price_obj.fecha_fin = datetime.now()
    db.commit()
    
    # Crear un nuevo registro con el precio actualizado
    new_price_record = InsumoPuntoVentaPrecio(
        insumo_punto_venta_id=current_price_obj.insumo_punto_venta_id,
        precio=data.precio,
        fecha_inicio=datetime.now(),
        estado=current_price_obj.estado,
        modified_by=modified_by
    )
    db.add(new_price_record)
    db.commit()
    db.refresh(new_price_record)
    
    return new_price_record


def update_insumo_punto_venta_precio(
    obj: InsumoPuntoVentaPrecio,
    db: Session,
    data: InsumoPuntoVentaPrecioUpdate,
    modified_by: str,
) -> InsumoPuntoVentaPrecio:
    # Actualizar otros campos sin cambiar el precio
    if obj.fecha_inicio.date() != data.fecha_inicio.date():
        obj.fecha_inicio = datetime.combine(data.fecha_inicio, obj.fecha_inicio.time())
    
    if data.fecha_fin is not None and (obj.fecha_fin is None or obj.fecha_fin.date() != data.fecha_fin.date()):
        obj.fecha_fin = datetime.combine(data.fecha_fin, obj.fecha_fin.time())
    
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    
    return obj
