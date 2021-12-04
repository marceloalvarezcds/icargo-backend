from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import SemiClasificacion


def get_semi_clasificacion_by_descripcion(
    db: Session, descripcion: str
) -> Optional[SemiClasificacion]:
    return (
        db.query(SemiClasificacion)
        .filter(SemiClasificacion.descripcion == descripcion)
        .first()
    )


def get_semi_clasificacion_list(db: Session) -> List[SemiClasificacion]:
    return db.query(SemiClasificacion).order_by(SemiClasificacion.descripcion).all()
