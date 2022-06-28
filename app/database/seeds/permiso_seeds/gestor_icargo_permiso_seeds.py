from typing import List

from sqlalchemy.orm import Session  # type: ignore

from app.models import Permiso

from .entities_permiso_seeds import entities_permiso_seeds
from .estado_cuenta_permiso_seeds import (
    estado_cuenta_gestor_permiso_seeds,
    estado_cuenta_permiso_seeds,
)
from .flete_permiso_seeds import flete_permiso_seeds
from .flota_permiso_seeds import flota_permiso_seeds
from .listado_permiso_seeds import listado_permiso_seeds
from .orden_carga_permiso_seeds import (
    orden_carga_gestor_permiso_seeds,
    orden_carga_permiso_seeds,
)
from .rol_permiso_seeds import rol_permiso_seeds
from .user_permiso_seeds import user_permiso_seeds


def gestor_icargo_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.extend(entities_permiso_seeds(db))
    permisos.extend(flete_permiso_seeds(db))
    permisos.extend(flota_permiso_seeds(db))
    permisos.extend(orden_carga_gestor_permiso_seeds(db))
    permisos.extend(estado_cuenta_gestor_permiso_seeds(db))
    permisos.extend(listado_permiso_seeds(db))
    permisos.extend(rol_permiso_seeds(db))
    permisos.extend(user_permiso_seeds(db))
    return permisos


def gestor_suplente_icargo_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.extend(entities_permiso_seeds(db))
    permisos.extend(flete_permiso_seeds(db))
    permisos.extend(flota_permiso_seeds(db))
    permisos.extend(orden_carga_permiso_seeds(db))
    permisos.extend(estado_cuenta_permiso_seeds(db))
    return permisos
