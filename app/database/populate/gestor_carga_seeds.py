from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import GestorCarga
from app.repositories import (
    get_ciudad_by_nombre_and_localidad_id,
    get_composicion_juridica_by_nombre,
    get_localidad_by_nombre_and_pais_id,
    get_moneda_by_simbolo,
    get_pais_by_nombre_corto,
    get_tipo_documento_by_descripcion,
)

from .centro_operativo_seeds import centro_operativo_seeds


def gestor_carga_seeds(db: Session):
    try:
        composicion_juridica = get_composicion_juridica_by_nombre(
            db, "Sociedad Anónima"
        )
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

        gestor_carga = GestorCarga(
            nombre="Transred",
            nombre_corto="TRD",
            tipo_documento_id=tipo_documento.id if tipo_documento else None,
            numero_documento="800100100",
            digito_verificador="1",
            composicion_juridica_id=composicion_juridica.id
            if composicion_juridica
            else None,
            moneda_id=moneda.id if moneda else None,
            logo=None,
            pagina_web="www.transred.com",
            info_complementaria="",
            latitud=-25.658948139894708,
            longitud=-54.717514329980474,
            direccion="Asunción, Paraguay",
            ciudad_id=asuncion.id if asuncion else None,
        )
        db.add(gestor_carga)
        db.commit()

        centro_operativo_seeds(db, gestor_carga)
    except IntegrityError:
        db.rollback()
