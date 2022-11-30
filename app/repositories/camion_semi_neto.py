from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore
from sqlalchemy.sql.expression import null  # type: ignore

from app.enums import EstadoEnum
from app.models import CamionSemiNeto
from app.schemas import CamionSemiNetoForm


def get_camion_semi_neto_by_id(db: Session, id: int) -> Optional[CamionSemiNeto]:
    return db.query(CamionSemiNeto).get(id)


def get_camion_semi_neto_by_camion_id_and_semi_id(
    db: Session,
    camion_id: int,
    semi_id: int,
    gestor_carga_id: Optional[int],
) -> Optional[CamionSemiNeto]:
    return (
        db.query(CamionSemiNeto)
        .filter(
            and_(
                CamionSemiNeto.camion_id == camion_id,
                CamionSemiNeto.semi_id == semi_id,
                CamionSemiNeto.producto_id == null(),
                CamionSemiNeto.gestor_carga_id == gestor_carga_id,
                CamionSemiNeto.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            CamionSemiNeto.created_at.desc(),
            CamionSemiNeto.camion_id,
            CamionSemiNeto.semi_id,
        )
        .first()
    )


def get_camion_semi_neto_by_camion_id_and_semi_id_and_producto_id(
    db: Session,
    camion_id: int,
    semi_id: int,
    producto_id: int,
    gestor_carga_id: Optional[int],
) -> Optional[CamionSemiNeto]:
    return (
        db.query(CamionSemiNeto)
        .filter(
            and_(
                CamionSemiNeto.camion_id == camion_id,
                CamionSemiNeto.semi_id == semi_id,
                CamionSemiNeto.producto_id == producto_id,
                CamionSemiNeto.gestor_carga_id == gestor_carga_id,
                CamionSemiNeto.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            CamionSemiNeto.created_at.desc(),
            CamionSemiNeto.camion_id,
            CamionSemiNeto.semi_id,
            CamionSemiNeto.producto_id,
        )
        .first()
    )


def get_camion_semi_neto_by_camion_id_and_semi_id_and_neto(
    db: Session,
    camion_id: int,
    semi_id: int,
    neto: Decimal,
    gestor_carga_id: Optional[int],
) -> Optional[CamionSemiNeto]:
    return (
        db.query(CamionSemiNeto)
        .filter(
            and_(
                CamionSemiNeto.camion_id == camion_id,
                CamionSemiNeto.semi_id == semi_id,
                CamionSemiNeto.producto_id == null(),
                CamionSemiNeto.neto == neto,
                CamionSemiNeto.gestor_carga_id == gestor_carga_id,
                CamionSemiNeto.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            CamionSemiNeto.created_at.desc(),
            CamionSemiNeto.camion_id,
            CamionSemiNeto.semi_id,
        )
        .first()
    )


def get_camion_semi_neto_by_camion_id_and_semi_id_and_producto_id_and_neto(
    db: Session,
    camion_id: int,
    semi_id: int,
    producto_id: int,
    neto: Decimal,
    gestor_carga_id: Optional[int],
) -> Optional[CamionSemiNeto]:
    return (
        db.query(CamionSemiNeto)
        .filter(
            and_(
                CamionSemiNeto.camion_id == camion_id,
                CamionSemiNeto.semi_id == semi_id,
                CamionSemiNeto.producto_id == producto_id,
                CamionSemiNeto.neto == neto,
                CamionSemiNeto.gestor_carga_id == gestor_carga_id,
                CamionSemiNeto.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            CamionSemiNeto.created_at.desc(),
            CamionSemiNeto.camion_id,
            CamionSemiNeto.semi_id,
            CamionSemiNeto.producto_id,
        )
        .first()
    )


def get_camion_semi_neto_list_by_producto_id(
    db: Session, producto_id: int, gestor_carga_id: Optional[int]
) -> List[CamionSemiNeto]:
    return (
        db.query(CamionSemiNeto)
        .filter(
            and_(
                CamionSemiNeto.producto_id == producto_id,
                CamionSemiNeto.gestor_carga_id == gestor_carga_id,
                CamionSemiNeto.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            CamionSemiNeto.camion_id, CamionSemiNeto.semi_id, CamionSemiNeto.producto_id
        )
        .all()
    )


def get_camion_semi_neto_list_by_producto_id_null(
    db: Session, gestor_carga_id: Optional[int]
) -> List[CamionSemiNeto]:
    return (
        db.query(CamionSemiNeto)
        .filter(
            and_(
                CamionSemiNeto.producto_id == null(),
                CamionSemiNeto.gestor_carga_id == gestor_carga_id,
                CamionSemiNeto.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            CamionSemiNeto.camion_id, CamionSemiNeto.semi_id, CamionSemiNeto.producto_id
        )
        .all()
    )


def get_camion_semi_neto_list_by_camion_id(
    db: Session, camion_id: int
) -> List[CamionSemiNeto]:
    return (
        db.query(CamionSemiNeto)
        .filter(
            and_(
                CamionSemiNeto.camion_id == camion_id,
                CamionSemiNeto.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            CamionSemiNeto.camion_id, CamionSemiNeto.semi_id, CamionSemiNeto.producto_id
        )
        .all()
    )


def get_camion_semi_neto_list_by_camion_id_and_producto_id_null(
    db: Session, camion_id: int, gestor_carga_id: int
) -> List[CamionSemiNeto]:
    return (
        db.query(CamionSemiNeto)
        .filter(
            and_(
                CamionSemiNeto.camion_id == camion_id,
                CamionSemiNeto.producto_id == null(),
                CamionSemiNeto.gestor_carga_id == gestor_carga_id,
                CamionSemiNeto.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            CamionSemiNeto.camion_id, CamionSemiNeto.semi_id, CamionSemiNeto.producto_id
        )
        .all()
    )


def get_camion_semi_neto_list_by_camion_id_and_producto_id(
    db: Session, camion_id: int, producto_id: int, gestor_carga_id: int
) -> List[CamionSemiNeto]:
    return (
        db.query(CamionSemiNeto)
        .filter(
            and_(
                CamionSemiNeto.camion_id == camion_id,
                CamionSemiNeto.producto_id == producto_id,
                CamionSemiNeto.gestor_carga_id == gestor_carga_id,
                CamionSemiNeto.estado != EstadoEnum.ELIMINADO.value,
            )
        )
        .order_by(
            CamionSemiNeto.camion_id, CamionSemiNeto.semi_id, CamionSemiNeto.producto_id
        )
        .all()
    )


def create_camion_semi_neto(
    db: Session,
    data: CamionSemiNetoForm,
    gestor_carga_id: int,
    modified_by: str,
) -> CamionSemiNeto:
    obj = CamionSemiNeto(
        camion_id=data.camion_id,
        semi_id=data.semi_id,
        producto_id=data.producto_id,
        neto=data.neto,
        gestor_carga_id=gestor_carga_id,
        estado=EstadoEnum.ACTIVO.value,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_camion_semi_neto(
    obj: CamionSemiNeto,
    db: Session,
    data: CamionSemiNetoForm,
    modified_by: str,
) -> CamionSemiNeto:
    obj.camion_id = data.camion_id
    obj.semi_id = data.semi_id
    obj.producto_id = data.producto_id
    obj.neto = data.neto
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def change_camion_semi_neto_status(
    obj: CamionSemiNeto,
    db: Session,
    status: EstadoEnum,
    modified_by: str,
) -> CamionSemiNeto:
    obj.estado = status.value
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_camion_semi_neto(
    obj: CamionSemiNeto,
    db: Session,
    modified_by: str,
) -> CamionSemiNeto:
    return change_camion_semi_neto_status(obj, db, EstadoEnum.ELIMINADO, modified_by)
