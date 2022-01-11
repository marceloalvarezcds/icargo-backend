from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import User

from .permiso_seeds import permiso_seeds


def flota_admin_permiso_seeds(db: Session, user: User):
    permiso_generico_seeds(db, user)
    permisos = []

    permisos.append(permiso_seeds(db, a.LISTAR, m.CAMION))
    permisos.append(permiso_seeds(db, a.VER, m.CAMION))
    permisos.append(permiso_seeds(db, a.REPORTE, m.CAMION, True, "Reporte de Camion"))

    permisos.append(permiso_seeds(db, a.LISTAR, m.CAMION_SEMI_NETO))
    permisos.append(permiso_seeds(db, a.VER, m.CAMION_SEMI_NETO))

    permisos.append(permiso_seeds(db, a.LISTAR, m.CHOFER))
    permisos.append(permiso_seeds(db, a.VER, m.CHOFER))
    permisos.append(permiso_seeds(db, a.REPORTE, m.CHOFER, True, "Reporte de Chofer"))

    permisos.append(permiso_seeds(db, a.LISTAR, m.PROPIETARIO))
    permisos.append(permiso_seeds(db, a.VER, m.PROPIETARIO))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.PROPIETARIO, True, "Reporte de Propietario")
    )

    permisos.append(permiso_seeds(db, a.LISTAR, m.SEMIRREMOLQUE))
    permisos.append(permiso_seeds(db, a.VER, m.SEMIRREMOLQUE))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.SEMIRREMOLQUE, True, "Reporte de Semirremolque")
    )

    user.permisos.extend(permisos)
    db.commit()


def flota_permiso_seeds(db: Session, user: User):
    permiso_generico_seeds(db, user)
    permiso_camion_seeds(db, user)
    permiso_camion_semi_neto_seeds(db, user)
    permiso_chofer_seeds(db, user)
    permiso_propietario_seeds(db, user)
    permiso_semirremolque_seeds(db, user)


def permiso_generico_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.CARGO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CIUDAD))
    permisos.append(permiso_seeds(db, a.LISTAR, m.COLOR))
    permisos.append(permiso_seeds(db, a.VER, m.CONTACTO))
    permisos.append(
        permiso_seeds(
            db,
            a.LISTAR,
            m.ENTE_EMISOR_AUTOMOTOR,
            True,
            "Listar Ente Emisor del Automotor",
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.LISTAR,
            m.ENTE_EMISOR_TRANSPORTE,
            True,
            "Listar Ente Emisor del Transporte",
        )
    )
    permisos.append(permiso_seeds(db, a.LISTAR, m.LOCALIDAD))
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.MARCA_CAMION, True, "Listar Marca de Camión")
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.MARCA_SEMI, True, "Listar Marca de Semi")
    )
    permisos.append(permiso_seeds(db, a.LISTAR, m.PAIS, True, "Listar País"))
    permisos.append(
        permiso_seeds(
            db,
            a.LISTAR,
            m.SEMI_CLASIFICACION,
            True,
            "Listar Clasificación Semi-remolque",
        )
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.TIPO_CAMION, True, "Listar Tipo de Camion")
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.TIPO_CARGA, True, "Listar Tipo de Carga")
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.TIPO_PERSONA, True, "Listar Tipo de Persona")
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.TIPO_REGISTRO, True, "Listar Tipo de Registro")
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.TIPO_SEMI, True, "Listar Tipo de Semi-Remolque")
    )
    permisos.append(permiso_seeds(db, a.LISTAR, m.USER))
    permisos.append(permiso_seeds(db, a.VER, m.USER))
    user.permisos.extend(permisos)
    db.commit()


def permiso_camion_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.CAMION))
    permisos.append(permiso_seeds(db, a.CREAR, m.CAMION))
    permisos.append(permiso_seeds(db, a.EDITAR, m.CAMION))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.CAMION))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CAMION))
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.CAMION,
            True,
            "Modificar Contactos de Camion",
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.MODIFICAR_ALIAS, m.CAMION, True, "Modificar Alias de Camion"
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.CAMION))
    permisos.append(permiso_seeds(db, a.REPORTE, m.CAMION, True, "Reporte de Camion"))
    user.permisos.extend(permisos)
    db.commit()


def permiso_camion_semi_neto_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.CAMION_SEMI_NETO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.CAMION_SEMI_NETO))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.CAMION_SEMI_NETO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CAMION_SEMI_NETO))
    permisos.append(permiso_seeds(db, a.VER, m.CAMION_SEMI_NETO))
    user.permisos.extend(permisos)
    db.commit()


def permiso_chofer_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.CHOFER))
    permisos.append(permiso_seeds(db, a.CREAR, m.CHOFER))
    permisos.append(permiso_seeds(db, a.EDITAR, m.CHOFER))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.CHOFER))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CHOFER))
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.CHOFER,
            True,
            "Modificar Contactos de Chofer",
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.MODIFICAR_ALIAS, m.CHOFER, True, "Modificar Alias de Chofer"
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.CHOFER))
    permisos.append(permiso_seeds(db, a.REPORTE, m.CHOFER, True, "Reporte de Chofer"))
    user.permisos.extend(permisos)
    db.commit()


def permiso_propietario_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.PROPIETARIO))
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


def permiso_semirremolque_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.SEMIRREMOLQUE))
    permisos.append(permiso_seeds(db, a.CREAR, m.SEMIRREMOLQUE))
    permisos.append(permiso_seeds(db, a.EDITAR, m.SEMIRREMOLQUE))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.SEMIRREMOLQUE))
    permisos.append(permiso_seeds(db, a.LISTAR, m.SEMIRREMOLQUE))
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.SEMIRREMOLQUE,
            True,
            "Modificar Contactos de Semirremolque",
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_ALIAS,
            m.SEMIRREMOLQUE,
            True,
            "Modificar Alias de Semirremolque",
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.SEMIRREMOLQUE))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.SEMIRREMOLQUE, True, "Reporte de Semirremolque")
    )
    user.permisos.extend(permisos)
    db.commit()
