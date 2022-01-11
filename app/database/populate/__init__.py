from sqlalchemy.orm import Session  # type: ignore

from .cargo_seeds import cargo_seeds
from .composicion_juridica_seeds import composicion_juridica_seeds
from .contacto_seeds import contacto_seeds
from .flete_cargill_seeds import flete_cargill_seeds
from .flete_seeds import flete_seeds
from .gestor_carga_seeds import gestor_carga_seeds
from .orden_carga_seeds import orden_carga_seeds
from .tipo_documento_seeds import tipo_documento_seeds


def populate(db: Session):  # Used only for test data in development
    cargo_seeds(db)
    composicion_juridica_seeds(db)
    contacto_seeds(db)
    tipo_documento_seeds(db)
    gestor_carga_seeds(db)
    flete_seeds(db, 1)
    flete_cargill_seeds(db, 2)
    orden_carga_seeds(db, 1)
    orden_carga_seeds(db, 2)
