from typing import List

from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.enums import PermisoModuloEnum as u
from app.models import Permiso

from .permiso_seeds import permiso_seeds


def orden_carga_admin_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.extend(permiso_generico_seeds(db))

    permisos.append(permiso_seeds(db, a.VER, m.INSUMO, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.VER, m.INSUMO_PUNTO_VENTA, u.BIBLIOTECA))
    permisos.append(permiso_seeds(db, a.VER, m.INSUMO_PUNTO_VENTA_PRECIO, u.BIBLIOTECA))
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.INSUMO_PUNTO_VENTA_PRECIO, u.BIBLIOTECA)
    )

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA, u.OC))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.ORDEN_CARGA, u.OC, "Reporte de Orden de Carga")
    )

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_ANTICIPO_RETIRADO, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_ANTICIPO_RETIRADO, u.OC))

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_ANTICIPO_SALDO, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_ANTICIPO_SALDO, u.OC))

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_COMPLEMENTO, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_COMPLEMENTO, u.OC))

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_DESCUENTO, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_DESCUENTO, u.OC))

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_REMISION_DESTINO, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_DESTINO, u.OC))

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_REMISION_ORIGEN, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_ORIGEN, u.OC))

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_REMISION_RESULTADO, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_RESULTADO, u.OC))

    permisos.append(
        permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_RESULTADO_GESTOR, u.OC)
    )
    return permisos


def orden_carga_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.extend(permiso_generico_seeds(db))
    permisos.extend(permiso_orden_carga_seeds(db))
    permisos.extend(permiso_orden_carga_anticipo_retirado_seeds(db))
    permisos.extend(permiso_orden_carga_anticipo_saldo_seeds(db))
    permisos.extend(permiso_orden_carga_complemento_seeds(db))
    permisos.extend(permiso_orden_carga_descuento_seeds(db))
    permisos.extend(permiso_orden_carga_remision_destino_seeds(db))
    permisos.extend(permiso_orden_carga_remision_origen_seeds(db))
    permisos.extend(permiso_orden_carga_remision_resultado_seeds(db))
    return permisos


def orden_carga_gestor_permiso_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.extend(orden_carga_permiso_seeds(db))
    permisos.extend(permiso_orden_carga_remision_resultado_gestor_seeds(db))
    return permisos


def permiso_generico_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.CAMION, u.FLOTA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CAMION_SEMI_NETO, u.FLOTA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CENTRO_OPERATIVO, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE, u.FLETE))
    permisos.append(permiso_seeds(db, a.LISTAR, m.INSUMO, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.LISTAR, m.INSUMO_PUNTO_VENTA, u.BIBLIOTECA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.MONEDA, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.LISTAR, m.PRODUCTO, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.LISTAR, m.REMITENTE, u.ENTIDADES))
    permisos.append(permiso_seeds(db, a.LISTAR, m.SEMIRREMOLQUE, u.FLOTA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_ANTICIPO, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_CARGA, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_COMPROBANTE, u.PARAMETROS))
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.TIPO_CONCEPTO_COMPLEMENTO, u.PARAMETROS)
    )
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.TIPO_CONCEPTO_DESCUENTO, u.PARAMETROS)
    )
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_INSUMO, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.LISTAR, m.UNIDAD, u.PARAMETROS))
    permisos.append(permiso_seeds(db, a.VER, m.CAMION_SEMI_NETO, u.FLOTA))
    permisos.append(permiso_seeds(db, a.VER, m.CONTACTO, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.INSUMO_PUNTO_VENTA_PRECIO, u.BIBLIOTECA))
    permisos.append(
        permiso_seeds(db, a.LISTAR, m.INSUMO_PUNTO_VENTA_PRECIO, u.BIBLIOTECA)
    )
    return permisos


def permiso_orden_carga_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.ORDEN_CARGA, u.OC))
    permisos.append(permiso_seeds(db, a.CONCILIAR, m.ORDEN_CARGA, u.OC))
    permisos.append(permiso_seeds(db, a.CREAR, m.ORDEN_CARGA, u.OC))
    permisos.append(permiso_seeds(db, a.EDITAR, m.ORDEN_CARGA, u.OC))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.ORDEN_CARGA, u.OC))
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA, u.OC))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.ORDEN_CARGA, u.OC, "Reporte de Orden de Carga")
    )
    return permisos


def permiso_orden_carga_anticipo_retirado_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.ORDEN_CARGA_ANTICIPO_RETIRADO, u.OC))
    permisos.append(permiso_seeds(db, a.EDITAR, m.ORDEN_CARGA_ANTICIPO_RETIRADO, u.OC))
    permisos.append(
        permiso_seeds(db, a.ELIMINAR, m.ORDEN_CARGA_ANTICIPO_RETIRADO, u.OC)
    )
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_ANTICIPO_RETIRADO, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_ANTICIPO_RETIRADO, u.OC))
    return permisos


def permiso_orden_carga_anticipo_saldo_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.ORDEN_CARGA_ANTICIPO_SALDO, u.OC))
    permisos.append(permiso_seeds(db, a.EDITAR, m.ORDEN_CARGA_ANTICIPO_SALDO, u.OC))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.ORDEN_CARGA_ANTICIPO_SALDO, u.OC))
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_ANTICIPO_SALDO, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_ANTICIPO_SALDO, u.OC))
    return permisos


def permiso_orden_carga_complemento_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.ORDEN_CARGA_COMPLEMENTO, u.OC))
    permisos.append(permiso_seeds(db, a.EDITAR, m.ORDEN_CARGA_COMPLEMENTO, u.OC))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.ORDEN_CARGA_COMPLEMENTO, u.OC))
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_COMPLEMENTO, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_COMPLEMENTO, u.OC))
    return permisos


def permiso_orden_carga_descuento_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.ORDEN_CARGA_DESCUENTO, u.OC))
    permisos.append(permiso_seeds(db, a.EDITAR, m.ORDEN_CARGA_DESCUENTO, u.OC))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.ORDEN_CARGA_DESCUENTO, u.OC))
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_DESCUENTO, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_DESCUENTO, u.OC))
    return permisos


def permiso_orden_carga_remision_destino_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.ORDEN_CARGA_REMISION_DESTINO, u.OC))
    permisos.append(permiso_seeds(db, a.EDITAR, m.ORDEN_CARGA_REMISION_DESTINO, u.OC))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.ORDEN_CARGA_REMISION_DESTINO, u.OC))
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_REMISION_DESTINO, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_DESTINO, u.OC))
    return permisos


def permiso_orden_carga_remision_origen_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.ORDEN_CARGA_REMISION_ORIGEN, u.OC))
    permisos.append(permiso_seeds(db, a.EDITAR, m.ORDEN_CARGA_REMISION_ORIGEN, u.OC))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.ORDEN_CARGA_REMISION_ORIGEN, u.OC))
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_REMISION_ORIGEN, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_ORIGEN, u.OC))
    return permisos


def permiso_orden_carga_remision_resultado_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_REMISION_RESULTADO, u.OC))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_RESULTADO, u.OC))
    return permisos


def permiso_orden_carga_remision_resultado_gestor_seeds(db: Session) -> List[Permiso]:
    permisos = []
    permisos.append(
        permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_RESULTADO_GESTOR, u.OC)
    )
    return permisos
