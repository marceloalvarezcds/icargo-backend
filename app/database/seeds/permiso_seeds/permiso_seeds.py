from sqlalchemy.orm import Session  # type: ignore

from app.enums import PermisoAccionEnum, PermisoModeloEnum
from app.models import Permiso
from app.repositories import get_permiso_by


def permiso_seeds(
    db: Session,
    accion: PermisoAccionEnum,
    modelo: PermisoModeloEnum,
    autorizado: bool = True,
    descripcion: str = None,
) -> Permiso:
    permiso = get_permiso_by(db, accion, modelo, autorizado)
    if not permiso:
        if not descripcion:
            descripcion = (
                f"{str(accion.value).capitalize()} {str(modelo.value).capitalize()}"
            )
        permiso = Permiso(
            modelo=modelo.value,
            accion=accion.value,
            autorizado=autorizado,
            descripcion=descripcion,
        )
        db.add(permiso)
        db.commit()
        db.refresh(permiso)
    return permiso
