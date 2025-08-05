from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore

from app.enums import EstadoEnum
from app.models import Propietario
from app.models.combinacion import Combinacion
from app.models.permiso import Permiso
from app.models.rol import Rol
from app.models.user import User
from app.schemas import Chofer, PropietarioEditForm, PropietarioForm


def get_propietario_list(db: Session) -> List[Propietario]:
    return (
        db.query(Propietario)
        .filter(Propietario.estado != EstadoEnum.ELIMINADO.value)
        .order_by(Propietario.created_at.desc(), Propietario.nombre)
        .all()
    )


def get_propietario_list_by_gestor_cuenta_id(
    db: Session, gestor_cuenta_id: Optional[int]
) -> List[Propietario]:
    return (
        db.query(Propietario)
        .filter(
            and_(
                Propietario.gestor_cuenta_id == gestor_cuenta_id,
                Propietario.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(Propietario.created_at.desc(), Propietario.id)
        .all()
    )

# def get_propietario_list_by_tipo_persona_id(
#     db: Session, tipo_persona_id: int
# ) -> List[Propietario]:
#     return (
#         db.query(Propietario)
#         .filter(
#             and_(
#                 Propietario.tipo_persona_id == tipo_persona_id,
#             )
#         )
#         .order_by(Propietario.created_at.desc(), Propietario.nombre)
#         .all()
#     )


def get_combinaciones_by_propietario_id(db: Session, propietario_id: int) -> List[Combinacion]:
    return db.query(Combinacion).filter(Combinacion.propietario_id == propietario_id).all()


def get_propietario_by(
    db: Session,
    composicion_juridica_id: int,
    ruc: str,
) -> Optional[Propietario]:
    return (
        db.query(Propietario)
        .filter(
            and_(
                Propietario.ruc == ruc,
                Propietario.composicion_juridica_id == composicion_juridica_id,
            )
        )
        .first()
    )


def get_propietario_by_id(db: Session, id: int) -> Optional[Propietario]:
    return db.query(Propietario).filter(Propietario.id == id).first()


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


def get_rol_id_by_usuario_id(db: Session, usuario_id: int) -> int:
    usuario = db.query(User).filter(User.id == usuario_id).first()
    if not usuario:
        raise ValueError(f"No se encontró usuario con id {usuario_id}")

    if not usuario.user_roles or len(usuario.user_roles) == 0:
        raise ValueError(f"El usuario con id {usuario_id} no tiene roles asignados")

    return usuario.user_roles[0].rol_id


def create_propietario(
    db: Session,
    data: PropietarioForm,
    gestor_cuenta_id: Optional[int],
    foto_documento_frente_url: Optional[str],
    foto_documento_reverso_url: Optional[str],
    foto_perfil_url: Optional[str],
    chofer: Optional[Chofer],
    modified_by: str,
    usuario_id: int,
) -> Propietario:

    rol_id = get_rol_id_by_usuario_id(db, usuario_id)

    roles_permisos = rol_tiene_permiso(rol_id, "Cambiar_estado 1 - propietario", db)

    # Determinar el estado inicial según el permiso
    if roles_permisos:
        estado_inicial = EstadoEnum.ACTIVO.value
    else:
        estado_inicial = EstadoEnum.NUEVO.value
    obj = Propietario(
        nombre=data.nombre,
        nombre_corto=data.nombre_corto,
        composicion_juridica_id=data.composicion_juridica_id,
        tipo_documento_propietario_id=data.tipo_documento_propietario_id,
        ruc=data.ruc,
        digito_verificador=data.digito_verificador,
        pais_origen_id=data.pais_origen_id,
        fecha_nacimiento=data.fecha_nacimiento,
        gestor_cuenta_id=gestor_cuenta_id,
        oficial_cuenta_id=data.oficial_cuenta_id,
        es_chofer=data.es_chofer,
        is_propietario_condicionado=data.is_propietario_condicionado,
        puede_recibir_anticipos=data.puede_recibir_anticipos,
        foto_documento_frente=foto_documento_frente_url,
        foto_documento_reverso=foto_documento_reverso_url,
        foto_perfil=foto_perfil_url,
        estado=estado_inicial,
        telefono=data.telefono,
        email=data.email,
        direccion=data.direccion,
        ciudad_id=data.ciudad_id,
        chofer_id=chofer.id if chofer else None,
        modified_by=modified_by,
        created_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_propietario(
    obj: Propietario,
    db: Session,
    data: PropietarioEditForm,
    foto_documento_frente_url: Optional[str],
    foto_documento_reverso_url: Optional[str],
    foto_perfil_url: Optional[str],
    chofer: Optional[Chofer],
    modified_by: str,
) -> Propietario:
    if data.composicion_juridica_id and data.ruc:
        obj.ruc = data.ruc
        obj.composicion_juridica_id = data.composicion_juridica_id
        #obj.tipo_documento_id = data.tipo_documento_id
        obj.digito_verificador = data.digito_verificador
        obj.fecha_nacimiento = data.fecha_nacimiento
        obj.es_chofer = data.es_chofer
        obj.is_propietario_condicionado=data.is_propietario_condicionado
        obj.puede_recibir_anticipos = data.puede_recibir_anticipos
        obj.email = data.email
        obj.direccion = data.direccion
        obj.ciudad_id = data.ciudad_id
        if data.nombre:
            obj.nombre = data.nombre
        if data.nombre_corto:
            obj.nombre = data.nombre_corto
        if data.pais_origen_id:
            obj.pais_origen_id = data.pais_origen_id
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
        obj.chofer_id = chofer.id if chofer else None
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.refresh(obj)
    return obj


def change_propietario_status(
    obj: Propietario,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> Propietario:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_propietario(
    obj: Propietario,
    db: Session,
    modified_by: str,
) -> Propietario:
    return change_propietario_status(obj, db, EstadoEnum.ELIMINADO, modified_by)
