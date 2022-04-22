from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.schemas import Rentabilidad


def get_rentabilidad_list(
    db: Session, gestor_carga_id: Optional[int]
) -> List[Rentabilidad]:
    lista = repositories.get_orden_carga_list(db)
    if gestor_carga_id:
        lista = repositories.get_orden_carga_list_by_gestor_carga_id(
            db, gestor_carga_id
        )
    return Rentabilidad.get_list_by_oc(lista)
