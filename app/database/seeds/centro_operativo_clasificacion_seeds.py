from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import CentroOperativoClasificacion


def centro_operativo_clasificacion_seeds(db: Session):
    try:
        db.add(
            CentroOperativoClasificacion(nombre="Silo", estado=EstadoEnum.ACTIVO.value)
        )
        db.add(
            CentroOperativoClasificacion(
                nombre="Puerto seco", estado=EstadoEnum.ACTIVO.value
            )
        )
        db.add(
            CentroOperativoClasificacion(
                nombre="Puerto multimodal", estado=EstadoEnum.ACTIVO.value
            )
        )
        db.add(
            CentroOperativoClasificacion(
                nombre="Deposito", estado=EstadoEnum.ACTIVO.value
            )
        )
        db.add(
            CentroOperativoClasificacion(
                nombre="Centro de distribución", estado=EstadoEnum.ACTIVO.value
            )
        )
        db.add(
            CentroOperativoClasificacion(nombre="Campo", estado=EstadoEnum.ACTIVO.value)
        )
        db.add(
            CentroOperativoClasificacion(
                nombre="Aduana", estado=EstadoEnum.ACTIVO.value
            )
        )
        db.add(
            CentroOperativoClasificacion(
                nombre="Acopio", estado=EstadoEnum.ACTIVO.value
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
