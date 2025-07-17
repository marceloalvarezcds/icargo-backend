from enum import Enum
from typing import Dict


class PermisoAccionEnum(Enum):
    INICIAR_SESION = "iniciar_sesion"
    ACEPTAR = "aceptar"
    CAMBIAR_ESTADO = "cambiar_estado"
    CANCELAR = "cancelar"
    CONCILIAR = "conciliar"
    FINALIZAR = "finalizar"
    ANTICIPO = "anticipo"
    RECEPCIONAR = "recepcionar"
    REMISIONAR = "remisionar"
    CREAR_EFECTIVO = 'crear_efectivo'
    CREAR_INSUMO = 'crear_insumo'
    CREAR = "crear"
    EDITAR = "editar"
    ELIMINAR = "eliminar"
    ANULAR = "anular"
    LISTAR = "listar"
    EN_PROCESO = "listar_en_proceso"
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
    COMBINACION = "combinacion"
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
    MONEDA_COTIZACION = "moneda_cotizacion"
    MOVIMIENTO = "movimiento"
    ORDEN_CARGA = "orden_carga"
    ORDEN_CARGA_ANTICIPO_RETIRADO = "orden_carga_anticipo_retirado"
    ORDEN_CARGA_ANTICIPO_SALDO = "orden_carga_anticipo_saldo"
    ORDEN_CARGA_COMPLEMENTO = "orden_carga_complemento"
    ORDEN_CARGA_DESCUENTO = "orden_carga_descuento"
    ORDEN_CARGA_EVALUACION = "orden_carga_evaluacion"
    ORDEN_CARGA_REMISION_DESTINO = "orden_carga_remision_destino"
    ORDEN_CARGA_REMISION_ORIGEN = "orden_carga_remision_origen"
    ORDEN_CARGA_REMISION_RESULTADO = "orden_carga_remision_resultado"
    ORDEN_CARGA_REMISION_RESULTADO_GESTOR = "orden_carga_remision_resultado_gestor"
    ORDEN_CARGA_REMISION_RESULTADO_PROPIETARIO = "orden_carga_remision_resultado_propietario"
    GESTION_DE_LINEA = 'gestion_de_linea'
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
    # TIPO_TRACTO = "tipo_tracto"
    TIPO_CARGA = "tipo_carga"
    TIPO_COMPROBANTE = "tipo_comprobante"
    TIPO_CONCEPTO_COMPLEMENTO = "tipo_concepto_complemento"
    TIPO_CONCEPTO_DESCUENTO = "tipo_concepto_descuento"
    TIPO_CONTRAPARTE = "tipo_contraparte"
    TIPO_CUENTA = "tipo_cuenta"
    TIPO_DOCUMENTO = "tipo_documento"
    TIPO_DOCUMENTO_RELACIONADO = "tipo_documento_relacionado"
    TIPO_EVALUACION = 'tipo_evaluacion'
    TIPO_INSTRUMENTO = "tipo_instrumento"
    TIPO_INSUMO = "tipo_insumo"
    TIPO_IVA = "tipo_iva"
    TIPO_MOVIMIENTO = "tipo_movimiento"
    TIPO_PERSONA = "tipo_persona"
    TIPO_REGISTRO = "tipo_registro"
    TIPO_SEMI = "tipo_semi"
    UNIDAD = "unidad"
    USER = "usuario"
    TEXTO_LEGAL ="texto_legal"



class PermisoModuloEnum(Enum):
    USUARIOS = "1 - Usuarios"
    ENTIDADES = "2 - Entidades"
    FLOTA = "3 - Flota"
    FLETE = "4 - Pedido"
    OC = "5 - Orden de Carga"
    CAJA_BANCO = "6 - Caja & Banco"
    ESTADO_CUENTA = "7 - Estado de Cuenta"
    LISTADOS = "8 - Listados"
    BIBLIOTECA = "9 - Biblioteca de Usuario"
    PARAMETROS = "Parámetros del Sistema"


permisoModeloTitulo: Dict[str, str] = {
    # USUARIOS
    "usuario": "1 - Usuario",
    "rol": "2 - Rol",
    "permiso": "3 - Permiso",
    # ENTIDADES
    "remitente": "1 - Remitente",
    "centro_operativo": "2 - Centro Operativo",
    "proveedor": "3 - Proveedor",
    "punto_venta": "4 - Punto de Venta",
    "gestor_carga": "5 - Gestor de Carga",
    "contacto": "6 - Contacto",
    # FLOTA
    "propietario": "1 - Propietario",
    "chofer": "2 - Chofer",
    "camion": "3 - Tracto",
    "semirremolque": "4 - Semi",
    "camion_semi_neto": "5 - Neto de la Combinacion Tracto-Semi",
    "combinacion": "6 - Combinacion",
    # FLETE
    "flete": "Flete",
    "flete_anticipo": "Flete Anticipo",
    "flete_complemento": "Flete Complemento",
    "flete_descuento": "Flete Descuento",
    # OC (Orden de Carga)
    "orden_carga": "1 - Orden de Carga",
    "orden_carga_complemento": "2 - Complemento",
    "orden_carga_descuento": "3 - Descuento",
    "orden_carga_anticipo_saldo": "4 - Saldo de Anticipo",
    "orden_carga_anticipo_retirado": "5 - Anticipo Retirado",
    "orden_carga_remision_destino": "6 - Remisión Destino",
    "orden_carga_remision_origen": "7 - Remisión Origen",
    "orden_carga_remision_resultado": "8 - Resultado de Remisión",
    "orden_carga_remision_resultado_gestor": "9 - Resultado de Remisión de la Gestora",
    "orden_carga_evaluacion": "10 - Evaluacion",
    # CAJA_BANCO
    "caja": "1 - Caja",
    "banco": "2 - Banco",
    # ESTADO_CUENTA
    "estado_cuenta": "1 - Estado de Cuenta",
    "movimiento": "2 - Movimiento",
    "liquidacion": "3 - Liquidación",
    "instrumento": "4 - Instrumento",
    "factura": "5 - Factura",
    # LISTADOS
    "rentabilidad": "Rentabilidad",
    # BIBLIOTECA
    "cargo": "Cargo",
    "moneda_cotizacion": "Cotizacion",
    "insumo_punto_venta": "Insumo Punto de Venta",
    "insumo_punto_venta_precio": "Precio de Insumo en Punto de Venta",
    # PARAMETROS
    "ciudad": "Ciudad",
    "centro_operativo_clasificacion": "Clasificación Centro Operativo",
    "semi_clasificacion": "Clasificación de Semi",
    "color": "Color",
    "combinacion": "Combinacion",
    "composicion_juridica": "Composición Jurídica",
    "ente_emisor_automotor": "Ente emisor de Registro Automotor",
    "ente_emisor_transporte": "Ente emisor de Registro de Transporte",
    "instrumento_via": "Vía de Instrumento",
    "insumo": "Insumo",
    "localidad": "Localidad",
    "marca_camion": "Marca de Tracto",
    "marca_semi": "Marca de Semi",
    "moneda": "Moneda",
    "pais": "País",
    "producto": "Producto",
    "tipo_anticipo": "Tipo de Tracto",
    "tipo_camion": "Tipo de Tracto",
    "tipo_carga": "Tipo de Carga",
    "tipo_comprobante": "Tipo de Comprobante",
    "tipo_concepto_complemento": "Concepto de Complemento",
    "tipo_concepto_descuento": "Concepto de Descuento",
    "tipo_contraparte": "Tipo de Contraparte",
    "tipo_cuenta": "Tipo de Cuenta",
    "tipo_documento": "Tipo de Documento",
    "tipo_documento_relacionado": "Tipo de Documento Relacionado",
    "tipo_instrumento": "Tipo de Instrumento",
    "tipo_evaluacion": "Tipo de Evaluacion",
    "tipo_insumo": "Tipo de Insumo",
    "tipo_iva": "Tipo de IVA",
    "tipo_movimiento": "Tipo de Movimiento",
    "tipo_persona": "Tipo Persona",
    "tipo_registro": "Tipo de Registro",
    "tipo_semi": "Tipo de Semi",
    "unidad": "Unidad",
    "texto_legal":"Texto Legal"
}
