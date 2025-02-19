from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import GestorCarga
from app.repositories import (
    get_ciudad_by_nombre_and_localidad_id,
    get_composicion_juridica_by_nombre,
    get_gestor_carga_by,
    get_localidad_by_nombre_and_pais_id,
    get_moneda_by_simbolo,
    get_pais_by_nombre_corto,
    get_tipo_documento_by_descripcion,
)

from .camion_semi_neto_seeds import camion_semi_producto_combination_seeds
from .centro_operativo_seeds import (
    cargill_centro_operativo_seeds,
    multiple_centro_operativo_seeds,
)
from .chofer_seeds import cargill_chofer_seeds, multiple_chofer_seeds
# from .propietario_seeds import cargill_propietario_seeds, multiple_propietario_seeds
# from .proveedor_seeds import cargill_proveedor_seeds, multiple_proveedor_seeds
# from .remitente_seeds import cargill_remitente_seeds, multiple_remitente_seeds
from .user_seeds import user_seeds


def gestor_carga_seeds(db: Session):
    composicion_juridica = get_composicion_juridica_by_nombre(db, "Sociedad Anónima")
    paraguay = get_pais_by_nombre_corto(db, "PY")
    central = (
        get_localidad_by_nombre_and_pais_id(db, "Central", paraguay.id)
        if paraguay
        else None
    )
    asuncion = (
        get_ciudad_by_nombre_and_localidad_id(db, "Asunción", central.id)
        if central
        else None
    )
    moneda = get_moneda_by_simbolo(db, "PYG")
    tipo_documento = get_tipo_documento_by_descripcion(db, "RUC")
    if tipo_documento:
        numero_documento1 = "80015858"
        numero_documento2 = "80020020"

        gestor_carga1 = get_gestor_carga_by(db, tipo_documento.id, numero_documento1)

        if gestor_carga1 is None:
            gestor_carga1 = GestorCarga(
                nombre="Transred",
                nombre_corto="TRD",
                tipo_documento_id=tipo_documento.id,
                numero_documento=numero_documento1,
                digito_verificador="0",
                composicion_juridica_id=composicion_juridica.id
                if composicion_juridica
                else None,
                moneda_id=moneda.id if moneda else None,
                logo=None,
                telefono="0961111111",
                email="contacto@transred.com",
                pagina_web="www.transred.com",
                info_complementaria="",
                latitud=-25.658948139894708,
                longitud=-54.717514329980474,
                direccion="Asunción, Paraguay",
                ciudad_id=asuncion.id if asuncion else None,
            )
            db.add(gestor_carga1)
            db.commit()

        gestor_carga2 = get_gestor_carga_by(db, tipo_documento.id, numero_documento2)

        if gestor_carga2 is None:
            gestor_carga2 = GestorCarga(
                nombre="Cargill",
                nombre_corto="Cargill",
                tipo_documento_id=tipo_documento.id,
                numero_documento=numero_documento2,
                digito_verificador="2",
                composicion_juridica_id=composicion_juridica.id
                if composicion_juridica
                else None,
                moneda_id=moneda.id if moneda else None,
                logo=None,
                telefono="0961222222",
                email="contacto@cargill.com",
                pagina_web="www.cargill.com",
                info_complementaria="",
                latitud=-25.483858539894708,
                longitud=-54.887314329980474,
                direccion="Minga Guazú, Paraguay",
                ciudad_id=asuncion.id if asuncion else None,
            )
            db.add(gestor_carga2)
            db.commit()

        user_seeds(db, "admin-transred", "Admin", "Transred", gestor_carga1)
        user_seeds(
            db, "admin-suplente-transred", "Admin Suplente", "Transred", gestor_carga1
        )
        user_seeds(db, "admin-cargill", "Admin", "Cargill", gestor_carga2)

        try:
            multiple_centro_operativo_seeds(db, gestor_carga1)
            cargill_centro_operativo_seeds(db, gestor_carga2)
            multiple_proveedor_seeds(db, gestor_carga1)
            cargill_proveedor_seeds(db, gestor_carga2)
            multiple_remitente_seeds(db, gestor_carga1)
            cargill_remitente_seeds(db, gestor_carga2)
            multiple_chofer_seeds(db, gestor_carga1)
            cargill_chofer_seeds(db, gestor_carga2)
            multiple_propietario_seeds(db, gestor_carga1)
            cargill_propietario_seeds(db, gestor_carga2)
            # camion y semi deben estar creados para la combinación
            camion_semi_producto_combination_seeds(db, gestor_carga1)
            camion_semi_producto_combination_seeds(db, gestor_carga2)
        except IntegrityError:
            db.rollback()
