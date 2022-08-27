from typing import List

from diskcache import Cache  # type: ignore

from app.schemas import Ciudad

ciudades_cache = Cache("/app/cache/ciudades")


def get_ciudades_in_cache() -> List[Ciudad]:
    return ciudades_cache.get("ciudades", [])


def exists_ciudades_in_cache() -> bool:
    return ciudades_cache.get("ciudades", retry=True, default=None) is not None


def set_ciudades_in_cache(ciudades: List[Ciudad]):
    ciudades_cache.set("ciudades", ciudades, retry=True)


def reset_ciudades_in_cache():
    ciudades_cache.clear(retry=True)
