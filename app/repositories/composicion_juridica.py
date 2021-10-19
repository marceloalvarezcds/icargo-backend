from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import ComposicionJuridica


def get_composicion_juridica_by_nombre(
    db: Session, nombre: str
) -> Optional[ComposicionJuridica]:
    return (
        db.query(ComposicionJuridica)
        .filter(ComposicionJuridica.nombre == nombre)
        .first()
    )
