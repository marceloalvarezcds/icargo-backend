from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.elements import and_  # type: ignore
from sqlalchemy.sql.expression import null  # type: ignore

from app.models import CamionSemiNeto


def get_camion_semi_neto_list_by_producto_id(
    db: Session, producto_id: int, gestor_carga_id: int
) -> List[CamionSemiNeto]:
    return (
        db.query(CamionSemiNeto)
        .filter(
            and_(
                CamionSemiNeto.producto_id == producto_id,
                CamionSemiNeto.gestor_carga_id == gestor_carga_id,
            )
        )
        .order_by(
            CamionSemiNeto.camion_id, CamionSemiNeto.semi_id, CamionSemiNeto.producto_id
        )
        .all()
    )


def get_camion_semi_neto_list_by_producto_id_null(
    db: Session, gestor_carga_id: int
) -> List[CamionSemiNeto]:
    return (
        db.query(CamionSemiNeto)
        .filter(
            and_(
                CamionSemiNeto.producto_id == null(),
                CamionSemiNeto.gestor_carga_id == gestor_carga_id,
            )
        )
        .order_by(
            CamionSemiNeto.camion_id, CamionSemiNeto.semi_id, CamionSemiNeto.producto_id
        )
        .all()
    )


def get_camion_semi_neto_list_by_camion_id(
    db: Session, camion_id: int, gestor_carga_id: int
) -> List[CamionSemiNeto]:
    return (
        db.query(CamionSemiNeto)
        .filter(
            and_(
                CamionSemiNeto.camion_id == camion_id,
                CamionSemiNeto.producto_id == null(),
                CamionSemiNeto.gestor_carga_id == gestor_carga_id,
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
            )
        )
        .order_by(
            CamionSemiNeto.camion_id, CamionSemiNeto.semi_id, CamionSemiNeto.producto_id
        )
        .all()
    )


def get_camion_semi_neto_by_camion_id_and_semi_id(
    db: Session, camion_id: int, semi_id: int, gestor_carga_id: int
) -> Optional[CamionSemiNeto]:
    return (
        db.query(CamionSemiNeto)
        .filter(
            and_(
                CamionSemiNeto.camion_id == camion_id,
                CamionSemiNeto.semi_id == semi_id,
                CamionSemiNeto.producto_id == null(),
                CamionSemiNeto.gestor_carga_id == gestor_carga_id,
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
    db: Session, camion_id: int, semi_id: int, producto_id: int, gestor_carga_id: int
) -> Optional[CamionSemiNeto]:
    return (
        db.query(CamionSemiNeto)
        .filter(
            and_(
                CamionSemiNeto.camion_id == camion_id,
                CamionSemiNeto.semi_id == semi_id,
                CamionSemiNeto.producto_id == producto_id,
                CamionSemiNeto.gestor_carga_id == gestor_carga_id,
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
