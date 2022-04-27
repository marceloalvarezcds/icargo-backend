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


def gestor_carga_seeds(db: Session):
    composicion_juridica = get_composicion_juridica_by_nombre(db, "Sociedad Anónima")
    paraguay = get_pais_by_nombre_corto(db, "PY")
    central = (
        get_localidad_by_nombre_and_pais_id(db, "Central", paraguay.id)
        if paraguay
        else None
    )
    ciudad = (
        get_ciudad_by_nombre_and_localidad_id(db, "Villa Elisa", central.id)
        if central
        else None
    )
    moneda = get_moneda_by_simbolo(db, "PYG")
    tipo_documento = get_tipo_documento_by_descripcion(db, "RUC")
    if tipo_documento:
        numero_documento = "80015858"
        gestor_carga = get_gestor_carga_by(db, tipo_documento.id, numero_documento)

        if gestor_carga is None:
            gestor_carga = GestorCarga(
                nombre="TRANSRED SA (TRANSPORTES REPRESENTACIONES DISTRIBUCIONES)",
                nombre_corto="TRD LOGISTICA",
                tipo_documento_id=tipo_documento.id,
                numero_documento=numero_documento,
                digito_verificador="0",
                composicion_juridica_id=composicion_juridica.id
                if composicion_juridica
                else None,
                moneda_id=moneda.id if moneda else None,
                logo=None,
                telefono="(021) 237 7176",
                email="transred@transred.com.py",
                pagina_web="https://www.transred.com.py/",
                info_complementaria="",
                latitud=-25.374083,
                longitud=-57.605054,
                direccion="Avda. Defensores del Chaco 3435 c/ Sta. Teresa – Villa Elisa – Central - PY",  # noqa: B950
                ciudad_id=ciudad.id if ciudad else None,
            )
            db.add(gestor_carga)
            db.commit()
