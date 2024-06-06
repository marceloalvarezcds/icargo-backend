from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_, not_  # type: ignore

from app.enums import EstadoEnum
from app.models import Camion, Chofer
from app.schemas import ChoferEditForm, ChoferForm


def get_chofer_list(db: Session) -> List[Chofer]:
    return (
        db.query(Chofer)
        .filter(Chofer.estado != EstadoEnum.ELIMINADO.value)
        .order_by(Chofer.nombre)
        .all()
    )


def get_chofer_list_by_gestor_cuenta_id(
    db: Session, gestor_cuenta_id: Optional[int]
) -> List[Chofer]:
    return (
        db.query(Chofer)
        .filter(
            and_(
                Chofer.gestor_cuenta_id == gestor_cuenta_id,
                Chofer.estado == EstadoEnum.ACTIVO.value,
            )
        )
        .order_by(Chofer.nombre)
        .all()
    )


def get_chofer_list_without_camion(
    db: Session, gestor_cuenta_id: Optional[int]
) -> List[Chofer]:
    sub_query = (
        db.query(Camion.chofer_id)
        .distinct(Camion.chofer_id)
        .join(Camion.chofer)
        .filter(
            and_(
                Chofer.gestor_cuenta_id == gestor_cuenta_id,
                Chofer.estado == EstadoEnum.ACTIVO.value,
            )
        )
        .subquery()
    )
    return (
        db.query(Chofer)
        .filter(
            and_(
                Chofer.gestor_cuenta_id == gestor_cuenta_id,
                Chofer.estado == EstadoEnum.ACTIVO.value,
                not_(Chofer.id.in_(sub_query)),
            )
        )
        .order_by(Chofer.nombre)
        .all()
    )


def get_chofer_by(
    db: Session,
    tipo_documento_id: int,
    pais_emisor_documento_id: int,
    numero_documento: str,
) -> Optional[Chofer]:
    return (
        db.query(Chofer)
        .filter(
            and_(
                Chofer.numero_documento == numero_documento,
                Chofer.pais_emisor_documento_id == pais_emisor_documento_id,
                Chofer.tipo_documento_id == tipo_documento_id,
            )
        )
        .first()
    )


def get_chofer_by_id(db: Session, id: int) -> Optional[Chofer]:
    return db.query(Chofer).filter(Chofer.id == id).first()


def create_chofer(
    db: Session,
    data: ChoferForm,
    gestor_cuenta_id: Optional[int],
    foto_documento_frente_url: Optional[str],
    foto_documento_reverso_url: Optional[str],
    foto_perfil_url: Optional[str],
    foto_registro_frente_url: Optional[str],
    foto_registro_reverso_url: Optional[str],
    modified_by: str,
) -> Chofer:
    obj = Chofer(
        nombre=data.nombre,
        tipo_documento_id=data.tipo_documento_id,
        pais_emisor_documento_id=data.pais_emisor_documento_id,
        numero_documento=data.numero_documento,
        ruc=data.ruc,
        digito_verificador=data.digito_verificador,
        fecha_nacimiento=data.fecha_nacimiento,
        gestor_cuenta_id=gestor_cuenta_id,
        oficial_cuenta_id=data.oficial_cuenta_id,
        es_propietario=data.es_propietario,
        puede_recibir_anticipos=data.puede_recibir_anticipos,
        foto_documento_frente=foto_documento_frente_url,
        foto_documento_reverso=foto_documento_reverso_url,
        foto_perfil=foto_perfil_url,
        # inicio registro
        ciudad_emisor_registro_id=data.pais_emisor_registro_id,
        tipo_registro_id=data.tipo_registro_id,
        numero_registro=data.numero_registro,
        vencimiento_registro=data.vencimiento_registro,
        foto_registro_frente=foto_registro_frente_url,
        foto_registro_reverso=foto_registro_reverso_url,
        # fin registro
        estado=EstadoEnum.PENDIENTE.value,
        telefono=data.telefono,
        email=data.email,
        direccion=data.direccion,
        ciudad_id=data.ciudad_id,
        modified_by=modified_by,
        created_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_chofer(
    obj: Chofer,
    db: Session,
    data: ChoferEditForm,
    foto_documento_frente_url: Optional[str],
    foto_documento_reverso_url: Optional[str],
    foto_perfil_url: Optional[str],
    foto_registro_frente_url: Optional[str],
    foto_registro_reverso_url: Optional[str],
    modified_by: str,
) -> Chofer:
    if (
        data.tipo_documento_id
        and data.pais_emisor_documento_id
        and data.numero_documento
    ):
        obj.tipo_documento_id = data.tipo_documento_id
        obj.pais_emisor_documento_id = data.pais_emisor_documento_id
        obj.numero_documento = data.numero_documento
        obj.ruc = data.ruc
        obj.digito_verificador = data.digito_verificador
        obj.fecha_nacimiento = data.fecha_nacimiento
        obj.es_propietario = data.es_propietario
        obj.puede_recibir_anticipos = data.puede_recibir_anticipos
        obj.email = data.email
        obj.direccion = data.direccion
        obj.ciudad_id = data.ciudad_id
        obj.nombre = data.nombre
        if data.oficial_cuenta_id:
            obj.oficial_cuenta_id = data.oficial_cuenta_id
        if data.telefono:
            obj.telefono = data.telefono
        if foto_documento_frente_url:
            obj.foto_documento_frente = foto_documento_frente_url
        if foto_documento_reverso_url:
            obj.foto_documento_reverso = foto_documento_reverso_url
        if foto_perfil_url:
            obj.foto_perfil = foto_perfil_url
        # inicio registro
        obj.ciudad_emisor_registro_id = data.ciudad_emisor_registro_id
        obj.tipo_registro_id = data.tipo_registro_id
        obj.numero_registro = data.numero_registro
        obj.vencimiento_registro = data.vencimiento_registro
        if foto_registro_frente_url:
            obj.foto_registro_frente = foto_registro_frente_url
        if foto_registro_reverso_url:
            obj.foto_registro_reverso = foto_registro_reverso_url
        # fin registro
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.refresh(obj)
    return obj


def change_chofer_status(
    obj: Chofer,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> Chofer:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_chofer(
    obj: Chofer,
    db: Session,
    modified_by: str,
) -> Chofer:
    return change_chofer_status(obj, db, EstadoEnum.ELIMINADO, modified_by)
