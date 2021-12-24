from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import User

from .permiso_seeds import permiso_seeds


def flete_admin_permiso_seeds(db: Session, user: User):
    permiso_generico_seeds(db, user)
    permisos = []

    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE))
    permisos.append(permiso_seeds(db, a.VER, m.FLETE))
    permisos.append(permiso_seeds(db, a.REPORTE, m.FLETE, True, "Reporte de Flete"))

    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE_ANTICIPO))
    permisos.append(permiso_seeds(db, a.VER, m.FLETE_ANTICIPO))

    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE_COMPLEMENTO))
    permisos.append(permiso_seeds(db, a.VER, m.FLETE_COMPLEMENTO))

    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE_DESCUENTO))
    permisos.append(permiso_seeds(db, a.VER, m.FLETE_DESCUENTO))

    user.permisos.extend(permisos)
    db.commit()


def flete_permiso_seeds(db: Session, user: User):
    permiso_generico_seeds(db, user)
    permiso_flete_seeds(db, user)
    permiso_flete_anticipo_seeds(db, user)
    permiso_flete_complemento_seeds(db, user)
    permiso_flete_descuento_seeds(db, user)


def permiso_generico_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.CENTRO_OPERATIVO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.MONEDA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.PRODUCTO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.REMITENTE))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_ANTICIPO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_CARGA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_CONCEPTO_COMPLEMENTO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_CONCEPTO_DESCUENTO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.UNIDAD))
    permisos.append(permiso_seeds(db, a.VER, m.CONTACTO))
    user.permisos.extend(permisos)
    db.commit()


def permiso_flete_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.FLETE))
    permisos.append(permiso_seeds(db, a.CREAR, m.FLETE))
    permisos.append(permiso_seeds(db, a.EDITAR, m.FLETE))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.FLETE))
    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE))
    permisos.append(permiso_seeds(db, a.VER, m.FLETE))
    permisos.append(permiso_seeds(db, a.REPORTE, m.FLETE, True, "Reporte de Flete"))
    user.permisos.extend(permisos)
    db.commit()


def permiso_flete_anticipo_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.FLETE_ANTICIPO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.FLETE_ANTICIPO))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.FLETE_ANTICIPO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE_ANTICIPO))
    permisos.append(permiso_seeds(db, a.VER, m.FLETE_ANTICIPO))
    user.permisos.extend(permisos)
    db.commit()


def permiso_flete_complemento_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.FLETE_COMPLEMENTO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.FLETE_COMPLEMENTO))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.FLETE_COMPLEMENTO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE_COMPLEMENTO))
    permisos.append(permiso_seeds(db, a.VER, m.FLETE_COMPLEMENTO))
    user.permisos.extend(permisos)
    db.commit()


def permiso_flete_descuento_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.FLETE_DESCUENTO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.FLETE_DESCUENTO))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.FLETE_DESCUENTO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE_DESCUENTO))
    permisos.append(permiso_seeds(db, a.VER, m.FLETE_DESCUENTO))
    user.permisos.extend(permisos)
    db.commit()
