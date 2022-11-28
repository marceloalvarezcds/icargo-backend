from typing import Dict, Optional

from diskcache import Cache  # type: ignore

from app.enums import PermisoAccionEnum, PermisoModeloEnum

permisos_cache = Cache("/app/cache/permisos")

PermisosDict = Dict[str, Optional[bool]]


def _get_user_permisos(
    user_id: int,
) -> PermisosDict:
    value: Optional[PermisosDict] = permisos_cache.get(user_id, None)
    if not value:
        return {}
    return value


def check_permiso_in_cache(
    user_id: int,
    accion: PermisoAccionEnum,
    modelo: PermisoModeloEnum,
) -> Optional[bool]:
    key = f"{accion.value}_{modelo.value}"
    permiso = _get_user_permisos(user_id)
    return permiso.get(key, None)


def get_permiso_in_cache(
    user_id: int,
    accion: PermisoAccionEnum,
    modelo: PermisoModeloEnum,
) -> bool:
    key = f"{accion.value}_{modelo.value}"
    permiso = _get_user_permisos(user_id)
    return permiso.get(key, False) is True


def set_permiso_in_cache(
    user_id: int, accion: PermisoAccionEnum, modelo: PermisoModeloEnum, value: bool
):
    key = f"{accion.value}_{modelo.value}"
    permiso = _get_user_permisos(user_id)
    permiso[key] = value
    permisos_cache.set(user_id, permiso, retry=True)


def reset_permiso_in_cache_by_user_id(user_id: int):
    permisos_cache.delete(user_id, retry=True)


def reset_all_permiso_in_cache():
    permisos_cache.clear(retry=True)
