from typing import List

from sqlalchemy.orm.session import Session  # type: ignore

from app.models import Permiso

from .entities_permiso_seeds import entities_admin_permiso_seeds
from .estado_cuenta_permiso_seeds import estado_cuenta_permiso_seeds
from .flete_permiso_seeds import flete_admin_permiso_seeds
from .flota_permiso_seeds import flota_admin_permiso_seeds
from .listado_permiso_seeds import listado_permiso_seeds
from .orden_carga_permiso_seeds import orden_carga_admin_permiso_seeds
from .rol_permiso_seeds import rol_permiso_seeds
from .user_permiso_seeds import user_permiso_seeds


def admin_icargo_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.extend(entities_admin_permiso_seeds(db))
    permisos.extend(estado_cuenta_permiso_seeds(db))
    permisos.extend(flete_admin_permiso_seeds(db))
    permisos.extend(flota_admin_permiso_seeds(db))
    permisos.extend(listado_permiso_seeds(db))
    permisos.extend(orden_carga_admin_permiso_seeds(db))
    permisos.extend(user_permiso_seeds(db))
    permisos.extend(rol_permiso_seeds(db))
    return permisos
