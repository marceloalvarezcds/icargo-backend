from typing import List, Optional

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


def get_composicion_juridica_list(db: Session) -> List[ComposicionJuridica]:
    return db.query(ComposicionJuridica).order_by(ComposicionJuridica.nombre).all()
