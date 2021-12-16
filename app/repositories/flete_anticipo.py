from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import FleteAnticipo
from app.schemas import FleteAnticipoForm


def get_flete_anticipo_by(
    db: Session,
    tipo_id: int,
    flete_id: int,
) -> Optional[FleteAnticipo]:
    return (
        db.query(FleteAnticipo)
        .filter(
            FleteAnticipo.tipo_id == tipo_id,
            FleteAnticipo.flete_id == flete_id,
        )
        .first()
    )


def get_flete_anticipo_by_id(
    db: Session,
    id: int,
) -> Optional[FleteAnticipo]:
    return db.query(FleteAnticipo).filter(FleteAnticipo.id == id).first()


def create_flete_anticipo(
    db: Session,
    flete_id: int,
    data: FleteAnticipoForm,
    modified_by: str,
) -> FleteAnticipo:
    obj = FleteAnticipo(
        flete_id=flete_id,
        tipo_id=data.tipo_id,
        porcentaje=data.porcentaje,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_flete_anticipo(
    obj: FleteAnticipo,
    db: Session,
    data: FleteAnticipoForm,
    modified_by: str,
) -> FleteAnticipo:
    obj.tipo_id = data.tipo_id
    obj.porcentaje = data.porcentaje
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj


def delete_flete_anticipo(db: Session, id: int, modified_by: str):
    obj = db.query(FleteAnticipo).get(id)
    if obj:
        obj.modified_by = modified_by
        obj.modified_at = datetime.now()
        db.commit()
        db.delete(obj)
        db.commit()
