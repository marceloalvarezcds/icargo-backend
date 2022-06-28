from enum import Enum
from typing import Dict


class PermisoAccionEnum(Enum):
    ACEPTAR = "aceptar"
    CAMBIAR_ESTADO = "cambiar_estado"
    CANCELAR = "cancelar"
    CONCILIAR = "conciliar"
    CREAR = "crear"
    EDITAR = "editar"
    ELIMINAR = "eliminar"
    LISTAR = "listar"
    MODIFICAR_CONTACTOS = "modificar_contactos"
    MODIFICAR_ALIAS = "modificar_alias"
    PASAR_A_REVISION = "pasar_a_revision"
    RECHAZAR = "rechazar"
    REPORTE = "reporte"
    VER = "ver"


class PermisoModeloEnum(Enum):
    BANCO = "banco"
    CAJA = "caja"
    CAMION = "camion"
    CAMION_SEMI_NETO = "camion_semi_neto"
    CARGO = "cargo"
    CENTRO_OPERATIVO_CLASIFICACION = "centro_operativo_clasificacion"
    CENTRO_OPERATIVO = "centro_operativo"
    CHOFER = "chofer"
    CIUDAD = "ciudad"
    COLOR = "color"
    COMPOSICION_JURIDICA = "composicion_juridica"
    CONTACTO = "contacto"
    ENTE_EMISOR_AUTOMOTOR = "ente_emisor_automotor"
    ENTE_EMISOR_TRANSPORTE = "ente_emisor_transporte"
    ESTADO_CUENTA = "estado_cuenta"
    FACTURA = "factura"
    FLETE = "flete"
    FLETE_ANTICIPO = "flete_anticipo"
    FLETE_COMPLEMENTO = "flete_complemento"
    FLETE_DESCUENTO = "flete_descuento"
    GESTOR_CARGA = "gestor_carga"
    INSTRUMENTO = "instrumento"
    INSTRUMENTO_VIA = "instrumento_via"
    INSUMO = "insumo"
    INSUMO_PUNTO_VENTA = "insumo_punto_venta"
    INSUMO_PUNTO_VENTA_PRECIO = "insumo_punto_venta_precio"
    LIQUIDACION = "liquidacion"
    LOCALIDAD = "localidad"
    MARCA_CAMION = "marca_camion"
    MARCA_SEMI = "marca_semi"
    MONEDA = "moneda"
    MOVIMIENTO = "movimiento"
    ORDEN_CARGA = "orden_carga"
    ORDEN_CARGA_ANTICIPO_RETIRADO = "orden_carga_anticipo_retirado"
    ORDEN_CARGA_ANTICIPO_SALDO = "orden_carga_anticipo_saldo"
    ORDEN_CARGA_COMPLEMENTO = "orden_carga_complemento"
    ORDEN_CARGA_DESCUENTO = "orden_carga_descuento"
    ORDEN_CARGA_REMISION_DESTINO = "orden_carga_remision_destino"
    ORDEN_CARGA_REMISION_ORIGEN = "orden_carga_remision_origen"
    ORDEN_CARGA_REMISION_RESULTADO = "orden_carga_remision_resultado"
    ORDEN_CARGA_REMISION_RESULTADO_GESTOR = "orden_carga_remision_resultado_gestor"
    PAIS = "pais"
    PERMISO = "permiso"
    PRODUCTO = "producto"
    PROPIETARIO = "propietario"
    PROVEEDOR = "proveedor"
    PUNTO_VENTA = "punto_venta"
    REMITENTE = "remitente"
    RENTABILIDAD = "rentabilidad"
    ROL = "rol"
    SEMIRREMOLQUE = "semirremolque"
    SEMI_CLASIFICACION = "semi_clasificacion"
    TIPO_ANTICIPO = "tipo_anticipo"
    TIPO_CAMION = "tipo_camion"
    TIPO_CARGA = "tipo_carga"
    TIPO_COMPROBANTE = "tipo_comprobante"
    TIPO_CONCEPTO_COMPLEMENTO = "tipo_concepto_complemento"
    TIPO_CONCEPTO_DESCUENTO = "tipo_concepto_descuento"
    TIPO_CONTRAPARTE = "tipo_contraparte"
    TIPO_CUENTA = "tipo_cuenta"
    TIPO_DOCUMENTO = "tipo_documento"
    TIPO_DOCUMENTO_RELACIONADO = "tipo_documento_relacionado"
    TIPO_INSTRUMENTO = "tipo_instrumento"
    TIPO_INSUMO = "tipo_insumo"
    TIPO_IVA = "tipo_iva"
    TIPO_MOVIMIENTO = "tipo_movimiento"
    TIPO_PERSONA = "tipo_persona"
    TIPO_REGISTRO = "tipo_registro"
    TIPO_SEMI = "tipo_semi"
    UNIDAD = "unidad"
    USER = "usuario"


class PermisoModuloEnum(Enum):
    ENTIDADES = "Entidades"
    FLOTA = "Flota"
    FLETE = "Flete"
    OC = "Orden de Carga"
    CAJA_BANCO = "Caja & Banco"
    ESTADO_CUENTA = "Estado de Cuenta"
    LISTADOS = "Listados"
    USUARIOS = "Usuarios"
    PARAMETROS = "Parámetros del Sistema"
    BIBLIOTECA = "Biblioteca de Usuario"


permisoModeloTitulo: Dict[str, str] = {
    "banco": "Banco",
    "caja": "Caja",
    "camion": "Camión",
    "camion_semi_neto": "Neto de la Combinacion Camión-Semi",
    "cargo": "Cargo",
    "centro_operativo_clasificacion": "Clasificación Centro Operativo",
    "centro_operativo": "Centro Operativo",
    "chofer": "Chofer",
    "ciudad": "Ciudad",
    "color": "Color",
    "composicion_juridica": "Composición Jurídica",
    "contacto": "Contacto",
    "ente_emisor_automotor": "Ente emisor de Registro Automotor",
    "ente_emisor_transporte": "Ente emisor de Registro de Transporte",
    "estado_cuenta": "Estado de Cuenta",
    "factura": "Factura",
    "flete": "Flete",
    "flete_anticipo": "Flete Anticipo",
    "flete_complemento": "Flete Complemento",
    "flete_descuento": "Flete descuento",
    "gestor_carga": "Gestor de Carga",
    "instrumento": "Instrumento",
    "instrumento_via": "Vía de Instrumento",
    "insumo": "Insumo",
    "insumo_punto_venta": "Insumo Punto de Venta",
    "insumo_punto_venta_precio": "Precio de Insumo en Punto de Venta",
    "liquidacion": "Liquidación",
    "localidad": "Localidad",
    "marca_camion": "Marca de Camión",
    "marca_semi": "Marca de Semi",
    "moneda": "Moneda",
    "movimiento": "Movimiento",
    "orden_carga": "Orden de Carga",
    "orden_carga_anticipo_retirado": "Anticipo Retirado",
    "orden_carga_anticipo_saldo": "Saldo de Anticipo",
    "orden_carga_complemento": "Complemento",
    "orden_carga_descuento": "Descuento",
    "orden_carga_remision_destino": "Remisión Destino",
    "orden_carga_remision_origen": "Remisión Origen",
    "orden_carga_remision_resultado": "Resultado de Remisión",
    "orden_carga_remision_resultado_gestor": "Resultado de Remisión de la Gestora",
    "pais": "País",
    "permiso": "Permiso",
    "producto": "Producto",
    "propietario": "Propietario",
    "proveedor": "Proveedor",
    "punto_venta": "Punto de Venta",
    "remitente": "Remitente",
    "rentabilidad": "Rentabilidad",
    "rol": "Rol",
    "semirremolque": "Semi",
    "semi_clasificacion": "Clasificación de Semi",
    "tipo_anticipo": "Tipo de Anticipo",
    "tipo_camion": "Tipo de Camión",
    "tipo_carga": "Tipo de Carga",
    "tipo_comprobante": "Tipo de Comprobante",
    "tipo_concepto_complemento": "Concepto de Complemento",
    "tipo_concepto_descuento": "Concepto de Descuento",
    "tipo_contraparte": "Tipo de Contraparte",
    "tipo_cuenta": "Tipo de Cuenta",
    "tipo_documento": "Tipo de Documento",
    "tipo_documento_relacionado": "Tipo de Documento Relacionado",
    "tipo_instrumento": "Tipo de Instrumento",
    "tipo_insumo": "Tipo de Insumo",
    "tipo_iva": "Tipo de IVA",
    "tipo_movimiento": "Tipo de Movimiento",
    "tipo_persona": "Tipo Persona",
    "tipo_registro": "Tipo de Registro",
    "tipo_semi": "Tipo de Semi",
    "unidad": "Unidad",
    "usuario": "Usuario",
}
