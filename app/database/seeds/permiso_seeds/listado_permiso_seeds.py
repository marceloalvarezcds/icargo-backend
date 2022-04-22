from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import User

from .permiso_seeds import permiso_seeds


def listado_permiso_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.RENTABILIDAD))
    user.permisos.extend(permisos)
    db.commit()
