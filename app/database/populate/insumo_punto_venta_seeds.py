from datetime import date
from decimal import Decimal
from random import randrange
from typing import Optional

from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import GestorCarga, Insumo, InsumoPuntoVenta, Moneda, PuntoVenta
from app.repositories import get_insumo_by_descripcion, get_moneda_by_simbolo

from .insumo_punto_venta_precio_seeds import insumo_punto_venta_precio_seeds


def insumo_punto_venta_seeds(
    db: Session,
    insumo: Optional[Insumo],
    punto_venta: PuntoVenta,
    moneda: Optional[Moneda],
    gestor_carga: GestorCarga,
):
    try:
        if insumo and moneda:
            insumo_punto_venta = InsumoPuntoVenta(
                insumo_id=insumo.id,
                punto_venta_id=punto_venta.id,
                moneda_id=moneda.id,
                gestor_carga_id=gestor_carga.id,
            )
            db.add(insumo_punto_venta)
            db.commit()
            return insumo_punto_venta
        return None
    except IntegrityError:
        db.rollback()
        return None


def gasoil_comun_punto_venta_seeds(
    db: Session,
    punto_venta: PuntoVenta,
    gestor_carga: GestorCarga,
):
    gasoil = get_insumo_by_descripcion(db, "GASOIL COMÚN")
    pyg = get_moneda_by_simbolo(db, "PYG")
    insumo_punto_venta_pyg = insumo_punto_venta_seeds(
        db, gasoil, punto_venta, pyg, gestor_carga
    )
    insumo_punto_venta_precio_seeds(
        db, insumo_punto_venta_pyg, Decimal(6460.24), date(2022, 1, 21)
    )
    insumo_punto_venta_precio_seeds(
        db, insumo_punto_venta_pyg, Decimal(6330.41), date(2022, 2, 17)
    )


def aceite_motor_punto_venta_seeds(
    db: Session,
    punto_venta: PuntoVenta,
    gestor_carga: GestorCarga,
):
    aceite = get_insumo_by_descripcion(db, "ACEITE DE MOTOR")
    pyg = get_moneda_by_simbolo(db, "PYG")
    insumo_punto_venta_pyg = insumo_punto_venta_seeds(
        db, aceite, punto_venta, pyg, gestor_carga
    )
    insumo_punto_venta_precio_seeds(
        db, insumo_punto_venta_pyg, Decimal(2307.14), date(2022, 1, 28)
    )
    insumo_punto_venta_precio_seeds(
        db, insumo_punto_venta_pyg, Decimal(2645.42), date(2022, 2, 10)
    )


def insumo_punto_venta_list_seeds(
    db: Session,
    punto_venta: PuntoVenta,
    gestor_carga: GestorCarga,
):
    op = randrange(3)
    if op == 0 or op == 2:
        gasoil_comun_punto_venta_seeds(db, punto_venta, gestor_carga)
    if op == 1 or op == 2:
        aceite_motor_punto_venta_seeds(db, punto_venta, gestor_carga)
