from decimal import Decimal
from random import randrange
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.repositories import (
    get_camion_list_by_gestor_cuenta_id,
    get_flete_list_by_gestor_carga_id,
)
from app.schemas import OrdenCargaForm
from app.services import create_orden_carga, get_semi_list_by_camion_id_and_producto_id


def orden_carga_seeds(db: Session, gestor_carga_id: Optional[int]):
    modified_by = "system"
    if gestor_carga_id:
        fletes = get_flete_list_by_gestor_carga_id(db, gestor_carga_id)
        camiones = get_camion_list_by_gestor_cuenta_id(db, gestor_carga_id)
        for flete in fletes:
            for camion in camiones:
                semis = get_semi_list_by_camion_id_and_producto_id(
                    db, camion.id, flete.producto_id, gestor_carga_id
                )
                for semi in semis:
                    nro_comentario = flete.id + camion.id + semi.id
                    create_orden_carga(
                        db,
                        OrdenCargaForm(
                            camion_id=camion.id,
                            semi_id=semi.id,
                            flete_id=flete.id,
                            cantidad_nominada=Decimal(randrange(20000, 30000)),
                            comentarios=f"Comentario {nro_comentario}",
                        ),
                        gestor_carga_id,
                        modified_by,
                    )
