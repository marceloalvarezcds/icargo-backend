from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums import PermisoModuloEnum as u
from app.models import User

from .permiso_seeds import permiso_seeds


def user_permiso_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.USER, u.USUARIOS))
    permisos.append(permiso_seeds(db, a.CREAR, m.USER, u.USUARIOS))
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.USER, u.USUARIOS))
    permisos.append(permiso_seeds(db, a.EDITAR, m.USER, u.USUARIOS))
    permisos.append(permiso_seeds(db, a.VER, m.USER, u.USUARIOS))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.USER, u.USUARIOS))
    user.permisos.extend(permisos)
    db.commit()
