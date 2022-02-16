from typing import List

from app.enums import PermisoAccionEnum, PermisoModeloEnum
from app.models import Permiso, User


def check_permiso(
    current_user: User,
    modelo: PermisoModeloEnum,
    accion: PermisoAccionEnum,
    autorizado: bool = True,
) -> bool:
    permisos: List[Permiso] = current_user.permisos
    for permiso in permisos:
        if (
            permiso.modelo == modelo.value
            and permiso.accion == accion.value
            and permiso.autorizado == autorizado
        ):
            return True
    return False
