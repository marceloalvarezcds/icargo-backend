from sqlalchemy.orm import Session  # type: ignore

from .centro_operativo_clasificacion_seeds import centro_operativo_clasificacion_seeds
from .moneda_seeds import moneda_seeds
from .pais_seeds import pais_seeds
from .user_seeds import user_seeds


def seeds(db: Session):
    centro_operativo_clasificacion_seeds(db)
    moneda_seeds(db)
    pais_seeds(db)
    user_seeds(db)
