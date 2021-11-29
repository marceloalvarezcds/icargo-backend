from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import EnteEmisorTransporte


def get_ente_emisor_transporte_by_descripcion(
    db: Session, descripcion: str
) -> Optional[EnteEmisorTransporte]:
    return (
        db.query(EnteEmisorTransporte)
        .filter(EnteEmisorTransporte.descripcion == descripcion)
        .first()
    )


def get_ente_emisor_transporte_list(db: Session) -> List[EnteEmisorTransporte]:
    return (
        db.query(EnteEmisorTransporte).order_by(EnteEmisorTransporte.descripcion).all()
    )
