from typing import List, Union, cast, Optional
from sqlalchemy.orm import Session  # type: ignore
from app import repositories
from app.models import Factura


#def get_by_id(db: Session, id: int) -> List[Factura]:
#    return repositories.get_by_id(Rol, db, id)


def get_list(db: Session, gestor_carga_id: Optional[int]) -> List[Factura]:
    return repositories.get_all_contribuyente(db, gestor_carga_id)
