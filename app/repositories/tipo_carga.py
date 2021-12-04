from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoCarga


def get_tipo_carga_by_descripcion(db: Session, descripcion: str) -> Optional[TipoCarga]:
    return db.query(TipoCarga).filter(TipoCarga.descripcion == descripcion).first()


def get_tipo_carga_list(db: Session) -> List[TipoCarga]:
    return db.query(TipoCarga).order_by(TipoCarga.descripcion).all()
