from sqlalchemy.orm import Session  # type: ignore

from app.models import ComposicionJuridica
from app.repositories import get_composicion_juridica_by_nombre


def create_composicion_juridica(db: Session, nombre: str, nombre_corto: str):
    composicion_juridica = get_composicion_juridica_by_nombre(db, nombre)
    if composicion_juridica is None:
        composicion_juridica = ComposicionJuridica(
            nombre=nombre, nombre_corto=nombre_corto
        )
        db.add(composicion_juridica)
        db.commit()


def composicion_juridica_seeds(db: Session):
    create_composicion_juridica(db, nombre="Sociedad Anónima", nombre_corto="S.A.")
    create_composicion_juridica(
        db, nombre="Sociedad de Responsabilidad Limitada", nombre_corto="S.R.L."
    )
    create_composicion_juridica(
        db, nombre="Sociedad Anónima Comercial Industrial.", nombre_corto="S.A.C.I."
    )
