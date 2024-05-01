from typing import List

from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums import PermisoModuloEnum as u
from app.models import Permiso

from .permiso_seeds import permiso_seeds


def flota_admin_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.extend(permiso_generico_seeds(db))

    permisos.append(permiso_seeds(db, a.LISTAR, m.CAMION, u.FLOTA))
    permisos.append(permiso_seeds(db, a.VER, m.CAMION, u.FLOTA))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.CAMION, u.FLOTA, "Reporte de Camion")
    )

    permisos.append(permiso_seeds(db, a.LISTAR, m.CAMION_SEMI_NETO, u.FLOTA))
    permisos.append(permiso_seeds(db, a.VER, m.CAMION_SEMI_NETO, u.FLOTA))

    permisos.append(permiso_seeds(db, a.LISTAR, m.CHOFER, u.FLOTA))
    permisos.append(permiso_seeds(db, a.VER, m.CHOFER, u.FLOTA))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.CHOFER, u.FLOTA, "Reporte de Chofer")
    )

    permisos.append(permiso_seeds(db, a.LISTAR, m.PROPIETARIO, u.FLOTA))
    permisos.append(permiso_seeds(db, a.VER, m.PROPIETARIO, u.FLOTA))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.PROPIETARIO, u.FLOTA, "Reporte de Propietario")
    )

    permisos.append(permiso_seeds(db, a.LISTAR, m.SEMIRREMOLQUE, u.FLOTA))
    permisos.append(permiso_seeds(db, a.VER, m.SEMIRREMOLQUE, u.FLOTA))
    permisos.append(
        permiso_seeds(
            db, a.REPORTE, m.SEMIRREMOLQUE, u.FLOTA, "Reporte de Semirremolque"
        )
    )
    return permisos


def flota_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.extend(permiso_generico_seeds(db))
    permisos.extend(permiso_camion_seeds(db))
    permisos.extend(permiso_camion_semi_neto_seeds(db))
    permisos.extend(permiso_chofer_seeds(db))
    permisos.extend(permiso_propietario_seeds(db))
    permisos.extend(permiso_semirremolque_seeds(db))
    return permisos


def permiso_generico_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.CARGO, u.BIBLIOTECA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CIUDAD, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.LISTAR, m.COLOR, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.VER, m.CONTACTO, u.FLOTA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.CONTACTO, u.FLOTA))
    permisos.append(
        permiso_seeds(
            db,
            a.LISTAR,
            m.ENTE_EMISOR_AUTOMOTOR,
            u.PARAMETROS,
            "Listar Ente Emisor del Automotor",
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.LISTAR,
            m.ENTE_EMISOR_TRANSPORTE,
            u.PARAMETROS,
            "Listar Ente Emisor del Transporte",
        )
    )
    permisos.append(permiso_seeds(db, a.LISTAR, m.LOCALIDAD, u.PARAMETROS))
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.MARCA_CAMION, u.PARAMETROS, "Listar Marca de Camión"
        )
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.MARCA_SEMI, u.PARAMETROS, "Listar Marca de Semi")
    )
    permisos.append(permiso_seeds(db, a.LISTAR, m.PAIS, u.PARAMETROS, "Listar País"))
    permisos.append(
        permiso_seeds(
            db,
            a.LISTAR,
            m.SEMI_CLASIFICACION,
            u.PARAMETROS,
            "Listar Clasificación Semi-remolque",
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.TIPO_CAMION, u.PARAMETROS, "Listar Tipo de Camion"
        )
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.TIPO_CARGA, u.PARAMETROS, "Listar Tipo de Carga")
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.TIPO_PERSONA, u.PARAMETROS, "Listar Tipo de Persona"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.TIPO_REGISTRO, u.PARAMETROS, "Listar Tipo de Registro"
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.LISTAR, m.TIPO_SEMI, u.PARAMETROS, "Listar Tipo de Semi-Remolque"
        )
    )
    permisos.append(permiso_seeds(db, a.LISTAR, m.USER, u.USUARIOS))
    permisos.append(permiso_seeds(db, a.VER, m.USER, u.USUARIOS))
    return permisos


def permiso_camion_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.CAMION, u.FLOTA))
    permisos.append(permiso_seeds(db, a.CREAR, m.CAMION, u.FLOTA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.CAMION, u.FLOTA))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.CAMION, u.FLOTA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CAMION, u.FLOTA))
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.CAMION,
            u.FLOTA,
            "Modificar Contactos de Camion",
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.MODIFICAR_ALIAS, m.CAMION, u.FLOTA, "Modificar Alias de Camion"
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.CAMION, u.FLOTA))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.CAMION, u.FLOTA, "Reporte de Camion")
    )
    return permisos


def permiso_camion_semi_neto_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.CAMION_SEMI_NETO, u.FLOTA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.CAMION_SEMI_NETO, u.FLOTA))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.CAMION_SEMI_NETO, u.FLOTA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CAMION_SEMI_NETO, u.FLOTA))
    permisos.append(permiso_seeds(db, a.VER, m.CAMION_SEMI_NETO, u.FLOTA))
    return permisos


def permiso_chofer_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.CHOFER, u.FLOTA))
    permisos.append(permiso_seeds(db, a.CREAR, m.CHOFER, u.FLOTA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.CHOFER, u.FLOTA))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.CHOFER, u.FLOTA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CHOFER, u.FLOTA))
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.CHOFER,
            u.FLOTA,
            "Modificar Contactos de Chofer",
        )
    )
    permisos.append(
        permiso_seeds(
            db, a.MODIFICAR_ALIAS, m.CHOFER, u.FLOTA, "Modificar Alias de Chofer"
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.CHOFER, u.FLOTA))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.CHOFER, u.FLOTA, "Reporte de Chofer")
    )
    return permisos


def permiso_propietario_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.PROPIETARIO, u.FLOTA))
    permisos.append(permiso_seeds(db, a.CREAR, m.PROPIETARIO, u.FLOTA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.PROPIETARIO, u.FLOTA))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.PROPIETARIO, u.FLOTA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.PROPIETARIO, u.FLOTA))
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.PROPIETARIO,
            u.FLOTA,
            "Modificar Contactos de Propietario",
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_ALIAS,
            m.PROPIETARIO,
            u.FLOTA,
            "Modificar Alias de Propietario",
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.PROPIETARIO, u.FLOTA))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.PROPIETARIO, u.FLOTA, "Reporte de Propietario")
    )
    return permisos


def permiso_semirremolque_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.SEMIRREMOLQUE, u.FLOTA))
    permisos.append(permiso_seeds(db, a.CREAR, m.SEMIRREMOLQUE, u.FLOTA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.SEMIRREMOLQUE, u.FLOTA))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.SEMIRREMOLQUE, u.FLOTA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.SEMIRREMOLQUE, u.FLOTA))
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_CONTACTOS,
            m.SEMIRREMOLQUE,
            u.FLOTA,
            "Modificar Contactos de Semirremolque",
        )
    )
    permisos.append(
        permiso_seeds(
            db,
            a.MODIFICAR_ALIAS,
            m.SEMIRREMOLQUE,
            u.FLOTA,
            "Modificar Alias de Semirremolque",
        )
    )
    permisos.append(permiso_seeds(db, a.VER, m.SEMIRREMOLQUE, u.FLOTA))
    permisos.append(
        permiso_seeds(
            db, a.REPORTE, m.SEMIRREMOLQUE, u.FLOTA, "Reporte de Semirremolque"
        )
    )
    return permisos


def permiso_combinacion_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.COMBINACION, u.FLOTA))
    permisos.append(permiso_seeds(db, a.VER, m.COMBINACION, u.FLOTA))
    permisos.append(permiso_seeds(db, a.CREAR, m.COMBINACION, u.FLOTA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.COMBINACION, u.FLOTA))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.COMBINACION, u.FLOTA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.COMBINACION, u.FLOTA))
    permisos.append(permiso_seeds(db, a.REPORTE, m.COMBINACION, u.FLOTA, "Reporte de Combinacion")
    )
    return permisos