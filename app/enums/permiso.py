from enum import Enum


class PermisoAccionEnum(Enum):
    CREAR = "crear"
    EDITAR = "editar"
    ELIMINAR = "eliminar"
    LISTAR = "listar"
    MODIFICAR_CONTACTOS = "modificar_contactos"
    MODIFICAR_ALIAS = "modificar_alias"
    VER = "ver"
    REPORTE = "reporte"


class PermisoModeloEnum(Enum):
    CARGO = "cargo"
    CENTRO_OPERATIVO_CLASIFICACION = "centro_operativo_clasificacion"
    CENTRO_OPERATIVO = "centro_operativo"
    CIUDAD = "ciudad"
    COMPOSICION_JURIDICA = "composicion_juridica"
    CONTACTO = "contacto"
    GESTOR_CARGA = "gestor_carga"
    LOCALIDAD = "localidad"
    MONEDA = "moneda"
    PAIS = "pais"
    PERMISO = "permiso"
    PROPIETARIO = "propietario"
    PROVEEDOR = "proveedor"
    PUNTO_VENTA = "punto_venta"
    REMITENTE = "remitente"
    ROL = "rol"
    TIPO_DOCUMENTO = "tipo_documento"
    TIPO_PERSONA = "tipo_persona"
    USER = "usuario"
