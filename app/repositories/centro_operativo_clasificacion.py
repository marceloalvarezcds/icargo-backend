from typing import List, Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import CentroOperativoClasificacion


def get_centro_operativo_clasificacion_by_nombre(
    db: Session, nombre: str
) -> Optional[CentroOperativoClasificacion]:
    return (
        db.query(CentroOperativoClasificacion)
        .filter(CentroOperativoClasificacion.nombre == nombre)
        .first()
    )


def get_centro_operativo_clasificacion_list(
    db: Session,
) -> List[CentroOperativoClasificacion]:
    return (
        db.query(CentroOperativoClasificacion)
        .order_by(CentroOperativoClasificacion.id.desc())
        .all()
    )
