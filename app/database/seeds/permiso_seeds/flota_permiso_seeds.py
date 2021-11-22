from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import User

from .permiso_seeds import permiso_seeds


def flota_permiso_seeds(db: Session, user: User):
    permiso_generico_seeds(db, user)
    permiso_propietario_seeds(db, user)


def permiso_generico_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.CARGO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CIUDAD))
    permisos.append(permiso_seeds(db, a.VER, m.CONTACTO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.LOCALIDAD))
    permisos.append(permiso_seeds(db, a.LISTAR, m.PAIS, True, "Listar País"))
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.TIPO_PERSONA, True, "Listar Tipo de Persona")
    )
    permisos.append(permiso_seeds(db, a.LISTAR, m.USER))
    permisos.append(permiso_seeds(db, a.VER, m.USER))
    user.permisos.extend(permisos)
    db.commit()


def permiso_propietario_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.PROPIETARIO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.PROPIETARIO))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.PROPIETARIO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.PROPIETARIO))
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.PROPIETARIO,
            True,
            "Modificar Contactos de Propietario",
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.MODIFICAR_ALIAS, m.PROPIETARIO, True, "Modificar Alias de Propietario"
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.PROPIETARIO))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.PROPIETARIO, True, "Reporte de Propietario")
    )
    user.permisos.extend(permisos)
    db.commit()
