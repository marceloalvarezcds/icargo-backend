from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import SemiClasificacion


def semi_clasificacion_seeds(db: Session):
    try:
        db.add(SemiClasificacion(descripcion="CARRETA ABIERTA"))
        db.add(SemiClasificacion(descripcion="GRANELERO"))
        db.add(SemiClasificacion(descripcion="PLANCHA"))
        db.add(SemiClasificacion(descripcion="SIDER"))
        db.add(SemiClasificacion(descripcion="TANQUE"))
        db.add(SemiClasificacion(descripcion="TANQUE INOX"))
        db.commit()
    except IntegrityError:
        db.rollback()
