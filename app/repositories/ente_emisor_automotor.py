from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import EnteEmisorAutomotor


def get_ente_emisor_automotor_by_descripcion(
    db: Session, descripcion: str
) -> Optional[EnteEmisorAutomotor]:
    return (
        db.query(EnteEmisorAutomotor)
        .filter(EnteEmisorAutomotor.descripcion == descripcion)
        .first()
    )


def get_ente_emisor_automotor_list(db: Session) -> List[EnteEmisorAutomotor]:
    return db.query(EnteEmisorAutomotor).order_by(EnteEmisorAutomotor.descripcion).all()
