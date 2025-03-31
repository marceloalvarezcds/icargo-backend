from fastapi import APIRouter

from app.endpoints import (
    banco,
    caja,
    camion,
    camion_semi_neto,
    cargo,
    centro_operativo,
    centro_operativo_clasificacion,
    chofer,
    ciudad,
    color,
    composicion_juridica,
    contacto,
    contraparte,
    ente_emisor_automotor,
    ente_emisor_transporte,
    estado_cuenta,
    factura,
    flete,
    flete_anticipo,
    gestor_carga,
    instrumento,
    instrumento_via,
    insumo,
    insumo_punto_venta,
    insumo_punto_venta_precio,
    liquidacion,
    localidad,
    login,
    marca_camion,
    marca_semi,
    moneda,
    moneda_cotizacion,
    movimiento,
    orden_carga,
    orden_carga_anticipo_retirado,
    orden_carga_anticipo_saldo,
    orden_carga_complemento,
    orden_carga_descuento,
    orden_carga_evaluacion,
    orden_carga_remision_destino,
    orden_carga_remision_origen,
    pais,
    permiso,
    producto,
    propietario,
    proveedor,
    punto_venta,
    remitente,
    rentabilidad,
    rol,
    semi,
    semi_clasificacion,
    tipo_anticipo,
    tipo_camion,
    tipo_carga,
    tipo_comprobante,
    tipo_concepto_complemento,
    tipo_concepto_descuento,
    tipo_contraparte,
    tipo_cuenta,
    tipo_documento,
    tipo_incidente,
    tipo_instrumento,
    tipo_insumo,
    tipo_iva,
    tipo_movimiento,
    tipo_persona,
    tipo_registro,
    tipo_semi,
    unidad,
    user,
    combinacion,
    contribuyente,
    texto_legal
)

api = APIRouter()

api.include_router(banco.api, prefix="/banco", tags=["banco"])
api.include_router(caja.api, prefix="/caja", tags=["caja"])
api.include_router(camion.api, prefix="/camion", tags=["camion"])
api.include_router(
    camion_semi_neto.api, prefix="/camion_semi_neto", tags=["camion_semi_neto"]
)
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
api.include_router(combinacion.api, prefix="/combinacion", tags=["combinacion"])
api.include_router(
    composicion_juridica.api,
    prefix="/composicion_juridica",
    tags=["composicion_juridica"],
)
api.include_router(contacto.api, prefix="/contacto", tags=["contacto"])
api.include_router(contraparte.api, prefix="/contraparte", tags=["contraparte"])
api.include_router(
    ente_emisor_automotor.api,
    prefix="/ente_emisor_automotor",
    tags=["ente_emisor_automotor"],
)
api.include_router(
    ente_emisor_transporte.api,
    prefix="/ente_emisor_transporte",
    tags=["ente_emisor_transporte"],
)
api.include_router(estado_cuenta.api, prefix="/estado_cuenta", tags=["estado_cuenta"])
api.include_router(factura.api, prefix="/factura", tags=["factura"])
api.include_router(flete.api, prefix="/flete", tags=["flete"])
api.include_router(
    flete_anticipo.api, prefix="/flete_anticipo", tags=["flete_anticipo"]
)
api.include_router(gestor_carga.api, prefix="/gestor_carga", tags=["gestor_carga"])
api.include_router(instrumento.api, prefix="/instrumento", tags=["instrumento"])
api.include_router(
    instrumento_via.api, prefix="/instrumento_via", tags=["instrumento_via"]
)
api.include_router(insumo.api, prefix="/insumo", tags=["insumo"])
api.include_router(
    insumo_punto_venta.api, prefix="/insumo_punto_venta", tags=["insumo_punto_venta"]
)
api.include_router(
    insumo_punto_venta_precio.api,
    prefix="/insumo_punto_venta_precio",
    tags=["insumo_punto_venta_precio"],
)
api.include_router(liquidacion.api, prefix="/liquidacion", tags=["liquidacion"])
api.include_router(localidad.api, prefix="/localidad", tags=["localidad"])
api.include_router(login.api, prefix="/login", tags=["login"])
api.include_router(marca_camion.api, prefix="/marca_camion", tags=["marca_camion"])
api.include_router(marca_semi.api, prefix="/marca_semi", tags=["marca_semi"])
api.include_router(moneda.api, prefix="/moneda", tags=["moneda"])
api.include_router(moneda_cotizacion.api, prefix="/moneda_cotizacion", tags=["moneda_cotizacion"])
api.include_router(movimiento.api, prefix="/movimiento", tags=["movimiento"])
api.include_router(orden_carga.api, prefix="/orden_carga", tags=["orden_carga"])
api.include_router(
    orden_carga_anticipo_retirado.api,
    prefix="/orden_carga_anticipo_retirado",
    tags=["orden_carga_anticipo_retirado"],
)
api.include_router(
    orden_carga_anticipo_saldo.api,
    prefix="/orden_carga_anticipo_saldo",
    tags=["orden_carga_anticipo_saldo"],
)
api.include_router(
    orden_carga_complemento.api,
    prefix="/orden_carga_complemento",
    tags=["orden_carga_complemento"],
)
api.include_router(
    orden_carga_descuento.api,
    prefix="/orden_carga_descuento",
    tags=["orden_carga_descuento"],
)
api.include_router(
    orden_carga_evaluacion.api,
    prefix="/orden_carga_evaluacion",
    tags=["orden_carga_evaluacion"],
)
api.include_router(
    orden_carga_remision_destino.api,
    prefix="/orden_carga_remision_destino",
    tags=["orden_carga_remision_destino"],
)
api.include_router(
    orden_carga_remision_origen.api,
    prefix="/orden_carga_remision_origen",
    tags=["orden_carga_remision_origen"],
)
api.include_router(pais.api, prefix="/pais", tags=["pais"])
api.include_router(permiso.api, prefix="/permiso", tags=["permiso"])
api.include_router(producto.api, prefix="/producto", tags=["producto"])
api.include_router(propietario.api, prefix="/propietario", tags=["propietario"])
api.include_router(proveedor.api, prefix="/proveedor", tags=["proveedor"])
api.include_router(punto_venta.api, prefix="/punto_venta", tags=["punto_venta"])
api.include_router(remitente.api, prefix="/remitente", tags=["remitente"])
api.include_router(rentabilidad.api, prefix="/rentabilidad", tags=["rentabilidad"])
api.include_router(rol.api, prefix="/rol", tags=["rol"])
api.include_router(
    semi_clasificacion.api, prefix="/semi_clasificacion", tags=["semi_clasificacion"]
)
api.include_router(semi.api, prefix="/semi", tags=["semi"])
api.include_router(tipo_anticipo.api, prefix="/tipo_anticipo", tags=["tipo_anticipo"])
api.include_router(tipo_camion.api, prefix="/tipo_camion", tags=["tipo_camion"])
api.include_router(tipo_carga.api, prefix="/tipo_carga", tags=["tipo_carga"])
api.include_router(
    tipo_comprobante.api, prefix="/tipo_comprobante", tags=["tipo_comprobante"]
)
api.include_router(tipo_cuenta.api, prefix="/tipo_cuenta", tags=["tipo_cuenta"])
api.include_router(
    tipo_concepto_complemento.api,
    prefix="/tipo_concepto_complemento",
    tags=["tipo_concepto_complemento"],
)
api.include_router(
    tipo_concepto_descuento.api,
    prefix="/tipo_concepto_descuento",
    tags=["tipo_concepto_descuento"],
)
api.include_router(
    tipo_contraparte.api, prefix="/tipo_contraparte", tags=["tipo_contraparte"]
)
api.include_router(
    tipo_documento.api, prefix="/tipo_documento", tags=["tipo_documento"]
)

api.include_router(tipo_incidente.api, prefix="/tipo_incidente", tags=["tipo_incidente"])

api.include_router(
    tipo_instrumento.api, prefix="/tipo_instrumento", tags=["tipo_instrumento"]
)
api.include_router(tipo_insumo.api, prefix="/tipo_insumo", tags=["tipo_insumo"])
api.include_router(tipo_iva.api, prefix="/tipo_iva", tags=["tipo_iva"])
api.include_router(
    tipo_movimiento.api, prefix="/tipo_movimiento", tags=["tipo_movimiento"]
)
api.include_router(tipo_persona.api, prefix="/tipo_persona", tags=["tipo_persona"])
api.include_router(tipo_registro.api, prefix="/tipo_registro", tags=["tipo_registro"])
api.include_router(tipo_semi.api, prefix="/tipo_semi", tags=["tipo_semi"])
api.include_router(unidad.api, prefix="/unidad", tags=["unidad"])
api.include_router(user.api, prefix="/user", tags=["user"])
api.include_router(contribuyente.api, prefix="/contribuyente", tags=["contribuyente"])
api.include_router( texto_legal.api, prefix="/texto_legal", tags=["texto_legal"] )

@api.get("/alive")
def alive() -> dict:
    return {"alive": True}
