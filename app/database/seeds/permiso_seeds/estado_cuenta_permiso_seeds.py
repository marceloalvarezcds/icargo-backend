from typing import List

from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums import PermisoModuloEnum as u
from app.models import Permiso

from .permiso_seeds import permiso_seeds


def estado_cuenta_gestor_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.extend(permiso_generico_seeds(db))
    permisos.extend(permiso_banco_seeds(db))
    permisos.extend(permiso_caja_seeds(db))
    permisos.extend(permiso_factura_seeds(db))
    permisos.extend(permiso_instrumento_seeds(db))
    permisos.extend(permiso_movimiento_seeds(db))
    permisos.extend(permiso_liquidacion_seeds(db))
    permisos.append(permiso_seeds(db, a.ACEPTAR, m.LIQUIDACION, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.CANCELAR, m.LIQUIDACION, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.RECHAZAR, m.LIQUIDACION, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.INSTRUMENTO, u.ESTADO_CUENTA))
    return permisos


def estado_cuenta_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.extend(permiso_generico_seeds(db))
    permisos.extend(permiso_banco_seeds(db))
    permisos.extend(permiso_caja_seeds(db))
    permisos.extend(permiso_factura_seeds(db))
    permisos.extend(permiso_instrumento_seeds(db))
    permisos.extend(permiso_movimiento_seeds(db))
    permisos.extend(permiso_liquidacion_seeds(db))
    permisos.extend(permiso_tipo_cuenta_seeds(db))
    permisos.extend(permiso_tipo_movimiento_seeds(db))
    permisos.append(
        permiso_seeds(db, a.PASAR_A_REVISION, m.LIQUIDACION, u.ESTADO_CUENTA)
    )
    return permisos


def permiso_generico_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.ESTADO_CUENTA, u.ESTADO_CUENTA, "Listar Estado de cuenta"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.REPORTE, m.ESTADO_CUENTA, u.ESTADO_CUENTA, "Reporte Estado de cuenta"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.VER, m.ESTADO_CUENTA, u.ESTADO_CUENTA, "Ver Estado de cuenta"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.INSTRUMENTO_VIA, u.PARAMETROS, "Listar Instrumento via"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.TIPO_CONTRAPARTE, u.PARAMETROS, "Listar Tipo de contraparte"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.TIPO_CUENTA, u.PARAMETROS, "Listar Tipo de cuenta"
        )
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.TIPO_IVA, u.PARAMETROS, "Listar Tipo de IVA")
    )
    permisos.append(
        permiso_seeds(
            db,
            a.LISTAR,
            m.TIPO_DOCUMENTO_RELACIONADO,
            u.PARAMETROS,
            "Listar Tipo de documento relacionado",
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.TIPO_INSTRUMENTO, u.PARAMETROS, "Listar Tipo de instrumento"
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.LISTAR,
            m.TIPO_MOVIMIENTO,
            u.PARAMETROS,
            "Listar Tipo de movimiento",
        )
    )
    return permisos


def permiso_banco_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.BANCO, u.CAJA_BANCO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.BANCO, u.CAJA_BANCO))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.BANCO, u.CAJA_BANCO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.BANCO, u.CAJA_BANCO))
    permisos.append(permiso_seeds(db, a.VER, m.BANCO, u.CAJA_BANCO))
    permisos.append(permiso_seeds(db, a.REPORTE, m.BANCO, u.CAJA_BANCO))
    return permisos


def permiso_caja_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.CAJA, u.CAJA_BANCO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.CAJA, u.CAJA_BANCO))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.CAJA, u.CAJA_BANCO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CAJA, u.CAJA_BANCO))
    permisos.append(permiso_seeds(db, a.VER, m.CAJA, u.CAJA_BANCO))
    permisos.append(
        permiso_seeds(
            db,
            a.REPORTE,
            m.CAJA,
            u.CAJA_BANCO,
        )
    )
    return permisos


def permiso_factura_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.FACTURA, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.FACTURA, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.FACTURA, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.FACTURA, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.VER, m.FACTURA, u.ESTADO_CUENTA))
    return permisos


def permiso_instrumento_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.INSTRUMENTO, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.INSTRUMENTO, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.INSTRUMENTO, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.INSTRUMENTO, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.VER, m.INSTRUMENTO, u.ESTADO_CUENTA))
    permisos.append(
        permiso_seeds(
            db, a.REPORTE, m.INSTRUMENTO, u.ESTADO_CUENTA, "Reporte de Instrumento"
        )
    )
    return permisos


def permiso_movimiento_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.MOVIMIENTO, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.MOVIMIENTO, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.MOVIMIENTO, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.MOVIMIENTO, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.VER, m.MOVIMIENTO, u.ESTADO_CUENTA))
    permisos.append(
        permiso_seeds(
            db,
            a.REPORTE,
            m.MOVIMIENTO,
            u.ESTADO_CUENTA,
        )
    )
    return permisos


def permiso_liquidacion_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.LIQUIDACION, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.LIQUIDACION, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.LIQUIDACION, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.LIQUIDACION, u.ESTADO_CUENTA))
    permisos.append(permiso_seeds(db, a.VER, m.LIQUIDACION, u.ESTADO_CUENTA))
    permisos.append(
        permiso_seeds(
            db, a.REPORTE, m.LIQUIDACION, u.ESTADO_CUENTA, "Reporte de Liquidación"
        )
    )
    return permisos


def permiso_tipo_cuenta_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_CUENTA, u.BIBLIOTECA))
    permisos.append(permiso_seeds(db, a.VER, m.TIPO_CUENTA, u.BIBLIOTECA))
    permisos.append(permiso_seeds(db, a.CREAR, m.TIPO_CUENTA, u.BIBLIOTECA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.TIPO_CUENTA, u.BIBLIOTECA))
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.TIPO_CUENTA, u.BIBLIOTECA))
    return permisos


def permiso_tipo_movimiento_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_MOVIMIENTO, u.BIBLIOTECA))
    permisos.append(permiso_seeds(db, a.VER, m.TIPO_MOVIMIENTO, u.BIBLIOTECA))
    permisos.append(permiso_seeds(db, a.CREAR, m.TIPO_MOVIMIENTO, u.BIBLIOTECA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.TIPO_MOVIMIENTO, u.BIBLIOTECA))
    permisos.append(
        permiso_seeds(db, a.CAMBIAR_ESTADO, m.TIPO_MOVIMIENTO, u.BIBLIOTECA)
    )
    return permisos
