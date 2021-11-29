from fastapi import APIRouter

from app.endpoints import (
    cargo,
    centro_operativo,
    centro_operativo_clasificacion,
    chofer,
    ciudad,
    color,
    composicion_juridica,
    contacto,
    ente_emisor_automotor,
    gestor_carga,
    localidad,
    login,
    moneda,
    pais,
    permiso,
    propietario,
    proveedor,
    punto_venta,
    remitente,
    tipo_documento,
    tipo_persona,
    tipo_registro,
    user,
)

api = APIRouter()

api.include_router(cargo.api, prefix="/cargo", tags=["cargo"])
api.include_router(
    centro_operativo_clasificacion.api,
    prefix="/centro_operativo_clasificacion",
    tags=["centro_operativo_clasificacion"],
)
api.include_router(
    centro_operativo.api, prefix="/centro_operativo", tags=["centro_operativo"]
)
api.include_router(chofer.api, prefix="/chofer", tags=["chofer"])
api.include_router(ciudad.api, prefix="/ciudad", tags=["ciudad"])
api.include_router(color.api, prefix="/color", tags=["color"])
api.include_router(
    composicion_juridica.api,
    prefix="/composicion_juridica",
    tags=["composicion_juridica"],
)
api.include_router(contacto.api, prefix="/contacto", tags=["contacto"])
api.include_router(
    ente_emisor_automotor.api,
    prefix="/ente_emisor_automotor",
    tags=["ente_emisor_automotor"],
)
api.include_router(gestor_carga.api, prefix="/gestor_carga", tags=["gestor_carga"])
api.include_router(localidad.api, prefix="/localidad", tags=["localidad"])
api.include_router(login.api, prefix="/login", tags=["login"])
api.include_router(moneda.api, prefix="/moneda", tags=["moneda"])
api.include_router(pais.api, prefix="/pais", tags=["pais"])
api.include_router(permiso.api, prefix="/permiso", tags=["permiso"])
api.include_router(propietario.api, prefix="/propietario", tags=["propietario"])
api.include_router(proveedor.api, prefix="/proveedor", tags=["proveedor"])
api.include_router(punto_venta.api, prefix="/punto_venta", tags=["punto_venta"])
api.include_router(remitente.api, prefix="/remitente", tags=["remitente"])
api.include_router(
    tipo_documento.api, prefix="/tipo_documento", tags=["tipo_documento"]
)
api.include_router(tipo_persona.api, prefix="/tipo_persona", tags=["tipo_persona"])
api.include_router(tipo_registro.api, prefix="/tipo_registro", tags=["tipo_registro"])
api.include_router(user.api, prefix="/user", tags=["user"])


@api.get("/alive")
def alive() -> dict:
    return {"alive": True}
