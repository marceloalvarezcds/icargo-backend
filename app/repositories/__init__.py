# should be imported to help code editor (vscode) for autocompletion
from .banco import (  # noqa
    change_banco_status,
    create_banco,
    delete_banco,
    edit_banco,
    get_banco_by,
    get_banco_by_id,
    get_banco_list,
    get_banco_list_by_gestor_carga_id,
)
from .caja import (  # noqa
    change_caja_status,
    create_caja,
    delete_caja,
    edit_caja,
    get_caja_by,
    get_caja_by_id,
    get_caja_list,
    get_caja_list_by_gestor_carga_id,
)
from .camion import (  # noqa
    change_camion_status,
    create_camion,
    delete_camion,
    edit_camion,
    get_camion_by,
    get_camion_by_id,
    get_camion_list,
    get_camion_list_by_gestor_cuenta_id,
    get_camion_list_by_propietario_id,
)
from .camion_semi_neto import (  # noqa
    get_camion_semi_neto_by_camion_id_and_semi_id,
    get_camion_semi_neto_by_camion_id_and_semi_id_and_producto_id,
    get_camion_semi_neto_list_by_camion_id,
    get_camion_semi_neto_list_by_camion_id_and_producto_id,
    get_camion_semi_neto_list_by_producto_id,
    get_camion_semi_neto_list_by_producto_id_null,
)
from .cargo import get_cargo_by_descripcion, get_cargo_list  # noqa
from .centro_operativo import (  # noqa
    create_centro_operativo,
    delete_centro_operativo,
    edit_centro_operativo,
    get_centro_operativo_by,
    get_centro_operativo_by_id,
    get_centro_operativo_list,
    get_centro_operativo_list_by_gestor_cuenta_id,
)
from .centro_operativo_clasificacion import (  # noqa
    get_centro_operativo_clasificacion_by_nombre,
    get_centro_operativo_clasificacion_list,
)
from .centro_operativo_contacto_gestor_carga import (  # noqa
    create_centro_operativo_contacto_gestor_carga,
    delete_centro_operativo_contacto_gestor_carga,
    edit_centro_operativo_contacto_gestor_carga,
    get_centro_operativo_contacto_gestor_carga_by,
    get_centro_operativo_contacto_gestor_carga_by_id,
)
from .chofer import (  # noqa
    change_chofer_status,
    create_chofer,
    delete_chofer,
    edit_chofer,
    get_chofer_by,
    get_chofer_by_id,
    get_chofer_list,
    get_chofer_list_by_gestor_cuenta_id,
)
from .chofer_propietario import (  # noqa
    create_propietario_by_chofer,
    edit_propietario_by_chofer,
)
from .ciudad import get_ciudad_by_nombre_and_localidad_id, get_ciudad_list  # noqa
from .color import get_color_by_descripcion, get_color_list  # noqa
from .composicion_juridica import (  # noqa
    get_composicion_juridica_by_nombre,
    get_composicion_juridica_list,
)
from .contacto import (  # noqa
    create_contacto,
    edit_contacto,
    get_contacto_by_email,
    get_contacto_by_id,
    get_contacto_by_telefono,
    get_contacto_by_telefono_and_email,
)
from .ente_emisor_automotor import (  # noqa
    get_ente_emisor_automotor_by_descripcion,
    get_ente_emisor_automotor_list,
)
from .ente_emisor_transporte import (  # noqa
    get_ente_emisor_transporte_by_descripcion,
    get_ente_emisor_transporte_list,
)
from .flete import (  # noqa
    change_flete_public_status,
    change_flete_status,
    create_flete,
    delete_flete,
    edit_flete,
    get_flete_by_id,
    get_flete_list,
    get_flete_list_by_gestor_carga_id,
    update_flete_destinatarios,
)
from .flete_anticipo import (  # noqa
    create_flete_anticipo,
    delete_flete_anticipo,
    edit_flete_anticipo,
    get_flete_anticipo_by,
    get_flete_anticipo_by_id,
    get_flete_anticipo_list_by_flete_id,
)
from .flete_complemento import (  # noqa
    create_flete_complemento,
    delete_flete_complemento,
    edit_flete_complemento,
    get_flete_complemento_by,
    get_flete_complemento_by_id,
)
from .flete_descuento import (  # noqa
    create_flete_descuento,
    delete_flete_descuento,
    edit_flete_descuento,
    get_flete_descuento_by,
    get_flete_descuento_by_id,
)
from .gestor_carga import (  # noqa
    create_gestor_carga,
    delete_gestor_carga,
    edit_gestor_carga,
    get_gestor_carga_by,
    get_gestor_carga_by_id,
    get_gestor_carga_list,
)
from .gestor_carga_centro_operativo import (  # noqa
    create_gestor_carga_centro_operativo,
    edit_gestor_carga_centro_operativo,
    get_gestor_carga_centro_operativo_by,
)
from .gestor_carga_chofer import (  # noqa
    create_gestor_carga_chofer,
    edit_gestor_carga_chofer,
    get_gestor_carga_chofer_by,
)
from .gestor_carga_propietario import (  # noqa
    create_gestor_carga_propietario,
    edit_gestor_carga_propietario,
    get_gestor_carga_propietario_by,
)
from .gestor_carga_proveedor import (  # noqa
    create_gestor_carga_proveedor,
    edit_gestor_carga_proveedor,
    get_gestor_carga_proveedor_by,
)
from .gestor_carga_punto_venta import (  # noqa
    create_gestor_carga_punto_venta,
    edit_gestor_carga_punto_venta,
    get_gestor_carga_punto_venta_by,
)
from .gestor_carga_remitente import (  # noqa
    create_gestor_carga_remitente,
    edit_gestor_carga_remitente,
    get_gestor_carga_remitente_by,
)
from .insumo import (  # noqa
    get_insumo_by_descripcion,
    get_insumo_list,
    get_insumo_list_by_tipo_insumo_id,
)
from .insumo_punto_venta import (  # noqa
    get_insumo_punto_venta_by_id,
    get_insumo_punto_venta_by_insumo_id_and_moneda_id_and_punto_venta_id,
    get_insumo_punto_venta_list_by_gestor_carga_id,
    get_insumo_punto_venta_list_by_insumo_id,
    get_insumo_punto_venta_list_by_insumo_id_and_punto_venta_id,
    get_insumo_punto_venta_list_by_tipo_insumo_id,
)
from .insumo_punto_venta_precio import (  # noqa
    get_last_insumo_punto_venta_precio_by_insumo_punto_venta_id,
)
from .localidad import get_localidad_by_nombre_and_pais_id, get_localidad_list  # noqa
from .marca_camion import get_marca_camion_by_descripcion, get_marca_camion_list  # noqa
from .marca_semi import get_marca_semi_by_descripcion, get_marca_semi_list  # noqa
from .moneda import get_moneda_by_simbolo, get_moneda_list  # noqa
from .orden_carga import (  # noqa
    aceptar_orden_carga,
    arribado_a_cargar_orden_carga,
    arribado_a_descargar_orden_carga,
    cancelar_orden_carga,
    cargar_orden_carga,
    change_orden_carga_anticipos_liberados,
    change_orden_carga_status,
    conciliar_orden_carga,
    contabilizar_orden_carga,
    create_orden_carga,
    delete_orden_carga,
    descargar_orden_carga,
    edit_orden_carga,
    finalizar_orden_carga,
    get_orden_carga_by_id,
    get_orden_carga_list_by_gestor_carga_id,
    liquidar_orden_carga,
)
from .orden_carga_anticipo_retirado import (  # noqa
    create_orden_carga_anticipo_retirado,
    delete_orden_carga_anticipo_retirado,
    edit_orden_carga_anticipo_retirado,
    get_orden_carga_anticipo_retirado_by,
    get_orden_carga_anticipo_retirado_by_id,
)
from .orden_carga_anticipo_saldo import (  # noqa
    create_orden_carga_anticipo_saldo,
    delete_orden_carga_anticipo_saldo,
    edit_orden_carga_anticipo_saldo,
    get_orden_carga_anticipo_saldo_by,
    get_orden_carga_anticipo_saldo_by_id,
)
from .orden_carga_complemento import (  # noqa
    create_orden_carga_complemento,
    delete_orden_carga_complemento,
    edit_orden_carga_complemento,
    get_orden_carga_complemento_by_id,
)
from .orden_carga_complemento_flete import (  # noqa
    create_orden_carga_complemento_by_flete,
)
from .orden_carga_descuento import (  # noqa
    create_orden_carga_descuento,
    delete_orden_carga_descuento,
    edit_orden_carga_descuento,
    get_orden_carga_descuento_by_id,
)
from .orden_carga_descuento_flete import create_orden_carga_descuento_by_flete  # noqa
from .orden_carga_estado_historial import create_orden_carga_estado_historial  # noqa
from .orden_carga_remision_destino import (  # noqa
    create_orden_carga_remision_destino,
    delete_orden_carga_remision_destino,
    edit_orden_carga_remision_destino,
    get_orden_carga_remision_destino_by,
    get_orden_carga_remision_destino_by_id,
)
from .orden_carga_remision_origen import (  # noqa
    create_orden_carga_remision_origen,
    delete_orden_carga_remision_origen,
    edit_orden_carga_remision_origen,
    get_orden_carga_remision_origen_by,
    get_orden_carga_remision_origen_by_id,
    get_orden_carga_remision_origen_list_by_orden_carga_id,
)
from .pais import get_pais_by_nombre_corto, get_pais_list  # noqa
from .permiso import get_permiso_by, get_permiso_list  # noqa
from .producto import get_producto_by_descripcion, get_producto_list  # noqa
from .propietario import (  # noqa
    change_propietario_status,
    create_propietario,
    delete_propietario,
    edit_propietario,
    get_propietario_by,
    get_propietario_by_id,
    get_propietario_list,
    get_propietario_list_by_gestor_cuenta_id,
)
from .propietario_chofer import (  # noqa
    create_chofer_by_propietario,
    edit_chofer_by_propietario,
)
from .propietario_contacto_gestor_carga import (  # noqa
    create_propietario_contacto_gestor_carga,
    delete_propietario_contacto_gestor_carga,
    edit_propietario_contacto_gestor_carga,
    get_propietario_contacto_gestor_carga_by,
)
from .proveedor import (  # noqa
    create_proveedor,
    delete_proveedor,
    edit_proveedor,
    get_proveedor_by,
    get_proveedor_by_id,
    get_proveedor_list,
    get_proveedor_list_by_gestor_cuenta_id,
)
from .proveedor_contacto_gestor_carga import (  # noqa
    create_proveedor_contacto_gestor_carga,
    delete_proveedor_contacto_gestor_carga,
    edit_proveedor_contacto_gestor_carga,
    get_proveedor_contacto_gestor_carga_by,
)
from .punto_venta import (  # noqa
    create_punto_venta,
    delete_punto_venta,
    edit_punto_venta,
    get_punto_venta_by,
    get_punto_venta_by_id,
    get_punto_venta_list,
)
from .punto_venta_contacto_gestor_carga import (  # noqa
    create_punto_venta_contacto_gestor_carga,
    delete_punto_venta_contacto_gestor_carga,
    edit_punto_venta_contacto_gestor_carga,
    get_punto_venta_contacto_gestor_carga_by,
)
from .remitente import (  # noqa
    create_remitente,
    delete_remitente,
    edit_remitente,
    get_remitente_by,
    get_remitente_by_id,
    get_remitente_list,
    get_remitente_list_by_gestor_cuenta_id,
)
from .remitente_contacto_gestor_carga import (  # noqa
    create_remitente_contacto_gestor_carga,
    delete_remitente_contacto_gestor_carga,
    edit_remitente_contacto_gestor_carga,
    get_remitente_contacto_gestor_carga_by,
    get_remitente_contacto_gestor_carga_by_id,
)
from .rol import get_rol_by_codigo, get_rol_list  # noqa
from .semi import (  # noqa
    change_semi_status,
    create_semi,
    delete_semi,
    edit_semi,
    get_semi_by,
    get_semi_by_id,
    get_semi_list,
    get_semi_list_by_propietario_id,
)
from .semi_clasificacion import (  # noqa
    get_semi_clasificacion_by_descripcion,
    get_semi_clasificacion_list,
)
from .tipo_anticipo import (  # noqa
    get_tipo_anticipo_by_descripcion,
    get_tipo_anticipo_list,
)
from .tipo_camion import get_tipo_camion_by_descripcion, get_tipo_camion_list  # noqa
from .tipo_carga import get_tipo_carga_by_descripcion, get_tipo_carga_list  # noqa
from .tipo_comprobante import (  # noqa
    get_tipo_comprobante_by_descripcion,
    get_tipo_comprobante_list,
)
from .tipo_concepto_complemento import (  # noqa
    get_tipo_concepto_complemento_by_descripcion,
    get_tipo_concepto_complemento_list,
)
from .tipo_concepto_descuento import (  # noqa
    get_tipo_concepto_descuento_by_descripcion,
    get_tipo_concepto_descuento_list,
)
from .tipo_documento import (  # noqa
    get_tipo_documento_by_descripcion,
    get_tipo_documento_list,
)
from .tipo_insumo import get_tipo_insumo_by_descripcion, get_tipo_insumo_list  # noqa
from .tipo_persona import get_tipo_persona_by_descripcion, get_tipo_persona_list  # noqa
from .tipo_registro import (  # noqa
    get_tipo_registro_by_descripcion,
    get_tipo_registro_list,
)
from .tipo_semi import get_tipo_semi_by_descripcion, get_tipo_semi_list  # noqa
from .unidad import get_unidad_by_descripcion, get_unidad_list  # noqa
from .user import (  # noqa
    create,
    get,
    get_by_email,
    get_by_username,
    get_user_list_by_gestor_carga_id,
)
