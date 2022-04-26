from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import ComposicionJuridica


def composicion_juridica_seeds(db: Session):
    try:
        db.add(ComposicionJuridica(nombre="Uni-personal", nombre_corto="U.P."))
        db.add(ComposicionJuridica(nombre="Sociedad Anónima", nombre_corto="S.A."))
        db.add(
            ComposicionJuridica(
                nombre="Sociedad de Responsabilidad Limitada", nombre_corto="S.R.L."
            )
        )
        db.add(ComposicionJuridica(nombre="Sociedad Cooperativa", nombre_corto="S.C."))
        db.commit()
    except IntegrityError:
        db.rollback()
