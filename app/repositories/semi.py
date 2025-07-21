from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import Semi
from app.models.combinacion import Combinacion
from app.models.permiso import Permiso
from app.models.rol import Rol
from app.models.user import User, UserRol
from app.schemas import SemiForm


def get_semi_list(db: Session) -> List[Semi]:
    return (
        db.query(Semi)
        .filter(Semi.estado != EstadoEnum.ELIMINADO.value)
        .order_by(Semi.id.desc())
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
        .order_by(Semi.id.desc())
        .all()
    )


def get_combinaciones_by_semi_id(db: Session, semi_id: int) -> List[Combinacion]:
    return db.query(Combinacion).filter(Combinacion.semi_id == semi_id).all()


def rol_tiene_permiso(rol_id: int, permiso_descripcion: str, db: Session, usuario_id: int) -> bool:
    usuario_rol = db.query(UserRol).filter_by(rol_id=rol_id, user_id=usuario_id).first()

    if not usuario_rol:
        return False

    permiso = db.query(Permiso).filter_by(descripcion=permiso_descripcion).first()

    if not permiso:
        return False

    return permiso in usuario_rol.rol.permisos


def get_rol_id_by_gestor_carga_id(db: Session, gestor_carga_id: int) -> Optional[int]:
    rol = db.query(Rol).filter_by(gestor_carga_id=gestor_carga_id).first()

    return rol.id if rol else None


def get_rol_id_by_usuario_id(db: Session, usuario_id: int) -> int:
    usuario = db.query(User).filter(User.id == usuario_id).first()
    if not usuario:
        raise ValueError(f"No se encontró usuario con id {usuario_id}")

    if not usuario.user_roles or len(usuario.user_roles) == 0:
        raise ValueError(f"El usuario con id {usuario_id} no tiene roles asignados")

    return usuario.user_roles[0].rol_id


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
    gestor_carga_id: Optional[int],
    usuario_id: int,
) -> Semi:

    rol_id = get_rol_id_by_usuario_id(db, usuario_id)

    roles_permisos = rol_tiene_permiso(rol_id, "Cambiar_estado 4 - semi", db, usuario_id)

    if roles_permisos:
        estado_inicial = EstadoEnum.ACTIVO.value
    else:
        estado_inicial = EstadoEnum.PENDIENTE.value
    obj = Semi(
        placa=data.placa,
        propietario_id=data.propietario_id,
        numero_chasis=data.numero_chasis,
        foto=foto_url,
        ciudad_habilitacion_municipal_id=data.ciudad_habilitacion_municipal_id,
        numero_habilitacion_municipal=data.numero_habilitacion_municipal,
        vencimiento_habilitacion_municipal=data.vencimiento_habilitacion_municipal,
        foto_habilitacion_municipal_frente=foto_habilitacion_municipal_frente_url,
        foto_habilitacion_municipal_reverso=foto_habilitacion_municipal_reverso_url,
        ente_emisor_transporte_id=data.ente_emisor_transporte_id,
        numero_habilitacion_transporte=data.numero_habilitacion_transporte,
        vencimiento_habilitacion_transporte=data.vencimiento_habilitacion_transporte,
        foto_habilitacion_transporte_frente=foto_habilitacion_transporte_frente_url,
        foto_habilitacion_transporte_reverso=foto_habilitacion_transporte_reverso_url,
        ente_emisor_automotor_id=data.ente_emisor_automotor_id,
        titular_habilitacion_automotor=data.titular_habilitacion_automotor,
        foto_habilitacion_automotor_frente=foto_habilitacion_automotor_frente_url,
        foto_habilitacion_automotor_reverso=foto_habilitacion_automotor_reverso_url,
        marca_id=data.marca_id,
        clasificacion_id=data.clasificacion_id,
        tipo_id=data.tipo_id,
        tipo_carga_id=data.tipo_carga_id,
        color_id=data.color_id,
        anho=data.anho,
        bruto=data.bruto,
        tara=data.tara,
        largo=data.largo,
        alto=data.alto,
        ancho=data.ancho,
        volumen=data.volumen,
        estado=estado_inicial,
        modified_by=modified_by,
        created_by=modified_by,
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
