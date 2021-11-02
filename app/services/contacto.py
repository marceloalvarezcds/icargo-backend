from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models import Contacto


def get_contacto_by(
    db: Session, telefono: Optional[str], email: Optional[str]
) -> Optional[Contacto]:
    if telefono and email:
        return repositories.get_contacto_by_telefono_and_email(db, telefono, email)
    elif telefono:
        return repositories.get_contacto_by_telefono(db, telefono)
    elif email:
        return repositories.get_contacto_by_email(db, email)
    return None
