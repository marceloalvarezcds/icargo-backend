from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app.enums import FleteDestinatarioEnum
from app.models import CentroOperativoContactoGestorCarga, RemitenteContactoGestorCarga
from app.repositories import (
    get_centro_operativo_by_id,
    get_moneda_by_simbolo,
    get_producto_by_descripcion,
    get_remitente_by_id,
    get_tipo_anticipo_by_descripcion,
    get_tipo_carga_by_descripcion,
    get_tipo_concepto_complemento_by_descripcion,
    get_tipo_concepto_descuento_by_descripcion,
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


def flete_seeds(db: Session, gestor_cuenta_id: Optional[int]):
    modified_by = "system"

    destino3 = get_centro_operativo_by_id(db, 3)
    origen2 = get_centro_operativo_by_id(db, 2)
    remitente1 = get_remitente_by_id(db, 1)

    pyg = get_moneda_by_simbolo(db, "PYG")
    usd = get_moneda_by_simbolo(db, "USD")
    brl = get_moneda_by_simbolo(db, "BRL")
    arp = get_moneda_by_simbolo(db, "ARP")
    bop = get_moneda_by_simbolo(db, "BOP")

    trigo = get_producto_by_descripcion(db, "Trigo")
    soja = get_producto_by_descripcion(db, "Soja")
    fertilizante = get_producto_by_descripcion(db, "Fertilizante a Granel")
    canola = get_producto_by_descripcion(db, "Canola")
    aceite = get_producto_by_descripcion(db, "Aceite de Soja")
    ganado = get_producto_by_descripcion(db, "Ganado")

    efectivo = get_tipo_anticipo_by_descripcion(db, "EFECTIVO")
    combustible = get_tipo_anticipo_by_descripcion(db, "COMBUSTIBLE")
    libricantes = get_tipo_anticipo_by_descripcion(db, "LUBRICANTES")
    otros = get_tipo_anticipo_by_descripcion(db, "OTROS")

    seca = get_tipo_carga_by_descripcion(db, "SECA")
    liquida = get_tipo_carga_by_descripcion(db, "LÍQUIDA")

    peaje = get_tipo_concepto_complemento_by_descripcion(db, "Peaje")
    expurgo = get_tipo_concepto_complemento_by_descripcion(db, "Expurgo")

    sistema = get_tipo_concepto_descuento_by_descripcion(db, "Sistema")
    seguro = get_tipo_concepto_descuento_by_descripcion(db, "Seguro")

    toneladas = get_unidad_by_descripcion(db, "Toneladas")
    kilogramos = get_unidad_by_descripcion(db, "Kilogramos")
    litros = get_unidad_by_descripcion(db, "Litros")

    if (
        gestor_cuenta_id
        and destino3
        and origen2
        and remitente1
        and pyg
        and usd
        and brl
        and arp
        and bop
        and trigo
        and soja
        and fertilizante
        and canola
        and aceite
        and ganado
        and efectivo
        and combustible
        and libricantes
        and otros
        and seca
        and liquida
        and peaje
        and expurgo
        and sistema
        and seguro
        and toneladas
        and kilogramos
        and litros
    ):
        destino3_contacto: CentroOperativoContactoGestorCarga = destino3.contactos[0]
        origen2_contacto: CentroOperativoContactoGestorCarga = origen2.contactos[0]
        remitente1_contacto: RemitenteContactoGestorCarga = remitente1.contactos[0]

        try:
            create_flete(
                db,
                FleteForm(
                    remitente_id=remitente1.id,
                    producto_id=trigo.id,
                    tipo_carga_id=seca.id,
                    numero_factura="001-001-1000000",
                    numero_crt="1000000",
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
                            id=destino3.id,
                            tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                            email=destino3_contacto.contacto_email,
                            nombre=f"{destino3_contacto.contacto_nombre} {destino3_contacto.contacto_apellido}",  # noqa: B950
                        ),
                        FleteDestinatario(
                            id=origen2.id,
                            tipo_destinatario=FleteDestinatarioEnum.CENTRO_OPERATIVO,
                            email=origen2_contacto.contacto_email,
                            nombre=f"{origen2_contacto.contacto_nombre} {origen2_contacto.contacto_apellido}",  # noqa: B950
                        ),
                        FleteDestinatario(
                            id=remitente1.id,
                            tipo_destinatario=FleteDestinatarioEnum.REMITENTE,
                            email=remitente1_contacto.contacto_email,
                            nombre=f"{remitente1_contacto.contacto_nombre} {remitente1_contacto.contacto_apellido}",  # noqa: B950
                        ),
                    ],
                    # FIN Emisión de Órdenes
                    vigencia_anticipos=datetime(2022, 6, 1).isoformat(),
                    anticipos=[
                        FleteAnticipoForm(tipo_id=efectivo.id, porcentaje=Decimal(10))
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
                        )
                    ],
                ),
                gestor_cuenta_id,
                modified_by,
            )
        except HTTPException:
            pass
