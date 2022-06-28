from typing import List

from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums import PermisoModuloEnum as u
from app.models import Permiso

from .permiso_seeds import permiso_seeds


def flete_admin_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.extend(permiso_generico_seeds(db))
    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE, u.FLETE))
    permisos.append(permiso_seeds(db, a.VER, m.FLETE, u.FLETE))
    permisos.append(permiso_seeds(db, a.REPORTE, m.FLETE, u.FLETE, "Reporte de Flete"))
    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE_ANTICIPO, u.FLETE))
    permisos.append(permiso_seeds(db, a.VER, m.FLETE_ANTICIPO, u.FLETE))
    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE_COMPLEMENTO, u.FLETE))
    permisos.append(permiso_seeds(db, a.VER, m.FLETE_COMPLEMENTO, u.FLETE))
    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE_DESCUENTO, u.FLETE))
    permisos.append(permiso_seeds(db, a.VER, m.FLETE_DESCUENTO, u.FLETE))
    return permisos


def flete_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.extend(permiso_generico_seeds(db))
    permisos.extend(permiso_flete_seeds(db))
    permisos.extend(permiso_flete_anticipo_seeds(db))
    permisos.extend(permiso_flete_complemento_seeds(db))
    permisos.extend(permiso_flete_descuento_seeds(db))
    return permisos


def permiso_generico_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.CENTRO_OPERATIVO, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.LISTAR, m.MONEDA, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.LISTAR, m.PRODUCTO, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.LISTAR, m.REMITENTE, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_ANTICIPO, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_CARGA, u.PARAMETROS))
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.TIPO_CONCEPTO_COMPLEMENTO, u.PARAMETROS)
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.TIPO_CONCEPTO_DESCUENTO, u.PARAMETROS)
    )
    permisos.append(permiso_seeds(db, a.LISTAR, m.UNIDAD, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.VER, m.CONTACTO, u.FLETE))
    return permisos


def permiso_flete_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.FLETE, u.FLETE))
    permisos.append(permiso_seeds(db, a.CREAR, m.FLETE, u.FLETE))
    permisos.append(permiso_seeds(db, a.EDITAR, m.FLETE, u.FLETE))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.FLETE, u.FLETE))
    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE, u.FLETE))
    permisos.append(permiso_seeds(db, a.VER, m.FLETE, u.FLETE))
    permisos.append(permiso_seeds(db, a.REPORTE, m.FLETE, u.FLETE, "Reporte de Flete"))
    return permisos


def permiso_flete_anticipo_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(
        permiso_seeds(db, a.CREAR, m.FLETE_ANTICIPO, u.FLETE, "Crear Anticipo de Flete")
    )
    permisos.append(
        permiso_seeds(
            db, a.EDITAR, m.FLETE_ANTICIPO, u.FLETE, "Editar Anticipo de Flete"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.ELIMINAR, m.FLETE_ANTICIPO, u.FLETE, "Eliminar Anticipo de Flete"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.FLETE_ANTICIPO, u.FLETE, "Listar Anticipo de Flete"
        )
    )
    permisos.append(
        permiso_seeds(db, a.VER, m.FLETE_ANTICIPO, u.FLETE, "Ver Anticipo de Flete")
    )
    return permisos


def permiso_flete_complemento_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(
        permiso_seeds(
            db, a.CREAR, m.FLETE_COMPLEMENTO, u.FLETE, "Crear Complemento de Flete"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.EDITAR, m.FLETE_COMPLEMENTO, u.FLETE, "Editar Complemento de Flete"
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.ELIMINAR,
            m.FLETE_COMPLEMENTO,
            u.FLETE,
            "Eliminar Complemento de Flete",
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.FLETE_COMPLEMENTO, u.FLETE, "Listar Complemento de Flete"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.VER, m.FLETE_COMPLEMENTO, u.FLETE, "Ver Complemento de Flete"
        )
    )
    return permisos


def permiso_flete_descuento_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(
        permiso_seeds(
            db, a.CREAR, m.FLETE_DESCUENTO, u.FLETE, "Crear Descuento de Flete"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.EDITAR, m.FLETE_DESCUENTO, u.FLETE, "Editar Descuento de Flete"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.ELIMINAR, m.FLETE_DESCUENTO, u.FLETE, "Eliminar Descuento de Flete"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.FLETE_DESCUENTO, u.FLETE, "Listar Descuento de Flete"
        )
    )
    permisos.append(
        permiso_seeds(db, a.VER, m.FLETE_DESCUENTO, u.FLETE, "Ver Descuento de Flete")
    )
    return permisos
