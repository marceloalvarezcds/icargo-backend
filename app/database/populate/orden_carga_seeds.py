from decimal import Decimal
from random import randrange
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore

from app.models import User
from app.repositories import (
    get_flete_list_by_gestor_carga_id,
    get_orden_carga_by_id,
    get_user_list_by_gestor_carga_id,
)
from app.schemas import OrdenCargaForm
from app.services import (
    create_orden_carga,
    get_camion_list_by_producto_id,
    get_semi_list_by_camion_id_and_producto_id,
)


def orden_carga_seeds(db: Session, user: Optional[User]):
    if user:
        fletes = get_flete_list_by_gestor_carga_id(db, user.gestor_carga_id)
        for flete in fletes:
            camiones = get_camion_list_by_producto_id(
                db, flete.producto_id, user.gestor_carga_id
            )
            for camion in camiones:
                semis = get_semi_list_by_camion_id_and_producto_id(
                    db, camion.id, flete.producto_id, user.gestor_carga_id
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
                        user,
                    )


def orden_carga_list_seeds(db: Session):
    orden_carga = get_orden_carga_by_id(db, 1)
    if not orden_carga:
        users1 = get_user_list_by_gestor_carga_id(db, 1)
        users2 = get_user_list_by_gestor_carga_id(db, 2)
        orden_carga_seeds(db, users1[0])
        orden_carga_seeds(db, users2[0])
