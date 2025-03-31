from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import Moneda
from app.models.gestor_carga import GestorCarga


def get_moneda_by_id(db: Session, id: int) -> Optional[Moneda]:
    return db.query(Moneda).get(id)


def get_moneda_by_simbolo(db: Session, simbolo: str) -> Optional[Moneda]:
    return db.query(Moneda).filter(Moneda.simbolo == simbolo).first()


def get_moneda_list(db: Session) -> List[Moneda]:
    return db.query(Moneda).order_by(Moneda.nombre).all()


def get_moneda_by_gestor_carga(db: Session, gestor_carga_id: int):
    gestor_carga = db.query(GestorCarga).filter(GestorCarga.id == gestor_carga_id).first()
    if gestor_carga and gestor_carga.moneda_id:
        return db.query(Moneda).filter(Moneda.id == gestor_carga.moneda_id).first()
    return None  
