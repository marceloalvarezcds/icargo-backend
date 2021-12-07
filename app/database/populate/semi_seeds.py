from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.enums import EstadoEnum
from app.models import (
    Ciudad,
    Color,
    MarcaSemi,
    Propietario,
    Semi,
    SemiClasificacion,
    TipoCarga,
    TipoSemi,
)
from app.repositories import (
    get_ente_emisor_automotor_by_descripcion,
    get_ente_emisor_transporte_by_descripcion,
    get_semi_by,
)

d1000 = Decimal(1000)


def semi_seeds(
    db: Session,
    placa: str,
    propietario: Propietario,
    numero_chasis: str,
    # INICIO Habilitaciones del Camión
    # inicio - municipal
    ciudad_habilitacion_municipal: Ciudad,
    numero_habilitacion_municipal: str,
    # fin - municipal
    # inicio - transporte
    numero_habilitacion_transporte: str,
    # fin - transporte
    # inicio - automotor
    titular_habilitacion_automotor: str,
    # fin - automotor
    # FIN Habilitaciones del Camión
    # INICIO Detalles del Camión
    marca: Optional[MarcaSemi],
    clasificacion: Optional[SemiClasificacion],
    tipo: Optional[TipoSemi],
    tipo_carga: Optional[TipoCarga],
    color: Optional[Color],
    anho: int = 2020,
    # FIN Detalles del Camión
    # INICIO Capacidad del Camión
    bruto: Decimal = d1000,
    tara: Decimal = d1000,
    largo: Decimal = d1000,
    alto: Decimal = d1000,
    ancho: Decimal = d1000,
    volumen: Decimal = d1000,
    # FIN Capacidad del Camión
):
    ciudad_id = (
        ciudad_habilitacion_municipal.id if ciudad_habilitacion_municipal else None
    )
    ente_emisor_transporte = get_ente_emisor_transporte_by_descripcion(
        db, "Dirección Nacional de Transporte. DINATRAN"
    )
    ente_emisor_automotor = get_ente_emisor_automotor_by_descripcion(
        db, "Dirección del Registro de Automotores"
    )
    if (
        placa
        and ente_emisor_transporte
        and ente_emisor_automotor
        and titular_habilitacion_automotor
        and marca
        and clasificacion
        and tipo
        and tipo_carga
        and color
        and ciudad_id
    ):
        obj = get_semi_by(db, placa)
        if not obj:
            semi = Semi(
                placa=placa,
                propietario_id=propietario.id,
                numero_chasis=numero_chasis,
                foto=None,
                # INICIO Habilitaciones del Camión
                # inicio - municipal
                ciudad_habilitacion_municipal_id=ciudad_id,
                numero_habilitacion_municipal=numero_habilitacion_municipal,
                vencimiento_habilitacion_municipal=date(2023, 6, 1),
                foto_habilitacion_municipal_frente=None,
                foto_habilitacion_municipal_reverso=None,
                # fin - municipal
                # inicio - transporte
                ente_emisor_transporte_id=ente_emisor_transporte.id,
                numero_habilitacion_transporte=numero_habilitacion_transporte,
                vencimiento_habilitacion_transporte=date(2024, 6, 1),
                foto_habilitacion_transporte_frente=None,
                foto_habilitacion_transporte_reverso=None,
                # fin - transporte
                # inicio - automotor
                ente_emisor_automotor_id=ente_emisor_automotor.id,
                titular_habilitacion_automotor=titular_habilitacion_automotor,
                foto_habilitacion_automotor_frente=None,
                foto_habilitacion_automotor_reverso=None,
                # fin - automotor
                # FIN Habilitaciones del Camión
                # INICIO Detalles del Camión
                marca_id=marca.id,
                clasificacion_id=clasificacion.id,
                tipo_id=tipo.id,
                tipo_carga_id=tipo_carga.id,
                color_id=color.id,
                anho=anho,
                # FIN Detalles del Camión
                # INICIO Capacidad del Camión
                bruto=bruto,
                tara=tara,
                largo=largo,
                alto=alto,
                ancho=ancho,
                volumen=volumen,
                estado=EstadoEnum.ACTIVO.value,
            )
            db.add(semi)
            db.commit()
