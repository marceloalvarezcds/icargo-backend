from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import FleteDestinatarioEnum
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
from app.services import create_flete


def flete_seeds(db: Session, gestor_carga_id: Optional[int]):
    modified_by = "system"

    destino3 = get_centro_operativo_by_id(db, 3)
    destino5 = get_centro_operativo_by_id(db, 5)
    destino9 = get_centro_operativo_by_id(db, 9)
    destino11 = get_centro_operativo_by_id(db, 11)

    origen2 = get_centro_operativo_by_id(db, 2)
    origen4 = get_centro_operativo_by_id(db, 4)
    origen8 = get_centro_operativo_by_id(db, 8)
    origen12 = get_centro_operativo_by_id(db, 12)

    remitente1 = get_remitente_by_id(db, 1)
    remitente2 = get_remitente_by_id(db, 2)
    remitente3 = get_remitente_by_id(db, 3)
    remitente4 = get_remitente_by_id(db, 4)

    pyg = get_moneda_by_simbolo(db, "PYG")
    # usd = get_moneda_by_simbolo(db, "USD") # TODO
    # brl = get_moneda_by_simbolo(db, "BRL")
    # arp = get_moneda_by_simbolo(db, "ARP")

    trigo = get_producto_by_descripcion(db, "Trigo en granos")
    soja = get_producto_by_descripcion(db, "Soja en granos")
    fertilizante = get_producto_by_descripcion(db, "Fertilizante a Granel")
    canola = get_producto_by_descripcion(db, "Canola en granos")

    efectivo = get_tipo_anticipo_by_descripcion(db, "EFECTIVO")
    tipo_insumo = get_tipo_anticipo_by_descripcion(db, "INSUMOS")

    combustible = get_tipo_insumo_by_descripcion(db, "COMBUSTIBLE")
    lubricantes = get_tipo_insumo_by_descripcion(db, "LUBRICANTES")

    seca = get_tipo_carga_by_descripcion(db, "SECA")
    liquida = get_tipo_carga_by_descripcion(db, "LÍQUIDA")

    peaje = get_tipo_concepto_complemento_by_descripcion(db, "Peaje")
    expurgo = get_tipo_concepto_complemento_by_descripcion(db, "Expurgo")

    sistema = get_tipo_concepto_descuento_by_descripcion(db, "Sistema")
    seguro = get_tipo_concepto_descuento_by_descripcion(db, "Seguro")

    # toneladas = get_unidad_by_descripcion(db, "Toneladas")  # TODO
    kilogramos = get_unidad_by_descripcion(db, "Kilogramos")
    # litros = get_unidad_by_descripcion(db, "Litros")  # TODO

    if (
        gestor_carga_id
        and destino3
        and destino5
        and destino9
        and destino11
        and origen2
        and origen4
        and origen8
        and origen12
        and remitente1
        and remitente2
        and remitente3
        and remitente4
        and pyg
        # and usd
        # and brl
        # and arp
        and trigo
        and soja
        and fertilizante
        and canola
        and efectivo
        and tipo_insumo
        and combustible
        and lubricantes
        and seca
        and liquida
        and peaje
        and expurgo
        and sistema
        and seguro
        and kilogramos
        # and toneladas
        # and litros
    ):
        destino3_contacto: CentroOperativoContactoGestorCarga = destino3.contactos[0]
        destino5_contacto: CentroOperativoContactoGestorCarga = destino5.contactos[0]
        destino9_contacto: CentroOperativoContactoGestorCarga = destino9.contactos[0]
        destino11_contacto: CentroOperativoContactoGestorCarga = destino11.contactos[0]

        origen2_contacto: CentroOperativoContactoGestorCarga = origen2.contactos[0]
        origen4_contacto: CentroOperativoContactoGestorCarga = origen4.contactos[0]
        origen8_contacto: CentroOperativoContactoGestorCarga = origen8.contactos[0]
        origen12_contacto: CentroOperativoContactoGestorCarga = origen12.contactos[0]

        remitente1_contacto: RemitenteContactoGestorCarga = remitente1.contactos[0]
        remitente2_contacto: RemitenteContactoGestorCarga = remitente2.contactos[0]
        remitente3_contacto: RemitenteContactoGestorCarga = remitente3.contactos[0]
        remitente4_contacto: RemitenteContactoGestorCarga = remitente4.contactos[0]

        flete1 = get_flete_by_id(db, 1)
        flete2 = get_flete_by_id(db, 2)
        flete3 = get_flete_by_id(db, 3)
        flete4 = get_flete_by_id(db, 4)

        if not flete1:
            create_flete(
                db,
                FleteForm(
                    remitente_id=remitente1.id,
                    producto_id=trigo.id,
                    tipo_carga_id=seca.id,
                    numero_lote="1000000",
                    publicado=True,
                    es_subasta=False,
                    # INICIO Tramo de Fletes
                    origen_id=origen2.id,
                    origen_indicacion="Origen Indicaciones",
                    destino_id=destino3.id,
                    destino_indicacion="Destino Indicaciones",
                    distancia=Decimal(500),
                    # FIN Tramo de Fletes
                    # INICIO Cantidad y Flete
                    condicion_cantidad=Decimal(100000),
                    # inicio - Condiciones para el Gestor de Carga
                    condicion_gestor_carga_moneda_id=pyg.id,
                    condicion_gestor_carga_tarifa=Decimal(100),
                    condicion_gestor_carga_unidad_id=kilogramos.id,
                    # fin - Condiciones para el Gestor de Carga
                    # inicio - Condiciones para el Propietario
                    condicion_propietario_moneda_id=pyg.id,
                    condicion_propietario_tarifa=Decimal(80),
                    condicion_propietario_unidad_id=kilogramos.id,
                    # fin - Condiciones para el Propietario
                    # FIN Cantidad y Flete
                    # INICIO Mermas de Fletes
                    # inicio - Mermas para el Gestor de Carga
                    merma_gestor_carga_valor=Decimal(1000),
                    merma_gestor_carga_moneda_id=pyg.id,
                    merma_gestor_carga_unidad_id=kilogramos.id,
                    merma_gestor_carga_es_porcentual=False,
                    merma_gestor_carga_tolerancia=Decimal(100),
                    # fin - Mermas para el Gestor de Carga
                    # inicio - Mermas para el Propietario
                    merma_propietario_valor=Decimal(1500),
                    merma_propietario_moneda_id=pyg.id,
                    merma_propietario_unidad_id=kilogramos.id,
                    merma_propietario_es_porcentual=False,
                    merma_propietario_tolerancia=Decimal(50),
                    # fin - Mermas para el Propietario
                    # FIN Mermas de Fletes
                    # INICIO Emisión de Órdenes
                    emision_orden_texto_legal="Emisión de Órdenes - Texto Legal",
                    emision_orden_detalle="Emisión de Órdenes - Detalle",
                    destinatarios=[
                        FleteDestinatario(
                            id=destino3_contacto.id,
                            tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                            email=destino3_contacto.contacto_email,
                            nombre=f"{destino3_contacto.contacto_nombre} {destino3_contacto.contacto_apellido}",  # noqa: B950
                        ),
                        FleteDestinatario(
                            id=origen2_contacto.id,
                            tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                            email=origen2_contacto.contacto_email,
                            nombre=f"{origen2_contacto.contacto_nombre} {origen2_contacto.contacto_apellido}",  # noqa: B950
                        ),
                        FleteDestinatario(
                            id=remitente1_contacto.id,
                            tipo_destinatario=FleteDestinatarioEnum.REMITENTE,
                            email=remitente1_contacto.contacto_email,
                            nombre=f"{remitente1_contacto.contacto_nombre} {remitente1_contacto.contacto_apellido}",  # noqa: B950
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
                            propietario_monto=Decimal(5000),
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a pagar al Propietario
                            # INICIO Monto a cobrar al Remitente
                            remitente_monto=Decimal(5000),
                            remitente_moneda_id=pyg.id,
                        ),
                        FleteComplementoForm(
                            concepto_id=expurgo.id,
                            detalle="Flete Complemento Detalle",
                            habilitar_cobro_remitente=True,
                            anticipado=True,
                            # INICIO Monto a pagar al Propietario
                            propietario_monto=Decimal(10000),
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a pagar al Propietario
                            # INICIO Monto a cobrar al Remitente
                            remitente_monto=Decimal(12000),
                            remitente_moneda_id=pyg.id,
                        ),
                    ],
                    descuentos=[
                        FleteDescuentoForm(
                            concepto_id=sistema.id,
                            detalle="Flete Descuento Detalle",
                            habilitar_pago_proveedor=True,
                            anticipado=True,
                            # INICIO Monto a cobrar al Propietario
                            propietario_monto=Decimal(1000),
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a cobrar al Propietario
                            # INICIO Monto a pagar al Proveedor
                            proveedor_monto=Decimal(900),
                            proveedor_moneda_id=pyg.id,
                            proveedor_id=2,
                        ),
                        FleteDescuentoForm(
                            concepto_id=seguro.id,
                            detalle="Flete Descuento Detalle",
                            habilitar_pago_proveedor=True,
                            anticipado=False,
                            # INICIO Monto a cobrar al Propietario
                            propietario_monto=Decimal(1000),
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a cobrar al Propietario
                            # INICIO Monto a pagar al Proveedor
                            proveedor_monto=Decimal(1000),
                            proveedor_moneda_id=pyg.id,
                            proveedor_id=3,
                        ),
                    ],
                ),
                gestor_carga_id,
                modified_by,
            )

        if not flete2:
            create_flete(
                db,
                FleteForm(
                    remitente_id=remitente2.id,
                    producto_id=soja.id,
                    tipo_carga_id=liquida.id,
                    numero_lote="2000000",
                    publicado=True,
                    es_subasta=True,
                    # INICIO Tramo de Fletes
                    origen_id=origen4.id,
                    origen_indicacion="Origen Indicaciones",
                    destino_id=destino5.id,
                    destino_indicacion="Destino Indicaciones",
                    distancia=Decimal(500),
                    # FIN Tramo de Fletes
                    # INICIO Cantidad y Flete
                    condicion_cantidad=Decimal(50000),
                    # inicio - Condiciones para el Gestor de Carga
                    # condicion_gestor_carga_moneda_id=usd.id,
                    condicion_gestor_carga_moneda_id=pyg.id,
                    condicion_gestor_carga_tarifa=Decimal(0.2),
                    condicion_gestor_carga_unidad_id=kilogramos.id,
                    # fin - Condiciones para el Gestor de Carga
                    # inicio - Condiciones para el Propietario
                    # condicion_propietario_moneda_id=usd.id,
                    condicion_propietario_moneda_id=pyg.id,
                    condicion_propietario_tarifa=Decimal(0.1),
                    condicion_propietario_unidad_id=kilogramos.id,
                    # fin - Condiciones para el Propietario
                    # FIN Cantidad y Flete
                    # INICIO Mermas de Fletes
                    # inicio - Mermas para el Gestor de Carga
                    merma_gestor_carga_valor=Decimal(0.2),
                    # merma_gestor_carga_moneda_id=usd.id,
                    merma_gestor_carga_moneda_id=pyg.id,
                    merma_gestor_carga_unidad_id=kilogramos.id,
                    merma_gestor_carga_es_porcentual=True,
                    merma_gestor_carga_tolerancia=Decimal(12),
                    # fin - Mermas para el Gestor de Carga
                    # inicio - Mermas para el Propietario
                    merma_propietario_valor=Decimal(0.3),
                    # merma_propietario_moneda_id=usd.id,
                    merma_propietario_moneda_id=pyg.id,
                    merma_propietario_unidad_id=kilogramos.id,
                    merma_propietario_es_porcentual=True,
                    merma_propietario_tolerancia=Decimal(10),
                    # fin - Mermas para el Propietario
                    # FIN Mermas de Fletes
                    # INICIO Emisión de Órdenes
                    emision_orden_texto_legal="Emisión de Órdenes - Texto Legal",
                    emision_orden_detalle="Emisión de Órdenes - Detalle",
                    destinatarios=[
                        FleteDestinatario(
                            id=destino5_contacto.id,
                            tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                            email=destino5_contacto.contacto_email,
                            nombre=f"{destino5_contacto.contacto_nombre} {destino5_contacto.contacto_apellido}",  # noqa: B950
                        ),
                        FleteDestinatario(
                            id=origen4_contacto.id,
                            tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                            email=origen4_contacto.contacto_email,
                            nombre=f"{origen4_contacto.contacto_nombre} {origen4_contacto.contacto_apellido}",  # noqa: B950
                        ),
                        FleteDestinatario(
                            id=remitente2_contacto.id,
                            tipo_destinatario=FleteDestinatarioEnum.REMITENTE,
                            email=remitente2_contacto.contacto_email,
                            nombre=f"{remitente2_contacto.contacto_nombre} {remitente2_contacto.contacto_apellido}",  # noqa: B950
                        ),
                    ],
                    # FIN Emisión de Órdenes
                    vigencia_anticipos=datetime(2022, 8, 1).isoformat(),
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
                            propietario_monto=Decimal(7),
                            # propietario_moneda_id=usd.id,
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a pagar al Propietario
                            # INICIO Monto a cobrar al Remitente
                            remitente_monto=Decimal(7.1),
                            # remitente_moneda_id=usd.id,
                            remitente_moneda_id=pyg.id,
                        ),
                        FleteComplementoForm(
                            concepto_id=expurgo.id,
                            detalle="Flete Complemento Detalle",
                            habilitar_cobro_remitente=True,
                            anticipado=True,
                            # INICIO Monto a pagar al Propietario
                            propietario_monto=Decimal(1),
                            # propietario_moneda_id=usd.id,
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a pagar al Propietario
                            # INICIO Monto a cobrar al Remitente
                            remitente_monto=Decimal(1.2),
                            # remitente_moneda_id=usd.id,
                            remitente_moneda_id=pyg.id,
                        ),
                    ],
                    descuentos=[
                        FleteDescuentoForm(
                            concepto_id=sistema.id,
                            detalle="Flete Descuento Detalle",
                            habilitar_pago_proveedor=True,
                            anticipado=True,
                            # INICIO Monto a cobrar al Propietario
                            propietario_monto=Decimal(10),
                            # propietario_moneda_id=usd.id,
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a cobrar al Propietario
                            # INICIO Monto a pagar al Proveedor
                            proveedor_monto=Decimal(11),
                            # proveedor_moneda_id=usd.id,
                            proveedor_moneda_id=pyg.id,
                            proveedor_id=4,
                        ),
                        FleteDescuentoForm(
                            concepto_id=seguro.id,
                            detalle="Flete Descuento Detalle",
                            habilitar_pago_proveedor=True,
                            anticipado=True,
                            # INICIO Monto a cobrar al Propietario
                            propietario_monto=Decimal(21),
                            # propietario_moneda_id=usd.id,
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a cobrar al Propietario
                            # INICIO Monto a pagar al Proveedor
                            proveedor_monto=Decimal(22),
                            # proveedor_moneda_id=usd.id,
                            proveedor_moneda_id=pyg.id,
                            proveedor_id=5,
                        ),
                    ],
                ),
                gestor_carga_id,
                modified_by,
            )

        if not flete3:
            create_flete(
                db,
                FleteForm(
                    remitente_id=remitente3.id,
                    producto_id=fertilizante.id,
                    tipo_carga_id=seca.id,
                    numero_lote="3000000",
                    publicado=True,
                    es_subasta=False,
                    # INICIO Tramo de Fletes
                    origen_id=origen8.id,
                    origen_indicacion="Origen Indicaciones",
                    destino_id=destino11.id,
                    destino_indicacion="Destino Indicaciones",
                    distancia=Decimal(500),
                    # FIN Tramo de Fletes
                    # INICIO Cantidad y Flete
                    condicion_cantidad=Decimal(100000),
                    # inicio - Condiciones para el Gestor de Carga
                    # condicion_gestor_carga_moneda_id=brl.id,
                    condicion_gestor_carga_moneda_id=pyg.id,
                    condicion_gestor_carga_tarifa=Decimal(12),
                    # condicion_gestor_carga_unidad_id=toneladas.id,
                    condicion_gestor_carga_unidad_id=kilogramos.id,
                    # fin - Condiciones para el Gestor de Carga
                    # inicio - Condiciones para el Propietario
                    # condicion_propietario_moneda_id=brl.id,
                    condicion_propietario_moneda_id=pyg.id,
                    condicion_propietario_tarifa=Decimal(10),
                    # condicion_propietario_unidad_id=toneladas.id,
                    condicion_propietario_unidad_id=kilogramos.id,
                    # fin - Condiciones para el Propietario
                    # FIN Cantidad y Flete
                    # INICIO Mermas de Fletes
                    # inicio - Mermas para el Gestor de Carga
                    merma_gestor_carga_valor=Decimal(50),
                    # merma_gestor_carga_moneda_id=brl.id,
                    merma_gestor_carga_moneda_id=pyg.id,
                    # merma_gestor_carga_unidad_id=toneladas.id,
                    merma_gestor_carga_unidad_id=kilogramos.id,
                    merma_gestor_carga_es_porcentual=False,
                    merma_gestor_carga_tolerancia=Decimal(100),
                    # fin - Mermas para el Gestor de Carga
                    # inicio - Mermas para el Propietario
                    merma_propietario_valor=Decimal(60),
                    # merma_propietario_moneda_id=brl.id,
                    merma_propietario_moneda_id=pyg.id,
                    # merma_propietario_unidad_id=toneladas.id,
                    merma_propietario_unidad_id=kilogramos.id,
                    merma_propietario_es_porcentual=False,
                    merma_propietario_tolerancia=Decimal(90),
                    # fin - Mermas para el Propietario
                    # FIN Mermas de Fletes
                    # INICIO Emisión de Órdenes
                    emision_orden_texto_legal="Emisión de Órdenes - Texto Legal",
                    emision_orden_detalle="Emisión de Órdenes - Detalle",
                    destinatarios=[
                        FleteDestinatario(
                            id=destino11_contacto.id,
                            tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                            email=destino11_contacto.contacto_email,
                            nombre=f"{destino11_contacto.contacto_nombre} {destino11_contacto.contacto_apellido}",  # noqa: B950
                        ),
                        FleteDestinatario(
                            id=origen8_contacto.id,
                            tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                            email=origen8_contacto.contacto_email,
                            nombre=f"{origen8_contacto.contacto_nombre} {origen8_contacto.contacto_apellido}",  # noqa: B950
                        ),
                        FleteDestinatario(
                            id=remitente3_contacto.id,
                            tipo_destinatario=FleteDestinatarioEnum.REMITENTE,
                            email=remitente3_contacto.contacto_email,
                            nombre=f"{remitente3_contacto.contacto_nombre} {remitente3_contacto.contacto_apellido}",  # noqa: B950
                        ),
                    ],
                    # FIN Emisión de Órdenes
                    vigencia_anticipos=datetime(2022, 9, 1).isoformat(),
                    anticipos=[
                        FleteAnticipoForm(
                            tipo_id=efectivo.id,
                            tipo_descripcion=efectivo.descripcion,
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
                            concepto_id=expurgo.id,
                            detalle="Flete Complemento Detalle",
                            habilitar_cobro_remitente=True,
                            anticipado=True,
                            # INICIO Monto a pagar al Propietario
                            propietario_monto=Decimal(100),
                            # propietario_moneda_id=brl.id,
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a pagar al Propietario
                            # INICIO Monto a cobrar al Remitente
                            remitente_monto=Decimal(120),
                            # remitente_moneda_id=brl.id,
                            remitente_moneda_id=pyg.id,
                        ),
                    ],
                    descuentos=[
                        FleteDescuentoForm(
                            concepto_id=sistema.id,
                            detalle="Flete Descuento Detalle",
                            habilitar_pago_proveedor=True,
                            anticipado=False,
                            # INICIO Monto a cobrar al Propietario
                            propietario_monto=Decimal(100),
                            # propietario_moneda_id=brl.id,
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a cobrar al Propietario
                            # INICIO Monto a pagar al Proveedor
                            proveedor_monto=Decimal(100),
                            # proveedor_moneda_id=brl.id,
                            proveedor_moneda_id=pyg.id,
                            proveedor_id=6,
                        ),
                    ],
                ),
                gestor_carga_id,
                modified_by,
            )

        if not flete4:
            create_flete(
                db,
                FleteForm(
                    remitente_id=remitente4.id,
                    producto_id=canola.id,
                    tipo_carga_id=liquida.id,
                    numero_lote="4000000",
                    publicado=True,
                    es_subasta=False,
                    # INICIO Tramo de Fletes
                    origen_id=origen12.id,
                    origen_indicacion="Origen Indicaciones",
                    destino_id=destino9.id,
                    destino_indicacion="Destino Indicaciones",
                    distancia=Decimal(500),
                    # FIN Tramo de Fletes
                    # INICIO Cantidad y Flete
                    condicion_cantidad=Decimal(100000),
                    # inicio - Condiciones para el Gestor de Carga
                    # condicion_gestor_carga_moneda_id=arp.id,
                    condicion_gestor_carga_moneda_id=pyg.id,
                    condicion_gestor_carga_tarifa=Decimal(55),
                    # condicion_gestor_carga_unidad_id=toneladas.id,
                    condicion_gestor_carga_unidad_id=kilogramos.id,
                    # fin - Condiciones para el Gestor de Carga
                    # inicio - Condiciones para el Propietario
                    # condicion_propietario_moneda_id=arp.id,
                    condicion_propietario_moneda_id=pyg.id,
                    condicion_propietario_tarifa=Decimal(50),
                    # condicion_propietario_unidad_id=toneladas.id,
                    condicion_propietario_unidad_id=kilogramos.id,
                    # fin - Condiciones para el Propietario
                    # FIN Cantidad y Flete
                    # INICIO Mermas de Fletes
                    # inicio - Mermas para el Gestor de Carga
                    merma_gestor_carga_valor=Decimal(100),
                    # merma_gestor_carga_moneda_id=arp.id,
                    merma_gestor_carga_moneda_id=pyg.id,
                    # merma_gestor_carga_unidad_id=toneladas.id,
                    merma_gestor_carga_unidad_id=kilogramos.id,
                    merma_gestor_carga_es_porcentual=True,
                    merma_gestor_carga_tolerancia=Decimal(15),
                    # fin - Mermas para el Gestor de Carga
                    # inicio - Mermas para el Propietario
                    merma_propietario_valor=Decimal(110),
                    # merma_propietario_moneda_id=arp.id,
                    merma_propietario_moneda_id=pyg.id,
                    # merma_propietario_unidad_id=toneladas.id,
                    merma_propietario_unidad_id=kilogramos.id,
                    merma_propietario_es_porcentual=True,
                    merma_propietario_tolerancia=Decimal(12),
                    # fin - Mermas para el Propietario
                    # FIN Mermas de Fletes
                    # INICIO Emisión de Órdenes
                    emision_orden_texto_legal="Emisión de Órdenes - Texto Legal",
                    emision_orden_detalle="Emisión de Órdenes - Detalle",
                    destinatarios=[
                        FleteDestinatario(
                            id=destino9_contacto.id,
                            tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                            email=destino9_contacto.contacto_email,
                            nombre=f"{destino9_contacto.contacto_nombre} {destino9_contacto.contacto_apellido}",  # noqa: B950
                        ),
                        FleteDestinatario(
                            id=origen12_contacto.id,
                            tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                            email=origen12_contacto.contacto_email,
                            nombre=f"{origen12_contacto.contacto_nombre} {origen12_contacto.contacto_apellido}",  # noqa: B950
                        ),
                        FleteDestinatario(
                            id=remitente4_contacto.id,
                            tipo_destinatario=FleteDestinatarioEnum.REMITENTE,
                            email=remitente4_contacto.contacto_email,
                            nombre=f"{remitente4_contacto.contacto_nombre} {remitente4_contacto.contacto_apellido}",  # noqa: B950
                        ),
                    ],
                    # FIN Emisión de Órdenes
                    vigencia_anticipos=datetime(2022, 12, 1).isoformat(),
                    anticipos=[
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
                            # propietario_moneda_id=arp.id,
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a pagar al Propietario
                            # INICIO Monto a cobrar al Remitente
                            remitente_monto=Decimal(100),
                            # remitente_moneda_id=arp.id,
                            remitente_moneda_id=pyg.id,
                        ),
                    ],
                    descuentos=[
                        FleteDescuentoForm(
                            concepto_id=sistema.id,
                            detalle="Flete Descuento Detalle",
                            habilitar_pago_proveedor=True,
                            anticipado=True,
                            # INICIO Monto a cobrar al Propietario
                            propietario_monto=Decimal(100),
                            # propietario_moneda_id=arp.id,
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a cobrar al Propietario
                            # INICIO Monto a pagar al Proveedor
                            proveedor_monto=Decimal(100),
                            # proveedor_moneda_id=arp.id,
                            proveedor_moneda_id=pyg.id,
                            proveedor_id=7,
                        ),
                        FleteDescuentoForm(
                            concepto_id=seguro.id,
                            detalle="Flete Descuento Detalle",
                            habilitar_pago_proveedor=True,
                            anticipado=True,
                            # INICIO Monto a cobrar al Propietario
                            propietario_monto=Decimal(100),
                            # propietario_moneda_id=arp.id,
                            propietario_moneda_id=pyg.id,
                            # FIN Monto a cobrar al Propietario
                            # INICIO Monto a pagar al Proveedor
                            proveedor_monto=Decimal(100),
                            # proveedor_moneda_id=arp.id,
                            proveedor_moneda_id=pyg.id,
                            proveedor_id=8,
                        ),
                    ],
                ),
                gestor_carga_id,
                modified_by,
            )
