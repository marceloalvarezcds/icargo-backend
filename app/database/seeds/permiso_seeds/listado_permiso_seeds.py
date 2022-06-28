from typing import List

from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums import PermisoModuloEnum as u
from app.models import Permiso

from .permiso_seeds import permiso_seeds


def listado_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.RENTABILIDAD, u.LISTADOS))
    permisos.append(permiso_seeds(db, a.REPORTE, m.RENTABILIDAD, u.LISTADOS))
    return permisos
