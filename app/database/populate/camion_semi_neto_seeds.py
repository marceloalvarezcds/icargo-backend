from decimal import Decimal
from random import randrange
from typing import Optional

from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import Camion, CamionSemiNeto, GestorCarga, Producto, Semi
from app.repositories import (
    get_camion_by_id,
    get_producto_by_descripcion,
    get_semi_by_id,
)


def camion_semi_neto_seeds(
    db: Session,
    camion: Camion,
    semi: Optional[Semi],
    producto: Optional[Producto],
    gestor_carga: GestorCarga,
):
    try:
        if semi:
            neto = Decimal(camion.neto + semi.neto)
            camion_semi_neto = CamionSemiNeto(
                camion_id=camion.id,
                semi_id=semi.id,
                producto_id=producto.id if producto else None,
                gestor_carga_id=gestor_carga.id,
                neto=neto,
            )
            db.add(camion_semi_neto)
            db.commit()
            return camion_semi_neto
        return None
    except IntegrityError:
        db.rollback()
        return None


def camion_neto_seeds(db: Session, camion: Camion, gestor_carga: GestorCarga):
    trigo = get_producto_by_descripcion(db, "Trigo en granos")
    soja = get_producto_by_descripcion(db, "Soja en granos")
    fertilizante = get_producto_by_descripcion(db, "Fertilizante a Granel")
    canola = get_producto_by_descripcion(db, "Canola en granos")
    aceite = get_producto_by_descripcion(db, "Aceite de Soja")

    if trigo and soja and fertilizante and canola and aceite:
        productos = [trigo, soja, fertilizante, canola, aceite]
        cant_productos = len(productos)
        cantidad_semi = randrange(5)
        for _ in range(cantidad_semi):
            semi_id = 0
            if gestor_carga.id == 1:
                semi_id = randrange(1, 13)
            elif gestor_carga.id == 2:
                semi_id = randrange(13, 18)
            if semi_id != 0:
                semi = get_semi_by_id(db, semi_id)
                cantidad_producto = randrange(5)
                for _ in range(cantidad_producto):
                    producto_id = randrange(cant_productos + 1)
                    if producto_id == cant_productos:
                        producto = None
                    else:
                        producto = productos[producto_id]
                    camion_semi_neto_seeds(
                        db,
                        camion,
                        semi,
                        producto,
                        gestor_carga,
                    )


def camion_semi_producto_combination_seeds(db: Session, gestor_carga: GestorCarga):
    for camion_id in range(18):
        camion = get_camion_by_id(db, camion_id)
        if camion:
            camion_neto_seeds(db, camion, gestor_carga)
