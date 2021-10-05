from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import CentroOperativoClasificacion


def centro_operativo_clasificacion_seeds(db: Session):
    try:
        db.add(CentroOperativoClasificacion(nombre="Silo", es_moderado=True))
        db.add(CentroOperativoClasificacion(nombre="Puerto seco", es_moderado=True))
        db.add(
            CentroOperativoClasificacion(nombre="Puerto multimodal", es_moderado=True)
        )
        db.add(CentroOperativoClasificacion(nombre="Deposito", es_moderado=True))
        db.add(
            CentroOperativoClasificacion(
                nombre="Centro de distribución", es_moderado=True
            )
        )
        db.add(CentroOperativoClasificacion(nombre="Campo", es_moderado=True))
        db.add(CentroOperativoClasificacion(nombre="Aduana", es_moderado=True))
        db.add(CentroOperativoClasificacion(nombre="Acopio", es_moderado=True))
        db.commit()
    except IntegrityError:
        db.rollback()
