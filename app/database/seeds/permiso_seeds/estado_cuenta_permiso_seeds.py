from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import User

from .permiso_seeds import permiso_seeds


def estado_cuenta_permiso_seeds(db: Session, user: User):
    permiso_generico_seeds(db, user)
    permiso_banco_seeds(db, user)
    permiso_caja_seeds(db, user)
    permiso_instrumento_seeds(db, user)
    permiso_movimiento_seeds(db, user)
    permiso_liquidacion_seeds(db, user)


def permiso_generico_seeds(db: Session, user: User):
    permisos = []
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.ESTADO_CUENTA, True, "Listar Estado de cuenta")
    )
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.ESTADO_CUENTA, True, "Reporte Estado de cuenta")
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.TIPO_CONTRAPARTE, True, "Listar Tipo de contraparte"
        )
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.TIPO_CUENTA, True, "Listar Tipo de cuenta")
    )
    permisos.append(
        permiso_seeds(
            db,
            a.LISTAR,
            m.TIPO_DOCUMENTO_RELACIONADO,
            True,
            "Listar Tipo de documento relacionado",
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.TIPO_INSTRUMENTO, True, "Listar Tipo de instrumento"
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.LISTAR,
            m.TIPO_MOVIMIENTO,
            True,
            "Listar Tipo de movimiento",
        )
    )
    user.permisos.extend(permisos)
    db.commit()


def permiso_banco_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.BANCO, True))
    permisos.append(permiso_seeds(db, a.EDITAR, m.BANCO, True))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.BANCO, True))
    permisos.append(permiso_seeds(db, a.LISTAR, m.BANCO, True))
    permisos.append(permiso_seeds(db, a.VER, m.BANCO, True))
    permisos.append(permiso_seeds(db, a.REPORTE, m.BANCO, True))
    user.permisos.extend(permisos)
    db.commit()


def permiso_caja_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.CAJA, True))
    permisos.append(permiso_seeds(db, a.EDITAR, m.CAJA, True))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.CAJA, True))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CAJA, True))
    permisos.append(permiso_seeds(db, a.VER, m.CAJA, True))
    permisos.append(
        permiso_seeds(
            db,
            a.REPORTE,
            m.CAJA,
            True,
        )
    )
    user.permisos.extend(permisos)
    db.commit()


def permiso_instrumento_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.INSTRUMENTO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.INSTRUMENTO))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.INSTRUMENTO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.INSTRUMENTO))
    permisos.append(permiso_seeds(db, a.VER, m.INSTRUMENTO))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.INSTRUMENTO, True, "Reporte de Instrumento")
    )
    user.permisos.extend(permisos)
    db.commit()


def permiso_movimiento_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.MOVIMIENTO, True))
    permisos.append(permiso_seeds(db, a.EDITAR, m.MOVIMIENTO, True))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.MOVIMIENTO, True))
    permisos.append(permiso_seeds(db, a.LISTAR, m.MOVIMIENTO, True))
    permisos.append(permiso_seeds(db, a.VER, m.MOVIMIENTO, True))
    permisos.append(
        permiso_seeds(
            db,
            a.REPORTE,
            m.MOVIMIENTO,
            True,
        )
    )
    user.permisos.extend(permisos)
    db.commit()


def permiso_liquidacion_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.LIQUIDACION))
    permisos.append(permiso_seeds(db, a.EDITAR, m.LIQUIDACION))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.LIQUIDACION))
    permisos.append(permiso_seeds(db, a.LISTAR, m.LIQUIDACION))
    permisos.append(permiso_seeds(db, a.VER, m.LIQUIDACION))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.LIQUIDACION, True, "Reporte de Remitente")
    )
    user.permisos.extend(permisos)
    db.commit()
