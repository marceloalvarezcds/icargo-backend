from typing import List

from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.cache import (
    exists_ciudades_in_cache,
    get_ciudades_in_cache,
    set_ciudades_in_cache,
)
from app.schemas import Ciudad


def get_ciudad_list(db: Session) -> List[Ciudad]:
    if exists_ciudades_in_cache():
        return get_ciudades_in_cache()
    ciudades = repositories.get_ciudad_list(db)
    lista = [Ciudad.from_orm(x) for x in ciudades]
    set_ciudades_in_cache(lista)
    return lista
