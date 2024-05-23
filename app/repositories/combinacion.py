from datetime import datetime
from operator import and_
from typing import List, Optional

from app import schemas
from app.schemas.combinacion import CombinacionCreateModel, CombinacionForm
from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import Combinacion
from app.schemas import Chofer, Propietario

def get_combinacion_list(db: Session) -> List[Combinacion]:
    return (
        db.query(Combinacion)
        .filter(Combinacion.estado != EstadoEnum.ELIMINADO.value)
        .order_by(Combinacion.created_at.desc())
        .all()
    )



def get_combinacion_by_ids(
    db: Session,
    propietario_id: int,
    camion_id: int,
    chofer_id: int,
    semi_id: int,
) -> Combinacion:
    return db.query(Combinacion).filter(
        Combinacion.propietario_id == propietario_id,
        Combinacion.camion_id == camion_id,
        Combinacion.chofer_id == chofer_id,
        Combinacion.semi_id == semi_id
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
        .order_by(Propietario.created_at.desc(), Propietario.nombre)
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
    chofer: Optional[Chofer],
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
    if chofer:
        obj.chofer_id = chofer.id
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()

    return obj


def create_combinacion(
    db: Session,
    data: CombinacionCreateModel,
    gestor_carga_id: Optional[int],
    modified_by: str,
) -> Combinacion:
    obj = Combinacion(
        estado=EstadoEnum.PENDIENTE.value,
        propietario_id=data.propietario_id,
        camion_id=data.camion_id,
        semi_id=data.semi_id,
        chofer_id=data.chofer_id,
        comentario=data.comentario,
        neto= data.neto,
        gestor_carga_id=data.gestor_carga_id,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
