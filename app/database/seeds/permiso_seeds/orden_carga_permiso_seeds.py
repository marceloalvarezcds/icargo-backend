from sqlalchemy.orm.session import Session  # type: ignore

from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m
from app.models import User

from .permiso_seeds import permiso_seeds


def orden_carga_admin_permiso_seeds(db: Session, user: User):
    permiso_generico_seeds(db, user)
    permisos = []

    permisos.append(permiso_seeds(db, a.VER, m.INSUMO))
    permisos.append(permiso_seeds(db, a.VER, m.INSUMO_PUNTO_VENTA))
    permisos.append(permiso_seeds(db, a.VER, m.INSUMO_PUNTO_VENTA_PRECIO))

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.ORDEN_CARGA, True, "Reporte de Orden de Carga")
    )

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_ANTICIPO_RETIRADO))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_ANTICIPO_RETIRADO))

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_ANTICIPO_SALDO))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_ANTICIPO_SALDO))

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_COMPLEMENTO))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_COMPLEMENTO))

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_DESCUENTO))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_DESCUENTO))

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_REMISION_DESTINO))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_DESTINO))

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_REMISION_ORIGEN))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_ORIGEN))

    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_REMISION_RESULTADO))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_RESULTADO))

    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_RESULTADO_GESTOR))

    user.permisos.extend(permisos)
    db.commit()


def orden_carga_permiso_seeds(db: Session, user: User):
    permiso_generico_seeds(db, user)
    permiso_orden_carga_seeds(db, user)
    permiso_orden_carga_anticipo_retirado_seeds(db, user)
    permiso_orden_carga_anticipo_saldo_seeds(db, user)
    permiso_orden_carga_complemento_seeds(db, user)
    permiso_orden_carga_descuento_seeds(db, user)
    permiso_orden_carga_remision_destino_seeds(db, user)
    permiso_orden_carga_remision_origen_seeds(db, user)
    permiso_orden_carga_remision_resultado_seeds(db, user)


def orden_carga_gestor_permiso_seeds(db: Session, user: User):
    orden_carga_permiso_seeds(db, user)
    permiso_orden_carga_remision_resultado_gestor_seeds(db, user)


def permiso_generico_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.CAMION))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CAMION_SEMI_NETO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.CENTRO_OPERATIVO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.FLETE))
    permisos.append(permiso_seeds(db, a.LISTAR, m.INSUMO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.INSUMO_PUNTO_VENTA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.MONEDA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.PRODUCTO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.REMITENTE))
    permisos.append(permiso_seeds(db, a.LISTAR, m.SEMIRREMOLQUE))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_ANTICIPO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_CARGA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_COMPROBANTE))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_CONCEPTO_COMPLEMENTO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_CONCEPTO_DESCUENTO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.TIPO_INSUMO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.UNIDAD))
    permisos.append(permiso_seeds(db, a.VER, m.CAMION_SEMI_NETO))
    permisos.append(permiso_seeds(db, a.VER, m.CONTACTO))
    permisos.append(permiso_seeds(db, a.VER, m.INSUMO_PUNTO_VENTA_PRECIO))
    user.permisos.extend(permisos)
    db.commit()


def permiso_orden_carga_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CAMBIAR_ESTADO, m.ORDEN_CARGA))
    permisos.append(permiso_seeds(db, a.CONCILIAR, m.ORDEN_CARGA))
    permisos.append(permiso_seeds(db, a.CREAR, m.ORDEN_CARGA))
    permisos.append(permiso_seeds(db, a.EDITAR, m.ORDEN_CARGA))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.ORDEN_CARGA))
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA))
    permisos.append(
        permiso_seeds(db, a.REPORTE, m.ORDEN_CARGA, True, "Reporte de Orden de Carga")
    )
    user.permisos.extend(permisos)
    db.commit()


def permiso_orden_carga_anticipo_retirado_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.ORDEN_CARGA_ANTICIPO_RETIRADO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.ORDEN_CARGA_ANTICIPO_RETIRADO))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.ORDEN_CARGA_ANTICIPO_RETIRADO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_ANTICIPO_RETIRADO))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_ANTICIPO_RETIRADO))
    user.permisos.extend(permisos)
    db.commit()


def permiso_orden_carga_anticipo_saldo_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.ORDEN_CARGA_ANTICIPO_SALDO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.ORDEN_CARGA_ANTICIPO_SALDO))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.ORDEN_CARGA_ANTICIPO_SALDO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_ANTICIPO_SALDO))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_ANTICIPO_SALDO))
    user.permisos.extend(permisos)
    db.commit()


def permiso_orden_carga_complemento_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.ORDEN_CARGA_COMPLEMENTO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.ORDEN_CARGA_COMPLEMENTO))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.ORDEN_CARGA_COMPLEMENTO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_COMPLEMENTO))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_COMPLEMENTO))
    user.permisos.extend(permisos)
    db.commit()


def permiso_orden_carga_descuento_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.ORDEN_CARGA_DESCUENTO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.ORDEN_CARGA_DESCUENTO))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.ORDEN_CARGA_DESCUENTO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_DESCUENTO))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_DESCUENTO))
    user.permisos.extend(permisos)
    db.commit()


def permiso_orden_carga_remision_destino_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.ORDEN_CARGA_REMISION_DESTINO))
    permisos.append(permiso_seeds(db, a.EDITAR, m.ORDEN_CARGA_REMISION_DESTINO))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.ORDEN_CARGA_REMISION_DESTINO))
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_REMISION_DESTINO))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_DESTINO))
    user.permisos.extend(permisos)
    db.commit()


def permiso_orden_carga_remision_origen_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.CREAR, m.ORDEN_CARGA_REMISION_ORIGEN))
    permisos.append(permiso_seeds(db, a.EDITAR, m.ORDEN_CARGA_REMISION_ORIGEN))
    permisos.append(permiso_seeds(db, a.ELIMINAR, m.ORDEN_CARGA_REMISION_ORIGEN))
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_REMISION_ORIGEN))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_ORIGEN))
    user.permisos.extend(permisos)
    db.commit()


def permiso_orden_carga_remision_resultado_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.LISTAR, m.ORDEN_CARGA_REMISION_RESULTADO))
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_RESULTADO))
    user.permisos.extend(permisos)
    db.commit()


def permiso_orden_carga_remision_resultado_gestor_seeds(db: Session, user: User):
    permisos = []
    permisos.append(permiso_seeds(db, a.VER, m.ORDEN_CARGA_REMISION_RESULTADO_GESTOR))
    user.permisos.extend(permisos)
    db.commit()
