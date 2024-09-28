from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoIncidente


def get_tipo_incidente_by_descripcion(
    db: Session, descripcion: str
) -> Optional[TipoIncidente]:
    return (
        db.query(TipoIncidente).filter(TipoIncidente.descripcion == descripcion).first()
    )


def get_tipo_incidente_list(db: Session) -> List[TipoIncidente]:
    return db.query(TipoIncidente).order_by(TipoIncidente.descripcion).all()
