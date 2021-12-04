from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import MarcaCamion


def marca_camion_seeds(db: Session):
    try:
        db.add(MarcaCamion(descripcion="LUMAVIT"))
        db.add(MarcaCamion(descripcion="MERCEDES BENZ"))
        db.add(MarcaCamion(descripcion="METALURGICA GUTIERREZ"))
        db.add(MarcaCamion(descripcion="PHOENIX"))
        db.add(MarcaCamion(descripcion="SCANIA"))
        db.add(MarcaCamion(descripcion="TECNO EQUIPO"))
        db.add(MarcaCamion(descripcion="VOLVO"))
        db.commit()
    except IntegrityError:
        db.rollback()
