from datetime import datetime

from operator import and_

from app.models.camion import Camion
from sqlalchemy.sql.expression import update

from typing import List, Optional

from app import schemas
from app.models.gestor_carga import GestorCarga
from app.schemas.combinacion import CombinacionCreateModel, CombinacionForm
from app.models.permiso import Permiso
from app.models.rol import Rol
from app.models.propietario import Propietario
from sqlalchemy.orm import Session  # type: ignore


from app.enums import EstadoEnum
from app.models import Combinacion
from app.models.chofer import Chofer

def get_combinacion_list(db: Session) -> List[Combinacion]:
    return (
        db.query(Combinacion)
        .filter(Combinacion.estado != EstadoEnum.ELIMINADO.value)
        .order_by(Combinacion.id.desc()) 
        .all()
    )


def get_combinacion_list_by_gestor_carga_id(
    db: Session, gestor_carga_id: Optional[int]
) -> List[Combinacion]:
    return (
        db.query(Combinacion)
        .filter(
            and_(
                Combinacion.gestor_carga_id == gestor_carga_id,
                Combinacion.estado != EstadoEnum.ELIMINADO.value,
            ),
            Combinacion.estado != EstadoEnum.ELIMINADO.value,
        )
        .order_by(Combinacion.id.desc()) 
        .all()
    )


def get_combinacion_list_by_camion_id(
    db: Session, camion_id: int
) -> List[Combinacion]:
    return (
        db.query(Combinacion)
        .filter(
            and_(
                Combinacion.camion_id == camion_id,
                Combinacion.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            Combinacion.camion_id, Combinacion.semi_id
        )
        .all()
    )



####################################################################################

def get_camion_list_by_combinacion_id(
    db: Session, gestor_carga_id: Optional[int]
) -> List[Combinacion]:
    return (
        db.query(Combinacion)
        .filter(
            and_(
                Combinacion.gestor_carga_id == gestor_carga_id,
                Combinacion.estado == EstadoEnum.ACTIVO.value,
            )
        )
        .order_by(
            Combinacion.camion_id, Combinacion.semi_id
        )
        
        .all()
    )


def get_camion_combinacion_id_null(
    db: Session, gestor_carga_id: Optional[int]
) -> List[Combinacion]:
    return (
        db.query(Combinacion)
        .filter(
            and_(
                # Combinacion.camion_id == null(),
                Combinacion.gestor_carga_id == gestor_carga_id,
                Combinacion.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            Combinacion.camion_id, Combinacion.semi_id
        )
        .all()
    )


def get_semi_list_by_camion_id(
    db: Session, camion_id: int, gestor_carga_id: int
) -> List[Combinacion]:
    return (
        db.query(Combinacion)
        .filter(
            and_(
                # Combinacion.camion_id == camion_id,
                
                Combinacion.gestor_carga_id == gestor_carga_id,
                Combinacion.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            Combinacion.camion_id, Combinacion.semi_id
        )
        .all()
        
    )

def get_semi_list_by_camion_id_null(
    db: Session, camion_id: int, gestor_carga_id: int
) -> List[Combinacion]:
    return (
        db.query(Combinacion)
        .filter(
            and_(
                # Combinacion.camion_id == camion_id,
            
                Combinacion.gestor_carga_id == gestor_carga_id,
                Combinacion.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            Combinacion.camion_id, Combinacion.semi_id
        )
        .all()
    )


def get_combinacion_by_camion_id_and_semi_id(
    db: Session,
    camion_id: int,
    semi_id: int,
    gestor_carga_id: Optional[int],
) -> Optional[Combinacion]:
    return (
        db.query(Combinacion)
        .filter(
            and_(
                Combinacion.camion_id == camion_id,
                Combinacion.semi_id == semi_id,
                Combinacion.gestor_carga_id == gestor_carga_id,
                Combinacion.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            Combinacion.created_at.desc(),
            Combinacion.camion_id,
            Combinacion.semi_id,
        )
        .first()
    )


def get_camion_id_and_semi_id(
    db: Session,
    camion_id: int,
    semi_id: int,
    gestor_carga_id: Optional[int],
) -> Optional[Combinacion]:
    return (
        db.query(Combinacion)
        .filter(
            and_(

                Combinacion.gestor_carga_id == gestor_carga_id,
                Combinacion.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            Combinacion.created_at.desc(),
            Combinacion.camion_id,
            Combinacion.semi_id,
        )
        .first()
    )
##################################

def get_combinacion_by_params(
    db: Session,
    propietario_id: int,
    camion_id: int,
    chofer_id: int,
    gestor_carga_id: Optional[int]
) -> Optional[Combinacion]:
    return db.query(Combinacion).filter(
        and_(
            Combinacion.propietario_id == propietario_id,
            Combinacion.camion_id == camion_id,
            Combinacion.chofer_id == chofer_id,
            Combinacion.gestor_carga_id == gestor_carga_id
        )
    ).first()


def get_combinacion_by_ids(
    db: Session,
    propietario_id: int,
    camion_id: int,
    semi_id: int,
    chofer_id: int,
    gestor_carga_id: int,
) -> Combinacion:
    return db.query(Combinacion).filter(
        Combinacion.propietario_id == propietario_id,
        Combinacion.camion_id == camion_id,
        Combinacion.semi_id == semi_id,
        Combinacion.chofer_id == chofer_id,
        Combinacion.gestor_carga_id == gestor_carga_id
    ).first()


def get_combinacion_tracto_chofer_by_ids(
    db: Session,
    chofer_id: int,
    gestor_carga_id: int,
) -> Combinacion:
    return db.query(Combinacion).filter(

        Combinacion.chofer_id == chofer_id,
        Combinacion.gestor_carga_id == gestor_carga_id
    ).first()

def get_combinacion_tracto_propietario_ids(
    db: Session,
    camion_id: int,
    propietario_id: int,
    gestor_carga_id: int,
) -> Combinacion:
    return db.query(Combinacion).filter(
        Combinacion.camion_id == camion_id,
        Combinacion.propietario_id == propietario_id,
        Combinacion.gestor_carga_id == gestor_carga_id
    ).first()


def get_combinacion_tracto_semi_chofer_propietario_ids(
    db: Session,
    camion_id: int,
    semi_id: int,
    chofer_id: int,
    gestor_carga_id: int,
) -> Combinacion:
    return db.query(Combinacion).filter(
        Combinacion.camion_id == camion_id,
        Combinacion.semi_id == semi_id,
        Combinacion.chofer_id == chofer_id,
        Combinacion.gestor_carga_id == gestor_carga_id
    ).first()


def get_combinacion_semi_ids(
    db: Session,
    semi_id: int,
    gestor_carga_id: int,
) -> Combinacion:
    return db.query(Combinacion).filter(
        Combinacion.semi_id == semi_id,
        Combinacion.gestor_carga_id == gestor_carga_id
    ).first()


def get_combinacion_tracto_ids(
    db: Session,
    camion_id: int,
    gestor_carga_id: int,
) -> Combinacion:
    return db.query(Combinacion).filter(
        Combinacion.camion_id == camion_id,
        Combinacion.gestor_carga_id == gestor_carga_id
    ).first()


def get_combinacion_by_id(db: Session, id: int) -> Optional[Combinacion]:
    return db.query(Combinacion).filter(Combinacion.id == id).first()


def get_combinacion_list_by_gestor_cuenta_id(
    db: Session, gestor_cuenta_id: Optional[int]
) -> List[Combinacion]:
    return (
        db.query(Combinacion)
        .filter(
            and_(
                Combinacion.id == gestor_cuenta_id,
                Combinacion.estado == EstadoEnum.ACTIVO.value,
            )
        )
        # .order_by(Propietario.created_at.desc(), Propietario.nombre)
        .all()
    )


def change_combinacion_status(
    obj: Combinacion,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> Combinacion:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def get_combinacion_by(
    db: Session,
    propietario_id: int,
    camion_id: int,
    semi_id: int,
    chofer_id: int,
) -> Optional[schemas.Combinacion]:
    return db.query(Combinacion).filter(
        Combinacion.propietario_id == propietario_id,
        Combinacion.camion_id == camion_id,
        Combinacion.semi_id == semi_id,
        Combinacion.chofer_id == chofer_id,
    ).first()


def edit_combinacion(
    obj: CombinacionForm,
    db: Session,
    modified_by: str,
) ->Combinacion:

    if obj.propietario_id:
        obj.propietario_id = obj.propietario_id
    if obj.camion_id:
        obj.camion_id = obj.camion_id
    if obj.semi_id:
        obj.semi_id = obj.semi_id
    if obj.chofer_id:
        obj.chofer_id = obj.chofer_id
    if obj.comentario:
        obj.comentario = obj.comentario
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()

    return obj


def gestor_carga_tiene_permiso(gestor_carga_id: int, permiso_descripcion: str, db: Session) -> bool:
    gestor_carga = db.query(GestorCarga).filter_by(id=gestor_carga_id).first()
    
    if not gestor_carga:
        return False
    
    for rol in gestor_carga.roles:
        permiso = db.query(Permiso).filter_by(descripcion=permiso_descripcion).first()
        if permiso and permiso in rol.permisos:
            return True

    return False



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


def create_combinacion(
    db: Session,
    data: CombinacionCreateModel,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Combinacion:
    rol_id = get_rol_id_by_gestor_carga_id(db, gestor_carga_id)

    roles_permisos = rol_tiene_permiso(rol_id, "Cambiar_estado 6 - combinaciones", db)

    if roles_permisos:
        estado_inicial = EstadoEnum.ACTIVO.value
    else:
        estado_inicial = EstadoEnum.NUEVO.value
  
    combinacion = Combinacion(
        estado=estado_inicial,
        propietario_id=data.propietario_id,
        camion_id=data.camion_id,
        semi_id=data.semi_id,
        chofer_id=data.chofer_id,
        comentario=data.comentario,
        neto=data.neto,
        gestor_carga_id=gestor_carga_id,
        modified_by=modified_by,
        created_by=modified_by,
    )

    db.add(combinacion)
    db.commit()
    db.refresh(combinacion)
    db.execute(
        update(Camion)
        .where(Camion.id == data.camion_id)
        .values(limite_cantidad_oc_activas= data.oc_activa, 
                limite_monto_anticipos=data.limite_anticipos)
    )
    db.commit()
    
    db.execute(
        update(Propietario)
        .where(Propietario.id == data.propietario_id)
        .values(puede_recibir_anticipos= data.anticipo_propietario)
    )
    db.commit()

    db.execute(
        update(Chofer)
        .where(Chofer.id == data.chofer_id)
        .values(puede_recibir_anticipos= data.puede_recibir_anticipos)
    )
    db.commit()
    
    return combinacion