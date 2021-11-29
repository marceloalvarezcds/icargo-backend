from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import MarcaSemi


def marca_semi_seeds(db: Session):
    try:
        db.add(MarcaSemi(descripcion="GUERRA"))
        db.add(MarcaSemi(descripcion="LIBRELATO"))
        db.add(MarcaSemi(descripcion="LUMAVIT"))
        db.add(MarcaSemi(descripcion="METALURGICA GUTIERREZ"))
        db.add(MarcaSemi(descripcion="NOMA"))
        db.add(MarcaSemi(descripcion="PHOENIX"))
        db.add(MarcaSemi(descripcion="RANDON"))
        db.add(MarcaSemi(descripcion="RODOVALE"))
        db.add(MarcaSemi(descripcion="TECNO EQUIPO"))
        db.commit()
    except IntegrityError:
        db.rollback()
