from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql import and_  # type: ignore

from app.models import Contacto
from app.schemas import ContactoForm


def get_contacto_by_email(db: Session, email: str) -> Optional[Contacto]:
    return db.query(Contacto).filter(Contacto.email == email).first()


def get_contacto_by_id(db: Session, id: int) -> Optional[Contacto]:
    return db.query(Contacto).filter(Contacto.id == id).first()


def get_contacto_by_telefono(db: Session, telefono: str) -> Optional[Contacto]:
    return db.query(Contacto).filter(Contacto.telefono == telefono).first()


def get_contacto_by_telefono_and_email(
    db: Session, telefono: str, email: str
) -> Optional[Contacto]:
    return (
        db.query(Contacto)
        .filter(and_(Contacto.telefono == telefono, Contacto.email == email))
        .first()
    )


def create_contacto(
    db: Session,
    data: ContactoForm,
    modified_by: str,
) -> Contacto:
    obj = Contacto(
        nombre=data.nombre,
        apellido=data.apellido,
        telefono=data.telefono,
        email=data.email,
        created_by=modified_by,
        modified_by=modified_by,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def edit_contacto(
    obj: Contacto,
    db: Session,
    data: ContactoForm,
    modified_by: str,
) -> Contacto:
    obj.nombre = data.nombre
    obj.apellido = data.apellido
    obj.telefono = data.telefono
    obj.email = data.email
    obj.modified_by = modified_by
    obj.modified_at = datetime.now()
    db.commit()
    db.refresh(obj)
    return obj
