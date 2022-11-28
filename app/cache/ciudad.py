from typing import List, Optional

from diskcache import Cache  # type: ignore

from app.schemas import Ciudad

ciudades_cache = Cache("ciudades")


def get_ciudades_in_cache(key: str) -> Optional[List[Ciudad]]:
    return ciudades_cache.get(f"ciudades_{key}", retry=True, default=None)


def set_ciudades_in_cache(key: str, ciudades: List[Ciudad]):
    ciudades_cache.set(f"ciudades_{key}", ciudades, retry=True)


def get_ciudades_total_records_in_cache(key: str) -> Optional[int]:
    return ciudades_cache.get(f"ciudades_count_{key}", retry=True, default=None)


def set_ciudades_total_records_in_cache(key: str, totalRecords: int):
    ciudades_cache.set(f"ciudades_count_{key}", totalRecords, retry=True)


def reset_ciudades_in_cache():
    ciudades_cache.clear(retry=True)
