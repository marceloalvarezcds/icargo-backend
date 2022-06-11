from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import User

from .permiso_seeds import permiso_seeds


def user_permiso_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.PERMISO))
    permisos.append(permiso_seeds(db, a.CREAR, m.USER))
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.USER))
    permisos.append(permiso_seeds(db, a.EDITAR, m.USER))
    permisos.append(permiso_seeds(db, a.VER, m.USER))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.USER))
    user.permisos.extend(permisos)
    db.commit()
