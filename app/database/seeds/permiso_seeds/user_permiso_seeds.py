from typing import List

from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums import PermisoModuloEnum as u
from app.models import Permiso

from .permiso_seeds import permiso_seeds


def user_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.USER, u.USUARIOS))
    permisos.append(permiso_seeds(db, a.CREAR, m.USER, u.USUARIOS))
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.USER, u.USUARIOS))
    permisos.append(permiso_seeds(db, a.EDITAR, m.USER, u.USUARIOS))
    permisos.append(permiso_seeds(db, a.VER, m.USER, u.USUARIOS))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.USER, u.USUARIOS))
    return permisos
