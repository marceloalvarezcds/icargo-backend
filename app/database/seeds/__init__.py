from sqlalchemy.orm import Session  # type: ignore

from .centro_operativo_clasificacion_seeds import centro_operativo_clasificacion_seeds
from .color_seeds import color_seeds
from .moneda_seeds import moneda_seeds
from .pais_seeds import pais_seeds
from .rol_seeds import rol_seeds
from .tipo_persona_seeds import tipo_persona_seeds
from .tipo_registro_seeds import tipo_registro_seeds
from .user_seeds import user_seeds


def seeds(db: Session):
    centro_operativo_clasificacion_seeds(db)
    color_seeds(db)
    moneda_seeds(db)
    pais_seeds(db)
    rol_seeds(db)
    tipo_persona_seeds(db)
    tipo_registro_seeds(db)
    user_seeds(db)
