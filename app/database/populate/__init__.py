from sqlalchemy.orm import Session  # type: ignore

from .centro_operativo_seeds import centro_operativo_seeds


def populate(db: Session):  # Used only for test data in development
    pass
    centro_operativo_seeds(db)
