from typing import List

from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums import PermisoModuloEnum as u
from app.models import Permiso

from .permiso_seeds import permiso_seeds


def entities_admin_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.extend(permiso_generico_seeds(db))
    permisos.extend(permiso_centro_operativo_seeds(db))
    permisos.extend(permiso_gestor_carga_seeds(db))
    permisos.extend(permiso_proveedor_seeds(db))
    permisos.extend(permiso_punto_venta_seeds(db))
    permisos.extend(permiso_remitente_seeds(db))
    permisos.extend(permiso_transactional_user_seeds(db))
    permisos.append(
        permiso_seeds(
            db, a.CREAR, m.GESTOR_CARGA, u.ENTIDADES, "Crear Gestor de Carga", True
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.ELIMINAR,
            m.GESTOR_CARGA,
            u.ENTIDADES,
            "Eliminar Gestor de Carga",
            True,
        )
    )
    return permisos


def entities_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.extend(permiso_generico_seeds(db))
    permisos.extend(permiso_cargo_seeds(db))
    permisos.extend(permiso_centro_operativo_seeds(db))
    permisos.extend(permiso_gestor_carga_seeds(db))
    permisos.extend(permiso_proveedor_seeds(db))
    permisos.extend(permiso_punto_venta_seeds(db))
    permisos.extend(permiso_remitente_seeds(db))
    permisos.extend(permiso_transactional_user_seeds(db))
    return permisos


def permiso_generico_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(
        permiso_seeds(
            db,
            a.LISTAR,
            m.CENTRO_OPERATIVO_CLASIFICACION,
            u.PARAMETROS,
            "Listar Clasificación de Centro Operativo",
        )
    )
    permisos.append(permiso_seeds(db, a.LISTAR, m.CIUDAD, u.PARAMETROS))
    permisos.append(
        permiso_seeds(
            db,
            a.LISTAR,
            m.COMPOSICION_JURIDICA,
            u.PARAMETROS,
            "Listar Composición Jurídica",
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.CONTACTO, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.EDITAR, m.CONTACTO, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.LISTAR, m.LOCALIDAD, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.LISTAR, m.MONEDA, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.LISTAR, m.PAIS, u.PARAMETROS, "Listar País"))
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.TIPO_DOCUMENTO, u.PARAMETROS, "Listar Tipo de Documento"
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.USER, u.USUARIOS))
    return permisos


def permiso_cargo_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.CARGO, u.BIBLIOTECA))
    permisos.append(permiso_seeds(db, a.VER, m.CARGO, u.BIBLIOTECA))
    permisos.append(permiso_seeds(db, a.CREAR, m.CARGO, u.BIBLIOTECA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.CARGO, u.BIBLIOTECA))
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.CARGO, u.BIBLIOTECA))
    return permisos


def permiso_centro_operativo_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(
        permiso_seeds(
            db, a.CREAR, m.CENTRO_OPERATIVO, u.ENTIDADES, "Crear Centro Operativo"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.EDITAR, m.CENTRO_OPERATIVO, u.ENTIDADES, "Editar Centro Operativo"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.ELIMINAR, m.CENTRO_OPERATIVO, u.ENTIDADES, "Eliminar Centro Operativo"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.CENTRO_OPERATIVO, u.ENTIDADES, "Listar Centro Operativo"
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.CENTRO_OPERATIVO,
            u.ENTIDADES,
            "Modificar Contactos de Centro Operativo",
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_ALIAS,
            m.CENTRO_OPERATIVO,
            u.ENTIDADES,
            "Modificar Alias de Centro Operativo",
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.VER, m.CENTRO_OPERATIVO, u.ENTIDADES, "Ver Centro Operativo"
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.REPORTE,
            m.CENTRO_OPERATIVO,
            u.ENTIDADES,
            "Reporte de Centro Operativo",
        )
    )
    return permisos


def permiso_gestor_carga_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(
        permiso_seeds(
            db, a.EDITAR, m.GESTOR_CARGA, u.ENTIDADES, "Editar Gestor de Carga"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.GESTOR_CARGA, u.ENTIDADES, "Listar Gestor de Carga"
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.GESTOR_CARGA,
            u.ENTIDADES,
            "Modificar Contactos de Gestor de Carga",
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_ALIAS,
            m.GESTOR_CARGA,
            u.ENTIDADES,
            "Modificar Alias de Gestor de Carga",
        )
    )
    permisos.append(
        permiso_seeds(db, a.VER, m.GESTOR_CARGA, u.ENTIDADES, "Ver Gestor de Carga")
    )
    permisos.append(
        permiso_seeds(
            db, a.REPORTE, m.GESTOR_CARGA, u.ENTIDADES, "Reporte de Gestor de Carga"
        )
    )
    return permisos


def permiso_proveedor_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.PROVEEDOR, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.EDITAR, m.PROVEEDOR, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.PROVEEDOR, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.LISTAR, m.PROVEEDOR, u.ENTIDADES))
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.PROVEEDOR,
            u.ENTIDADES,
            "Modificar Contactos de Proveedor",
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_ALIAS,
            m.PROVEEDOR,
            u.ENTIDADES,
            "Modificar Alias de Proveedor",
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.PROVEEDOR, u.ENTIDADES))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.PROVEEDOR, u.ENTIDADES, "Reporte de Proveedor")
    )
    return permisos


def permiso_punto_venta_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(
        permiso_seeds(db, a.CREAR, m.PUNTO_VENTA, u.ENTIDADES, "Crear Punto de Venta")
    )
    permisos.append(
        permiso_seeds(db, a.EDITAR, m.PUNTO_VENTA, u.ENTIDADES, "Editar Punto de Venta")
    )
    permisos.append(
        permiso_seeds(
            db, a.ELIMINAR, m.PUNTO_VENTA, u.ENTIDADES, "Eliminar Punto de Venta"
        )
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.PUNTO_VENTA, u.ENTIDADES, "Listar Punto de Venta")
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.PUNTO_VENTA,
            u.ENTIDADES,
            "Modificar Contactos de Punto de Venta",
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_ALIAS,
            m.PUNTO_VENTA,
            u.ENTIDADES,
            "Modificar Alias de Punto de Venta",
        )
    )
    permisos.append(
        permiso_seeds(db, a.VER, m.PUNTO_VENTA, u.ENTIDADES, "Ver Punto de Venta")
    )
    permisos.append(
        permiso_seeds(
            db, a.REPORTE, m.PUNTO_VENTA, u.ENTIDADES, "Reporte de Punto de Venta"
        )
    )
    return permisos


def permiso_remitente_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.REMITENTE, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.EDITAR, m.REMITENTE, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.REMITENTE, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.LISTAR, m.REMITENTE, u.ENTIDADES))
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.REMITENTE,
            u.ENTIDADES,
            "Modificar Contactos de Remitente",
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_ALIAS,
            m.REMITENTE,
            u.ENTIDADES,
            "Modificar Alias de Remitente",
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.REMITENTE, u.ENTIDADES))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.REMITENTE, u.ENTIDADES, "Reporte de Remitente")
    )
    return permisos


def permiso_transactional_user_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(
        permiso_seeds(db, a.CAMBIAR_ESTADO, m.TRANSACTIONAL_USER, u.ENTIDADES)
    )
    permisos.append(permiso_seeds(db, a.CREAR, m.TRANSACTIONAL_USER, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.EDITAR, m.TRANSACTIONAL_USER, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.TRANSACTIONAL_USER, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TRANSACTIONAL_USER, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.VER, m.TRANSACTIONAL_USER, u.ENTIDADES))
    return permisos
