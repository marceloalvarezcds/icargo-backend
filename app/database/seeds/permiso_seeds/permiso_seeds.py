from sqlalchemy.orm import Session  # type: ignore

from app.enums import (
    PermisoAccionEnum,
    PermisoModeloEnum,
    PermisoModuloEnum,
    permisoModeloTitulo,
)
from app.models import Permiso
from app.repositories import get_permiso_by


def permiso_seeds(
    db: Session,
    accion: PermisoAccionEnum,
    modelo: PermisoModeloEnum,
    modulo: PermisoModuloEnum,
    descripcion: str = None,
    is_for_superuser: bool = False,
) -> Permiso:
    permiso = get_permiso_by(db, accion, modelo)
    if not permiso:
        modelo_titulo = permisoModeloTitulo[modelo.value]
        if not descripcion:
            descripcion = (
                f"{str(accion.value).capitalize()} {str(modelo_titulo).capitalize()}"
            )
        permiso = Permiso(
            modelo=modelo.value,
            accion=accion.value,
            modulo=modulo.value,
            modelo_titulo=modelo_titulo,
            descripcion=descripcion,
            is_for_superuser=is_for_superuser,
        )
        db.add(permiso)
        db.commit()
        db.refresh(permiso)
    return permiso
