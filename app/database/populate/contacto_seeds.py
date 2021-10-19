from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import Contacto


def contacto_seeds(db: Session):
    try:
        db.add(
            Contacto(
                nombre="Maria",
                apellido="Cardozo",
                telefono="0981100100",
                email="maria@cardozo.com",
            )
        )
        db.add(
            Contacto(
                nombre="Pedro",
                apellido="Molinas",
                telefono="0981200200",
                email="pedro@molinas.com",
            )
        )
        db.add(
            Contacto(
                nombre="Sonia",
                apellido="Sanchez",
                telefono="0981300300",
                email="sonia@sanchez.com",
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
