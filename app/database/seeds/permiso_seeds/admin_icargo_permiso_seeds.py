from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import User

from .entities_permiso_seeds import entities_permiso_seeds
from .flete_permiso_seeds import flete_admin_permiso_seeds
from .flota_permiso_seeds import flota_admin_permiso_seeds
from .orden_carga_permiso_seeds import orden_carga_admin_permiso_seeds
from .permiso_seeds import permiso_seeds


def admin_icargo_permiso_seeds(db: Session, user: User):
    entities_permiso_seeds(db, user)
    flete_admin_permiso_seeds(db, user)
    flota_admin_permiso_seeds(db, user)
    orden_carga_admin_permiso_seeds(db, user)
    user_permiso_seeds(db, user)


def user_permiso_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.PERMISO))
    permisos.append(permiso_seeds(db, a.CREAR, m.USER))
    user.permisos.extend(permisos)
    db.commit()
