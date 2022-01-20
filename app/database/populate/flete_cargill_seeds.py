from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import FleteDestinatarioEnum
from app.enums.estado import EstadoEnum
from app.models import CentroOperativoContactoGestorCarga, RemitenteContactoGestorCarga
from app.repositories import (
    get_centro_operativo_by_id,
    get_flete_by_id,
    get_moneda_by_simbolo,
    get_producto_by_descripcion,
    get_remitente_by_id,
    get_tipo_anticipo_by_descripcion,
    get_tipo_carga_by_descripcion,
    get_tipo_concepto_complemento_by_descripcion,
    get_tipo_concepto_descuento_by_descripcion,
    get_tipo_insumo_by_descripcion,
    get_unidad_by_descripcion,
)
from app.schemas import (
    FleteAnticipoForm,
    FleteComplementoForm,
    FleteDescuentoForm,
    FleteDestinatario,
    FleteForm,
)
from app.services import change_flete_status, create_flete


def flete_cargill_seeds(db: Session, gestor_cuenta_id: Optional[int]):
    modified_by = "system"

    destino15 = get_centro_operativo_by_id(db, 15)
    destino17 = get_centro_operativo_by_id(db, 17)

    origen14 = get_centro_operativo_by_id(db, 14)
    origen16 = get_centro_operativo_by_id(db, 16)

    remitente13 = get_remitente_by_id(db, 13)
    remitente15 = get_remitente_by_id(db, 15)

    pyg = get_moneda_by_simbolo(db, "PYG")
    bop = get_moneda_by_simbolo(db, "BOP")

    aceite = get_producto_by_descripcion(db, "Aceite de Soja")
    ganado = get_producto_by_descripcion(db, "Ganado")

    efectivo = get_tipo_anticipo_by_descripcion(db, "EFECTIVO")
    tipo_insumo = get_tipo_anticipo_by_descripcion(db, "TIPO DE INSUMO")

    combustible = get_tipo_insumo_by_descripcion(db, "COMBUSTIBLE")
    lubricantes = get_tipo_insumo_by_descripcion(db, "LUBRICANTES")

    seca = get_tipo_carga_by_descripcion(db, "SECA")
    liquida = get_tipo_carga_by_descripcion(db, "LÍQUIDA")

    peaje = get_tipo_concepto_complemento_by_descripcion(db, "Peaje")
    expurgo = get_tipo_concepto_complemento_by_descripcion(db, "Expurgo")

    sistema = get_tipo_concepto_descuento_by_descripcion(db, "Sistema")
    seguro = get_tipo_concepto_descuento_by_descripcion(db, "Seguro")

    toneladas = get_unidad_by_descripcion(db, "Toneladas")
    kilogramos = get_unidad_by_descripcion(db, "Kilogramos")

    if (
        gestor_cuenta_id
        and destino15
        and destino17
        and origen14
        and origen16
        and remitente13
        and remitente15
        and pyg
        and bop
        and aceite
        and ganado
        and efectivo
        and combustible
        and lubricantes
        and tipo_insumo
        and seca
        and liquida
        and peaje
        and expurgo
        and sistema
        and seguro
        and toneladas
        and kilogramos
    ):
        destino15_contacto: CentroOperativoContactoGestorCarga = destino15.contactos[0]
        destino17_contacto: CentroOperativoContactoGestorCarga = destino17.contactos[0]
        origen14_contacto: CentroOperativoContactoGestorCarga = origen14.contactos[0]
        origen16_contacto: CentroOperativoContactoGestorCarga = origen16.contactos[0]
        remitente13_contacto: RemitenteContactoGestorCarga = remitente13.contactos[0]
        remitente15_contacto: RemitenteContactoGestorCarga = remitente15.contactos[0]

        flete5 = get_flete_by_id(db, 5)
        flete6 = get_flete_by_id(db, 6)
        if not flete5:
            create_flete(
                db,
                FleteForm(
                    remitente_id=remitente13.id,
                    producto_id=aceite.id,
                    tipo_carga_id=seca.id,
                    numero_lote="1300000",
                    publicado=True,
                    es_subasta=False,
                    # INICIO Tramo de Fletes
                    origen_id=origen14.id,
                    origen_indicacion="Origen Indicaciones",
                    destino_id=destino15.id,
                    destino_indicacion="Destino Indicaciones",
                    distancia=Decimal(500),
                    # FIN Tramo de Fletes
                    # INICIO Cantidad y Flete
                    condicion_cantidad=Decimal(500),
                    # inicio - Condiciones para el Gestor de Cuenta
                    condicion_gestor_cuenta_moneda_id=pyg.id,
                    condicion_gestor_cuenta_tarifa=Decimal(500),
                    condicion_gestor_cuenta_unidad_id=toneladas.id,
                    # fin - Condiciones para el Gestor de Cuenta
                    # inicio - Condiciones para el Propietario
                    condicion_propietario_moneda_id=pyg.id,
                    condicion_propietario_tarifa=Decimal(500),
                    condicion_propietario_unidad_id=toneladas.id,
                    # fin - Condiciones para el Propietario
                    # FIN Cantidad y Flete
                    # INICIO Mermas de Fletes
                    # inicio - Mermas para el Gestor de Cuenta
                    merma_gestor_cuenta_valor=Decimal(500),
                    merma_gestor_cuenta_moneda_id=pyg.id,
                    merma_gestor_cuenta_unidad_id=toneladas.id,
                    merma_gestor_cuenta_es_porcentual=False,
                    merma_gestor_cuenta_tolerancia=Decimal(500),
                    # fin - Mermas para el Gestor de Cuenta
                    # inicio - Mermas para el Propietario
                    merma_propietario_valor=Decimal(500),
                    merma_propietario_moneda_id=pyg.id,
                    merma_propietario_unidad_id=toneladas.id,
                    merma_propietario_es_porcentual=False,
                    merma_propietario_tolerancia=Decimal(500),
                    # fin - Mermas para el Propietario
                    # FIN Mermas de Fletes
                    # INICIO Emisión de Órdenes
                    emision_orden_texto_legal="Emisión de Órdenes - Texto Legal",
                    emision_orden_detalle="Emisión de Órdenes - Detalle",
                    destinatarios=[
                        FleteDestinatario(
                            id=destino15.id,
                            tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                            email=destino15_contacto.contacto_email,
                            nombre=f"{destino15_contacto.contacto_nombre} {destino15_contacto.contacto_apellido}",  # noqa: B950
                        ),
                        FleteDestinatario(
                            id=origen14.id,
                            tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                            email=origen14_contacto.contacto_email,
                            nombre=f"{origen14_contacto.contacto_nombre} {origen14_contacto.contacto_apellido}",  # noqa: B950
                        ),
                        FleteDestinatario(
                            id=remitente13.id,
                            tipo_destinatario=FleteDestinatarioEnum.REMITENTE,
                            email=remitente13_contacto.contacto_email,
                            nombre=f"{remitente13_contacto.contacto_nombre} {remitente13_contacto.contacto_apellido}",  # noqa: B950
                        ),
                    ],
                    # FIN Emisión de Órdenes
                    vigencia_anticipos=datetime(2022, 6, 1).isoformat(),
                    anticipos=[
                        FleteAnticipoForm(
                            tipo_id=efectivo.id,
                            tipo_descripcion=efectivo.descripcion,
                            porcentaje=Decimal(10),
                        ),
                        FleteAnticipoForm(
                            tipo_id=tipo_insumo.id,
                            tipo_descripcion=tipo_insumo.descripcion,
                            tipo_insumo_id=combustible.id,
                            tipo_insumo_descripcion=combustible.descripcion,
                            porcentaje=Decimal(10),
                        ),
                    ],
                    complementos=[
                        FleteComplementoForm(
                            concepto_id=peaje.id,
                            detalle="Flete Complemento Detalle",
                            habilitar_cobro_remitente=True,
                            anticipado=True,
                            # INICIO Monto a pagar al Propietario
                            propietario_monto=Decimal(100),
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a pagar al Propietario
                            # INICIO Monto a cobrar al Remitente
                            remitente_monto=Decimal(100),
                            remitente_moneda_id=pyg.id,
                        )
                    ],
                    descuentos=[
                        FleteDescuentoForm(
                            concepto_id=sistema.id,
                            detalle="Flete Descuento Detalle",
                            habilitar_pago_proveedor=True,
                            anticipado=True,
                            # INICIO Monto a cobrar al Propietario
                            propietario_monto=Decimal(100),
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a cobrar al Propietario
                            # INICIO Monto a pagar al Proveedor
                            proveedor_monto=Decimal(100),
                            proveedor_moneda_id=pyg.id,
                            proveedor_id=1,
                        ),
                        FleteDescuentoForm(
                            concepto_id=seguro.id,
                            detalle="Flete Descuento Detalle",
                            habilitar_pago_proveedor=True,
                            anticipado=True,
                            # INICIO Monto a cobrar al Propietario
                            propietario_monto=Decimal(100),
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a cobrar al Propietario
                            # INICIO Monto a pagar al Proveedor
                            proveedor_monto=Decimal(100),
                            proveedor_moneda_id=pyg.id,
                            proveedor_id=1,
                        ),
                    ],
                ),
                gestor_cuenta_id,
                modified_by,
            )
        if not flete6:
            create_flete(
                db,
                FleteForm(
                    remitente_id=remitente15.id,
                    producto_id=ganado.id,
                    tipo_carga_id=liquida.id,
                    numero_lote="1300000",
                    publicado=False,
                    es_subasta=False,
                    # INICIO Tramo de Fletes
                    origen_id=origen16.id,
                    origen_indicacion="Origen Indicaciones",
                    destino_id=destino17.id,
                    destino_indicacion="Destino Indicaciones",
                    distancia=Decimal(500),
                    # FIN Tramo de Fletes
                    # INICIO Cantidad y Flete
                    condicion_cantidad=Decimal(500),
                    # inicio - Condiciones para el Gestor de Cuenta
                    condicion_gestor_cuenta_moneda_id=bop.id,
                    condicion_gestor_cuenta_tarifa=Decimal(500),
                    condicion_gestor_cuenta_unidad_id=kilogramos.id,
                    # fin - Condiciones para el Gestor de Cuenta
                    # inicio - Condiciones para el Propietario
                    condicion_propietario_moneda_id=bop.id,
                    condicion_propietario_tarifa=Decimal(500),
                    condicion_propietario_unidad_id=kilogramos.id,
                    # fin - Condiciones para el Propietario
                    # FIN Cantidad y Flete
                    # INICIO Mermas de Fletes
                    # inicio - Mermas para el Gestor de Cuenta
                    merma_gestor_cuenta_valor=Decimal(500),
                    merma_gestor_cuenta_moneda_id=bop.id,
                    merma_gestor_cuenta_unidad_id=kilogramos.id,
                    merma_gestor_cuenta_es_porcentual=False,
                    merma_gestor_cuenta_tolerancia=Decimal(500),
                    # fin - Mermas para el Gestor de Cuenta
                    # inicio - Mermas para el Propietario
                    merma_propietario_valor=Decimal(500),
                    merma_propietario_moneda_id=bop.id,
                    merma_propietario_unidad_id=kilogramos.id,
                    merma_propietario_es_porcentual=False,
                    merma_propietario_tolerancia=Decimal(500),
                    # fin - Mermas para el Propietario
                    # FIN Mermas de Fletes
                    # INICIO Emisión de Órdenes
                    emision_orden_texto_legal="Emisión de Órdenes - Texto Legal",
                    emision_orden_detalle="Emisión de Órdenes - Detalle",
                    destinatarios=[
                        FleteDestinatario(
                            id=destino17.id,
                            tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                            email=destino17_contacto.contacto_email,
                            nombre=f"{destino17_contacto.contacto_nombre} {destino17_contacto.contacto_apellido}",  # noqa: B950
                        ),
                        FleteDestinatario(
                            id=origen16.id,
                            tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                            email=origen16_contacto.contacto_email,
                            nombre=f"{origen16_contacto.contacto_nombre} {origen16_contacto.contacto_apellido}",  # noqa: B950
                        ),
                        FleteDestinatario(
                            id=remitente15.id,
                            tipo_destinatario=FleteDestinatarioEnum.REMITENTE,
                            email=remitente15_contacto.contacto_email,
                            nombre=f"{remitente15_contacto.contacto_nombre} {remitente15_contacto.contacto_apellido}",  # noqa: B950
                        ),
                    ],
                    # FIN Emisión de Órdenes
                    vigencia_anticipos=datetime(2022, 6, 1).isoformat(),
                    anticipos=[
                        FleteAnticipoForm(
                            tipo_id=efectivo.id,
                            tipo_descripcion=efectivo.descripcion,
                            porcentaje=Decimal(10),
                        ),
                        FleteAnticipoForm(
                            tipo_id=tipo_insumo.id,
                            tipo_descripcion=tipo_insumo.descripcion,
                            tipo_insumo_id=combustible.id,
                            tipo_insumo_descripcion=combustible.descripcion,
                            porcentaje=Decimal(10),
                        ),
                        FleteAnticipoForm(
                            tipo_id=tipo_insumo.id,
                            tipo_descripcion=tipo_insumo.descripcion,
                            tipo_insumo_id=lubricantes.id,
                            tipo_insumo_descripcion=lubricantes.descripcion,
                            porcentaje=Decimal(10),
                        ),
                    ],
                    complementos=[
                        FleteComplementoForm(
                            concepto_id=peaje.id,
                            detalle="Flete Complemento Detalle",
                            habilitar_cobro_remitente=True,
                            anticipado=True,
                            # INICIO Monto a pagar al Propietario
                            propietario_monto=Decimal(100),
                            propietario_moneda_id=bop.id,
                            # FIN Monto a pagar al Propietario
                            # INICIO Monto a cobrar al Remitente
                            remitente_monto=Decimal(100),
                            remitente_moneda_id=bop.id,
                        ),
                        FleteComplementoForm(
                            concepto_id=expurgo.id,
                            detalle="Flete Complemento Detalle",
                            habilitar_cobro_remitente=True,
                            anticipado=True,
                            # INICIO Monto a pagar al Propietario
                            propietario_monto=Decimal(100),
                            propietario_moneda_id=bop.id,
                            # FIN Monto a pagar al Propietario
                            # INICIO Monto a cobrar al Remitente
                            remitente_monto=Decimal(100),
                            remitente_moneda_id=bop.id,
                        ),
                    ],
                    descuentos=[
                        FleteDescuentoForm(
                            concepto_id=seguro.id,
                            detalle="Flete Descuento Detalle",
                            habilitar_pago_proveedor=True,
                            anticipado=True,
                            # INICIO Monto a cobrar al Propietario
                            propietario_monto=Decimal(100),
                            propietario_moneda_id=bop.id,
                            # FIN Monto a cobrar al Propietario
                            # INICIO Monto a pagar al Proveedor
                            proveedor_monto=Decimal(100),
                            proveedor_moneda_id=bop.id,
                            proveedor_id=1,
                        )
                    ],
                ),
                gestor_cuenta_id,
                modified_by,
            )
            flete6 = get_flete_by_id(db, 6)
            change_flete_status(db, 6, EstadoEnum.CANCELADO, modified_by)
