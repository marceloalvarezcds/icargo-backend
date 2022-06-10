from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import User

from .permiso_seeds import permiso_seeds


def entities_admin_permiso_seeds(db: Session, user: User):
    permiso_generico_seeds(db, user)
    permiso_centro_operativo_seeds(db, user)
    permiso_gestor_carga_seeds(db, user)
    permiso_proveedor_seeds(db, user)
    permiso_punto_venta_seeds(db, user)
    permiso_remitente_seeds(db, user)
    permisos = []
    permisos.append(
        permiso_seeds(db, a.CREAR, m.GESTOR_CARGA, True, "Crear Gestor de Carga")
    )
    permisos.append(
        permiso_seeds(db, a.ELIMINAR, m.GESTOR_CARGA, True, "Eliminar Gestor de Carga")
    )
    user.permisos.extend(permisos)
    db.commit()


def entities_permiso_seeds(db: Session, user: User):
    permiso_generico_seeds(db, user)
    permiso_cargo_seeds(db, user)
    permiso_centro_operativo_seeds(db, user)
    permiso_gestor_carga_seeds(db, user)
    permiso_proveedor_seeds(db, user)
    permiso_punto_venta_seeds(db, user)
    permiso_remitente_seeds(db, user)


def permiso_generico_seeds(db: Session, user: User):
    permisos = []
    permisos.append(
        permiso_seeds(
            db,
            a.LISTAR,
            m.CENTRO_OPERATIVO_CLASIFICACION,
            True,
            "Listar Clasificación de Centro Operativo",
        )
    )
    permisos.append(permiso_seeds(db, a.LISTAR, m.CIUDAD))
    permisos.append(
        permiso_seeds(
            db,
            a.LISTAR,
            m.COMPOSICION_JURIDICA,
            True,
            "Listar Composición Jurídica",
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.CONTACTO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.CONTACTO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.LOCALIDAD))
    permisos.append(permiso_seeds(db, a.LISTAR, m.MONEDA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.PAIS, True, "Listar País"))
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.TIPO_DOCUMENTO, True, "Listar Tipo de Documento")
    )
    permisos.append(permiso_seeds(db, a.VER, m.USER))
    user.permisos.extend(permisos)
    db.commit()


def permiso_cargo_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.CARGO))
    permisos.append(permiso_seeds(db, a.VER, m.CARGO))
    permisos.append(permiso_seeds(db, a.CREAR, m.CARGO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.CARGO))
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.CARGO))
    user.permisos.extend(permisos)
    db.commit()


def permiso_centro_operativo_seeds(db: Session, user: User):
    permisos = []
    permisos.append(
        permiso_seeds(db, a.CREAR, m.CENTRO_OPERATIVO, True, "Crear Centro Operativo")
    )
    permisos.append(
        permiso_seeds(db, a.EDITAR, m.CENTRO_OPERATIVO, True, "Editar Centro Operativo")
    )
    permisos.append(
        permiso_seeds(
            db, a.ELIMINAR, m.CENTRO_OPERATIVO, True, "Eliminar Centro Operativo"
        )
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.CENTRO_OPERATIVO, True, "Listar Centro Operativo")
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.CENTRO_OPERATIVO,
            True,
            "Modificar Contactos de Centro Operativo",
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_ALIAS,
            m.CENTRO_OPERATIVO,
            True,
            "Modificar Alias de Centro Operativo",
        )
    )
    permisos.append(
        permiso_seeds(db, a.VER, m.CENTRO_OPERATIVO, True, "Ver Centro Operativo")
    )
    permisos.append(
        permiso_seeds(
            db, a.REPORTE, m.CENTRO_OPERATIVO, True, "Reporte de Centro Operativo"
        )
    )
    user.permisos.extend(permisos)
    db.commit()


def permiso_gestor_carga_seeds(db: Session, user: User):
    permisos = []
    permisos.append(
        permiso_seeds(db, a.EDITAR, m.GESTOR_CARGA, True, "Editar Gestor de Carga")
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.GESTOR_CARGA, True, "Listar Gestor de Carga")
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.GESTOR_CARGA,
            True,
            "Modificar Contactos de Gestor de Carga",
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_ALIAS,
            m.GESTOR_CARGA,
            True,
            "Modificar Alias de Gestor de Carga",
        )
    )
    permisos.append(
        permiso_seeds(db, a.VER, m.GESTOR_CARGA, True, "Ver Gestor de Carga")
    )
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.GESTOR_CARGA, True, "Reporte de Gestor de Carga")
    )
    user.permisos.extend(permisos)
    db.commit()


def permiso_proveedor_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.PROVEEDOR))
    permisos.append(permiso_seeds(db, a.EDITAR, m.PROVEEDOR))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.PROVEEDOR))
    permisos.append(permiso_seeds(db, a.LISTAR, m.PROVEEDOR))
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.PROVEEDOR,
            True,
            "Modificar Contactos de Proveedor",
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.MODIFICAR_ALIAS, m.PROVEEDOR, True, "Modificar Alias de Proveedor"
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.PROVEEDOR))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.PROVEEDOR, True, "Reporte de Proveedor")
    )
    user.permisos.extend(permisos)
    db.commit()


def permiso_punto_venta_seeds(db: Session, user: User):
    permisos = []
    permisos.append(
        permiso_seeds(db, a.CREAR, m.PUNTO_VENTA, True, "Crear Punto de Venta")
    )
    permisos.append(
        permiso_seeds(db, a.EDITAR, m.PUNTO_VENTA, True, "Editar Punto de Venta")
    )
    permisos.append(
        permiso_seeds(db, a.ELIMINAR, m.PUNTO_VENTA, True, "Eliminar Punto de Venta")
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.PUNTO_VENTA, True, "Listar Punto de Venta")
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.PUNTO_VENTA,
            True,
            "Modificar Contactos de Punto de Venta",
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_ALIAS,
            m.PUNTO_VENTA,
            True,
            "Modificar Alias de Punto de Venta",
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.PUNTO_VENTA, True, "Ver Punto de Venta"))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.PUNTO_VENTA, True, "Reporte de Punto de Venta")
    )
    user.permisos.extend(permisos)
    db.commit()


def permiso_remitente_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.REMITENTE))
    permisos.append(permiso_seeds(db, a.EDITAR, m.REMITENTE))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.REMITENTE))
    permisos.append(permiso_seeds(db, a.LISTAR, m.REMITENTE))
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.REMITENTE,
            True,
            "Modificar Contactos de Remitente",
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.MODIFICAR_ALIAS, m.REMITENTE, True, "Modificar Alias de Remitente"
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.REMITENTE))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.REMITENTE, True, "Reporte de Remitente")
    )
    user.permisos.extend(permisos)
    db.commit()
