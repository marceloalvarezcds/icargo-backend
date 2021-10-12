from typing import List

from sqlalchemy.orm import Session  # type: ignore

from app.models import CentroOperativoClasificacion


def get_centro_operativo_clasificacion_list(
    db: Session,
) -> List[CentroOperativoClasificacion]:
    return db.query(CentroOperativoClasificacion).all()
