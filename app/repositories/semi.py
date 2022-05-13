from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import Semi
from app.schemas import SemiForm


def get_semi_list(db: Session) -> List[Semi]:
    return (
        db.query(Semi)
        .filter(Semi.estado != EstadoEnum.ELIMINADO.value)
        .order_by(Semi.placa)
        .all()
    )


def get_semi_by(db: Session, placa: str) -> Optional[Semi]:
    return db.query(Semi).filter(Semi.placa == placa).first()


def get_semi_by_id(db: Session, id: int) -> Optional[Semi]:
    return db.query(Semi).filter(Semi.id == id).first()


def get_semi_list_by_propietario_id(db: Session, propietario_id: int) -> List[Semi]:
    return (
        db.query(Semi)
        .filter(Semi.propietario_id == propietario_id)
        .order_by(Semi.placa)
        .all()
    )


def create_semi(
    db: Session,
    data: SemiForm,
    foto_url: Optional[str],
    foto_habilitacion_municipal_frente_url: Optional[str],
    foto_habilitacion_municipal_reverso_url: Optional[str],
    foto_habilitacion_transporte_frente_url: Optional[str],
    foto_habilitacion_transporte_reverso_url: Optional[str],
    foto_habilitacion_automotor_frente_url: Optional[str],
    foto_habilitacion_automotor_reverso_url: Optional[str],
    modified_by: str,
) -> Semi:
    obj = Semi(
        placa=data.placa,
        propietario_id=data.propietario_id,
        numero_chasis=data.numero_chasis,
        foto=foto_url,
        # INICIO Habilitaciones del Camión
        # inicio - municipal
        ciudad_habilitacion_municipal_id=data.ciudad_habilitacion_municipal_id,
        numero_habilitacion_municipal=data.numero_habilitacion_municipal,
        vencimiento_habilitacion_municipal=data.vencimiento_habilitacion_municipal,
        foto_habilitacion_municipal_frente=foto_habilitacion_municipal_frente_url,
        foto_habilitacion_municipal_reverso=foto_habilitacion_municipal_reverso_url,
        # fin - municipal
        # inicio - transporte
        ente_emisor_transporte_id=data.ente_emisor_transporte_id,
        numero_habilitacion_transporte=data.numero_habilitacion_transporte,
        vencimiento_habilitacion_transporte=data.vencimiento_habilitacion_transporte,
        foto_habilitacion_transporte_frente=foto_habilitacion_transporte_frente_url,
        foto_habilitacion_transporte_reverso=foto_habilitacion_transporte_reverso_url,
        # fin - transporte
        # inicio - automotor
        ente_emisor_automotor_id=data.ente_emisor_automotor_id,
        titular_habilitacion_automotor=data.titular_habilitacion_automotor,
        foto_habilitacion_automotor_frente=foto_habilitacion_automotor_frente_url,
        foto_habilitacion_automotor_reverso=foto_habilitacion_automotor_reverso_url,
        # fin - automotor
        # FIN Habilitaciones del Camión
        # INICIO Detalles del Camión
        marca_id=data.marca_id,
        clasificacion_id=data.clasificacion_id,
        tipo_id=data.tipo_id,
        tipo_carga_id=data.tipo_carga_id,
        color_id=data.color_id,
        anho=data.anho,
        # FIN Detalles del Camión
        # INICIO Capacidad del Camión
        bruto=data.bruto,
        tara=data.tara,
        largo=data.largo,
        alto=data.alto,
        ancho=data.ancho,
        volumen=data.volumen,
        estado=EstadoEnum.PENDIENTE.value,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_semi(
    obj: Semi,
    db: Session,
    data: SemiForm,
    foto_url: Optional[str],
    foto_habilitacion_municipal_frente_url: Optional[str],
    foto_habilitacion_municipal_reverso_url: Optional[str],
    foto_habilitacion_transporte_frente_url: Optional[str],
    foto_habilitacion_transporte_reverso_url: Optional[str],
    foto_habilitacion_automotor_frente_url: Optional[str],
    foto_habilitacion_automotor_reverso_url: Optional[str],
    modified_by: str,
) -> Semi:
    if data.placa:
        obj.placa = data.placa
        obj.propietario_id = data.propietario_id
        obj.numero_chasis = data.numero_chasis
        if foto_url:
            obj.foto = foto_url
        # INICIO Habilitaciones del Camión
        # inicio - municipal
        obj.ciudad_habilitacion_municipal_id = data.ciudad_habilitacion_municipal_id
        obj.numero_habilitacion_municipal = data.numero_habilitacion_municipal
        obj.vencimiento_habilitacion_municipal = data.vencimiento_habilitacion_municipal
        if foto_habilitacion_municipal_frente_url:
            obj.foto_habilitacion_municipal_frente = (
                foto_habilitacion_municipal_frente_url
            )
        if foto_habilitacion_municipal_reverso_url:
            obj.foto_habilitacion_municipal_reverso = (
                foto_habilitacion_municipal_reverso_url
            )
        # fin - municipal
        # inicio - transporte
        obj.ente_emisor_transporte_id = data.ente_emisor_transporte_id
        obj.numero_habilitacion_transporte = data.numero_habilitacion_transporte
        obj.vencimiento_habilitacion_transporte = (
            data.vencimiento_habilitacion_transporte
        )
        if foto_habilitacion_transporte_frente_url:
            obj.foto_habilitacion_transporte_frente = (
                foto_habilitacion_transporte_frente_url
            )
        if foto_habilitacion_transporte_reverso_url:
            obj.foto_habilitacion_transporte_reverso = (
                foto_habilitacion_transporte_reverso_url
            )
        # fin - transporte
        # inicio - automotor
        obj.ente_emisor_automotor_id = data.ente_emisor_automotor_id
        obj.titular_habilitacion_automotor = data.titular_habilitacion_automotor
        if foto_habilitacion_automotor_frente_url:
            obj.foto_habilitacion_automotor_frente = (
                foto_habilitacion_automotor_frente_url
            )
        if foto_habilitacion_automotor_reverso_url:
            obj.foto_habilitacion_automotor_reverso = (
                foto_habilitacion_automotor_reverso_url
            )
        # fin - automotor
        # FIN Habilitaciones del Camión
        # INICIO Detalles del Camión
        obj.marca_id = data.marca_id
        obj.clasificacion_id = data.clasificacion_id
        obj.tipo_id = data.tipo_id
        obj.tipo_carga_id = data.tipo_carga_id
        obj.color_id = data.color_id
        obj.anho = data.anho
        # FIN Detalles del Camión
        # INICIO Capacidad del Camión
        obj.bruto = data.bruto
        obj.tara = data.tara
        obj.largo = data.largo
        obj.alto = data.alto
        obj.ancho = data.ancho
        obj.volumen = data.volumen
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.refresh(obj)
    return obj


def change_semi_status(
    obj: Semi,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> Semi:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_semi(
    obj: Semi,
    db: Session,
    modified_by: str,
) -> Semi:
    return change_semi_status(obj, db, EstadoEnum.ELIMINADO, modified_by)
