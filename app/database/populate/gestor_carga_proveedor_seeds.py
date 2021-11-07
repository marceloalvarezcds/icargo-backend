from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.models import GestorCarga, GestorCargaProveedor, Proveedor


def gestor_carga_proveedor_seeds(
    db: Session,
    proveedor: Proveedor,
    gestor_carga: GestorCarga,
    alias: str,
):
    try:
        db.add(
            GestorCargaProveedor(
                proveedor_id=proveedor.id,
                gestor_carga_id=gestor_carga.id,
                alias=alias,
            )
        )
        db.commit()
    except IntegrityError:
        db.rollback()
