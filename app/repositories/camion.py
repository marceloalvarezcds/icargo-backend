from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import Camion
from app.schemas import CamionForm


def get_camion_list(db: Session) -> List[Camion]:
    return db.query(Camion).filter(Camion.estado != EstadoEnum.ELIMINADO.value).all()


def get_camion_by(db: Session, placa: str) -> Optional[Camion]:
    return db.query(Camion).filter(Camion.placa == placa).first()


def get_camion_by_id(db: Session, id: int) -> Optional[Camion]:
    return db.query(Camion).filter(Camion.id == id).first()


def get_camion_list_by_propietario_id(db: Session, propietario_id: int) -> List[Camion]:
    return db.query(Camion).filter(Camion.propietario_id == propietario_id).all()


def create_camion(
    db: Session,
    data: CamionForm,
    foto_url: str,
    foto_habilitacion_municipal_frente_url: str,
    foto_habilitacion_municipal_reverso_url: str,
    foto_habilitacion_transporte_frente_url: str,
    foto_habilitacion_transporte_reverso_url: str,
    foto_habilitacion_automotor_frente_url: str,
    foto_habilitacion_automotor_reverso_url: str,
    modified_by: str,
) -> Camion:
    obj = Camion(
        placa=data.placa,
        propietario_id=data.propietario_id,
        chofer_id=data.chofer_id,
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
        tipo_id=data.tipo_id,
        color_id=data.color_id,
        anho=data.anho,
        # FIN Detalles del Camión
        # INICIO Capacidad del Camión
        bruto=data.bruto,
        tara=data.tara,
        estado=EstadoEnum.PENDIENTE.value,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_camion(
    obj: Camion,
    db: Session,
    data: CamionForm,
    foto_url: Optional[str],
    foto_habilitacion_municipal_frente_url: Optional[str],
    foto_habilitacion_municipal_reverso_url: Optional[str],
    foto_habilitacion_transporte_frente_url: Optional[str],
    foto_habilitacion_transporte_reverso_url: Optional[str],
    foto_habilitacion_automotor_frente_url: Optional[str],
    foto_habilitacion_automotor_reverso_url: Optional[str],
    modified_by: str,
) -> Camion:
    if data.placa:
        obj.placa = data.placa
        obj.propietario_id = data.propietario_id
        obj.chofer_id = data.chofer_id
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
        obj.tipo_id = data.tipo_id
        obj.color_id = data.color_id
        obj.anho = data.anho
        # FIN Detalles del Camión
        # INICIO Capacidad del Camión
        obj.bruto = data.bruto
        obj.tara = data.tara
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.refresh(obj)
    return obj


def delete_camion(
    obj: Camion,
    db: Session,
    modified_by: str,
) -> Camion:
    obj.estado = EstadoEnum.ELIMINADO.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj
