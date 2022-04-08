from decimal import Decimal

from sqlalchemy.orm import Session  # type: ignore

from app.models import TipoIva
from app.repositories import get_pais_by_nombre_corto, get_tipo_iva_by_descripcion
from app.utils import number_format


def create_tipo_iva(db: Session, pais_nombre_corto: str, iva: Decimal):
    pais = get_pais_by_nombre_corto(db, pais_nombre_corto)
    if pais:
        descripcion = f"{pais.nombre_corto}= {number_format(iva)}%"
        tipo_iva = get_tipo_iva_by_descripcion(db, descripcion)
        if tipo_iva is None:
            tipo_iva = TipoIva(descripcion=descripcion, pais_id=pais.id, iva=iva)
            db.add(tipo_iva)
            db.commit()


def tipo_iva_seeds(db: Session):
    PY = "PY"
    AR = "AR"
    create_tipo_iva(db, PY, Decimal(10))
    create_tipo_iva(db, AR, Decimal(21))
