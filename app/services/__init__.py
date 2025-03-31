# should be imported to help code editor (vscode) for autocompletion
from .auth import (  # noqa
    get_auth_user_from_authorization_header,
    get_authorization_header,
    login,
)
from .banco import (  # noqa
    create_banco,
    delete_banco,
    edit_banco,
    get_banco_by_id,
    get_banco_list,
    get_banco_reports,
)
from .caja import (  # noqa
    create_caja,
    delete_caja,
    edit_caja,
    get_caja_by_id,
    get_caja_list,
    get_caja_reports,
)
from .camion import (  # noqa
    change_camion_status,
    create_camion,
    delete_camion,
    edit_camion,
    get_camion_by_id,
    get_camion_reports,
    check_combinaciones_activas,
)
from .camion_semi_neto import (  # noqa
    create_camion_semi_neto,
    delete_camion_semi_neto,
    edit_camion_semi_neto,
    get_camion_list_by_producto_id,
    get_camion_semi_neto_by_camion_id_and_semi_id_and_producto_id,
    get_semi_list_by_camion_id_and_producto_id,
)
from .centro_operativo import (  # noqa
    create_centro_operativo,
    delete_centro_operativo,
    edit_centro_operativo,
    get_centro_operativo_by_id,
    get_centro_operativo_by_id_and_gestor_carga_id,
    get_centro_operativo_reports,
)
from .centro_operativo_contacto import update_centro_operativo_contacto_list  # noqa
from .chofer import (  # noqa
    change_chofer_status,
    create_chofer,
    delete_chofer,
    edit_chofer,
    get_chofer_by_id,
    get_chofer_by_id_and_gestor_cuenta_id,
    get_chofer_list_without_camion_by_camion_id,
    get_chofer_reports,
)
from .ciudad import get_ciudad_list  # noqa
from .contacto import get_contacto_by  # noqa
from .contraparte import get_contraparte_list_by_tipo_contraparte_id  # noqa
from .estado_cuenta import (  # noqa
    get_estado_cuenta_by_contraparte,
    get_estado_cuenta_list,
    get_estado_cuenta_reports,
    get_nuevo_servicio,
    get_saldo_cuenta_contraparte,
    get_report_nuevo_servicio,
    get_estado_cuenta_pdv_list,
    get_estado_cuenta_pdv,
)
from .factura import (  # noqa
    create_factura,
    delete_factura,
    edit_factura,
    get_factura_by_id,
)
from .flete import (  # noqa
    change_flete_public_status,
    change_flete_status,
    create_flete,
    delete_flete,
    edit_flete,
    get_flete_detail_by_id,
    get_flete_reports,
    get_flete_datail_by_id
)
from .flete_anticipo import (  # noqa
    get_tipo_anticipo_insumo_list,
    get_tipo_anticipo_list_by_flete_id,
    get_tipo_insumo_list_by_flete_id,
    get_flete_anticipo_by_flete_and_tipo,
)
from .flete_destinatario import get_destinatario_list_by  # noqa
from .gestor_carga import (  # noqa
    create_gestor_carga,
    delete_gestor_carga,
    edit_gestor_carga,
    get_gestor_carga_by_id,
    get_gestor_carga_reports,
)
from .gestor_carga_centro_operativo import (  # noqa
    create_gestor_carga_centro_operativo,
    edit_gestor_carga_centro_operativo,
)
from .gestor_carga_chofer import (  # noqa
    create_gestor_carga_chofer,
    edit_gestor_carga_chofer,
)
from .gestor_carga_propietario import (  # noqa
    create_gestor_carga_propietario,
    edit_gestor_carga_propietario,
)
from .gestor_carga_proveedor import (  # noqa
    create_gestor_carga_proveedor,
    edit_gestor_carga_proveedor,
)
from .gestor_carga_punto_venta import (  # noqa
    create_gestor_carga_punto_venta,
    edit_gestor_carga_punto_venta,
)
from .gestor_carga_remitente import (  # noqa
    create_gestor_carga_remitente,
    edit_gestor_carga_remitente,
)
from .instrumento import (  # noqa
    confirmar_instrumento,
    create_instrumento,
    delete_instrumento,
    edit_instrumento,
    get_instrumento_by_id,
    get_instrumento_reports,
    rechazar_instrumento,
)
from .insumo_punto_venta import (  # noqa
    get_insumo_list_by_tipo_insumo_id_and_gestor_carga_id,
    get_moneda_list_by_insumo_id_and_punto_venta_id,
    get_proveedor_list_by_insumo_id,
    get_punto_venta_list_by_insumo_id_and_proveedor_id,
    get_tipo_insumo_list_by_flete_id_and_gestor_carga_id,
    get_insumo_venta_precio_list,
    get_all_insumo_punto_venta_list,
)
from .insumo_punto_venta_precio import (  # noqa
    create_insumo_punto_venta_precio,
    get_insumo_punto_venta_precio_by_insumo_id_and_moneda_id_and_punto_venta_id,
    edit_insumo_punto_venta_precio,
    get_insumo_punto_venta_precio_list,
    get_insumo_punto_venta_precio_reports,
    get_insumo_punto_venta_precio_by_id,
    get_all_insumo_punto_venta_precio_list,
    get_insumos_by_punto_venta_id_and_gestor_carga,
    update_insumo_punto_venta_precio,
    edit_and_create_insumo_punto_venta_precio,
    update_insumo_punto_venta_precio_by_insumo_punto_venta,
    get_insumo_punto_venta_precio_list_by_estado_activo,
    get_inactive_insumo_punto_venta_precio_list,
    get_active_insumo_punto_venta_precio_list,
    create_or_update_insumo_punto_venta_precio,
    change_insumo_precio_venta_status,
    change_inactive_insumo_precio_venta_status,
    get_insumo_venta_precio_by_id,
)
from .liquidacion import (  # noqa
    aceptar_liquidacion,
    add_instrumentos,
    add_movimientos,
    cancelar_liquidacion,
    create_liquidacion,
    create_liquidacion_pendiente,
    delete_liquidacion,
    edit_liquidacion,
    en_revision_liquidacion,
    get_liquidacion_by_id,
    get_liquidacion_list,
    get_liquidacion_list_by_estado_cuenta,
    get_liquidacion_reports,
    get_liquidacion_reports_by_estado_cuenta,
    get_liquidacion_resumen_pdf_by_id,
    rechazar_liquidacion,
    remove_movimiento,
    someter_liquidacion,
    remove_movimientos,
    refresh_pago_cobro
)
from .movimiento import (  # noqa
    create_movimiento,
    create_movimiento_by_anticipo,
    create_movimiento_by_conciliacion_oc,
    create_movimiento_by_tipo_documento_relacionado_otro,
    delete_movimiento,
    edit_movimiento,
    edit_movimiento_by_gestor_flete,
    edit_movimiento_by_gestor_merma,
    edit_movimiento_by_propietario_flete,
    edit_movimiento_by_propietario_merma,
    get_movimiento_by_id,
    get_movimiento_list,
    get_movimiento_list_by_estado_cuenta,
    get_movimiento_list_by_liquidacion,
    get_movimiento_reports,
    get_movimiento_reports_by_contraparte,
    get_movimiento_reports_by_gestor_carga_id,
    get_all_movimiento_list_by_estado_cuenta,
    get_movimiento_estado_cuenta_reports_by_contraparte,
    create_movimiento_by_factura,
)
from .orden_carga import (  # noqa
    aceptar_orden_carga,
    arribado_a_cargar_orden_carga,
    arribado_a_descargar_orden_carga,
    cancelar_orden_carga,
    cargar_orden_carga,
    change_orden_carga_anticipos_liberados,
    conciliar_orden_carga,
    contabilizar_orden_carga,
    create_orden_carga,
    delete_orden_carga,
    descargar_orden_carga,
    edit_orden_carga,
    finalizar_orden_carga,
    get_orden_carga_by_id,
    get_orden_carga_detail,
    get_orden_carga_list,
    get_orden_carga_pdf_by_id,
    get_orden_carga_reports,
    get_orden_carga_resumen_pdf_by_id,
    liquidar_orden_carga,
    send_oc_mail,
    get_orden_carga_combinacion_detail,
    get_orden_carga_list_by_combinacion_id,
    get_orden_carga_list_combinacion,
    get_ordenes_carga_by_combinacion_id,
    get_ordenes_carga_by_combinacion_id_and_finalizar,
    get_ordenes_carga_by_combinacion_id_and_aceptado,
    get_ordenes_carga_by_combinacion_id_and_nuevo,
    update_comentarios,
    create_orden_carga_comentarios_historial,
    get_orden_carga_list_detail,
    get_orden_carga_aceptadas_list,
    get_orden_carga_finalizadas_list,
    edit_remitir_fecha,
    get_orden_carga_en_proceso_list,
    get_orden_carga_cerradas_list,
)
from .orden_carga_anticipo_retirado import (  # noqa
    create_orden_carga_anticipo_retirado,
    delete_orden_carga_anticipo_retirado,
    edit_orden_carga_anticipo_retirado,
    get_orden_carga_anticipo_retirado_by_id,
    get_orden_carga_anticipo_retirado_pdf_by_id,
    change_anticipo_status,
)
from .orden_carga_anticipo_saldo import (  # noqa
    get_saldo_anticipo_by_flete_anticipo_id_and_orden_carga_id,
    get_saldos_by_orden_carga,
    get_flete_anticipo_by_orden_carga_insumos,
    get_flete_anticipo_id_by_flete_id_and_orden_carga_id,
)
from .orden_carga_complemento import (  # noqa
    create_orden_carga_complemento,
    delete_orden_carga_complemento,
    edit_orden_carga_complemento,
    get_orden_carga_complemento_by_id,
)
from .orden_carga_descuento import (  # noqa
    create_orden_carga_descuento,
    delete_orden_carga_descuento,
    edit_orden_carga_descuento,
    get_orden_carga_descuento_by_id,
)
from .orden_carga_evaluacion import (  # noqa
    get_orden_carga_evaluaciones_historial_by_id,
    create_orden_carga_evaluacion,
)
from .orden_carga_remision_destino import (  # noqa
    create_orden_carga_remision_destino,
    delete_orden_carga_remision_destino,
    edit_orden_carga_remision_destino,
    get_orden_carga_remision_destino_by_id,
)
from .orden_carga_remision_origen import (  # noqa
    create_orden_carga_remision_origen,
    delete_orden_carga_remision_origen,
    edit_orden_carga_remision_origen,
    get_orden_carga_remision_origen_by_id,
)
from .pictshare import (  # noqa
    check_duplicate_images,
    upload_and_get_binary_url,
    upload_and_get_image_url,
    upload_image,
)
from .propietario import (  # noqa
    change_propietario_status,
    create_propietario,
    delete_propietario,
    edit_propietario,
    get_propietario_by_id,
    get_propietario_by_id_and_gestor_cuenta_id,
    get_tipo_persona_by_id,
    get_propietario_list_by_gestor_cuenta_and_camion_id,
    get_propietario_list_by_gestor_cuenta_and_semi_id,
    get_propietario_reports,
    get_propietario_list_by_tipo_persona_id,
    get_propietario_list_by_id,
)
from .propietario_contacto import update_propietario_contacto_list  # noqa
from .proveedor import (  # noqa
    create_proveedor,
    delete_proveedor,
    edit_proveedor,
    get_proveedor_by_id,
    get_proveedor_by_id_and_gestor_carga_id,
    get_proveedor_reports,
)
from .proveedor_contacto import update_proveedor_contacto_list  # noqa
from .punto_venta import (  # noqa
    create_punto_venta,
    delete_punto_venta,
    edit_punto_venta,
    get_punto_venta_by_id,
    get_punto_venta_by_id_and_gestor_carga_id,
    get_punto_venta_reports,
)
from .punto_venta_contacto import update_punto_venta_contacto_list  # noqa
from .remitente import (  # noqa
    create_remitente,
    delete_remitente,
    edit_remitente,
    get_remitente_by_id,
    get_remitente_by_id_and_gestor_carga_id,
    get_remitente_reports,
)
from .remitente_contacto import update_remitente_contacto_list  # noqa
from .rentabilidad import get_rentabilidad_list, get_rentabilidad_reports  # noqa
from .rol import (  # noqa
    change_rol_status,
    create_rol,
    delete_rol,
    edit_rol,
    get_rol_active_list,
    get_rol_by_id,
    get_rol_list,
)
from .security import create_access_token  # noqa
from .semi import (  # noqa
    change_semi_status,
    create_semi,
    delete_semi,
    edit_semi,
    get_semi_by_id,
    get_semi_reports,
)
from .tipo_cuenta import (  # noqa
    create_tipo_cuenta,
    edit_tipo_cuenta,
    get_tipo_cuenta_active_list_by_tipo_documento_relacionado_otro,
    get_tipo_cuenta_list_by_tipo_documento_relacionado_otro,
    get_tipo_cuenta_list,
    get_tipo_cuenta_active_list
)
from .tipo_instrumento import get_tipo_instrumento_via_banco  # noqa
from .tipo_movimiento import (  # noqa
    create_tipo_movimiento,
    edit_tipo_movimiento,
    get_tipo_movimiento_active_list_by_tipo_cuenta_other_than_viajes,
    get_tipo_movimiento_list_by_tipo_cuenta_other_than_viajes,
    get_tipo_movimiento_list,
    get_tipo_movimiento_active_list
)
from .user import (  # noqa
    change_user_status,
    create_user,
    create_user_with_rol_list,
    delete_user,
    edit_user,
    edit_user_with_rol_list,
    get_user_account,
    get_user_active_list_by_gestor_carga_id,
    get_user_by_id,
    get_user_by_username,
    get_user_list_by_gestor_carga_id,
    get_user_list_with_rol_list_by_gestor_carga_id,
    get_user_with_rol_list_by_id,
)
from .combinacion import (
    get_combinacion_by_id,
    create_combinacion,
    edit_combinacion,
    get_combinacion_reports,
    get_combinacion_by_gestor_cuenta_and_combinacion_id,
    change_combinacion_status,
    get_combinacion_list,
    get_camion_list_combinacion,
    get_semi_list_by_camion_id,
    get_combinacion_by_camion_id_and_semi_id_,
)
from .contribuyente import (
    get_list,
    #get_by_id,
)
from .texto_legal_service import (
    get_texto_legal_list,
    get_texto_legal_list_by_gestor,
    get_texto_legal_by_id,
    crear_texto_legal,
    edit_texto_legal
)
from .moneda_cotizacion import (read_cotizacion_moneda)