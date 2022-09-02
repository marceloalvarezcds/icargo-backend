from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.cache import (
    get_ciudades_in_cache,
    get_ciudades_total_records_in_cache,
    set_ciudades_in_cache,
    set_ciudades_total_records_in_cache,
)
from app.schemas import Ciudad, PaginatedList


def get_ciudad_list(
    db: Session, page: int, pageSize: int, query: str
) -> PaginatedList[Ciudad]:

    if query is not None and len(query) > 15:
        # Trim to 15 to prevent overflow
        query = query[:15]

    key = f"{page}__{pageSize}__{query}"
    count_key = f"{query}"

    result = get_ciudades_in_cache(key)
    if result is None:
        lista = repositories.get_ciudad_list(db, page, pageSize, query)
        result = [Ciudad.from_orm(x) for x in lista]
        set_ciudades_in_cache(key, result)
    count = get_ciudades_total_records_in_cache(count_key)
    if count is None:
        count = repositories.get_ciudad_count(db, query)
        set_ciudades_total_records_in_cache(count_key, count)

    return PaginatedList(
        rows=result, page=page, pageSize=pageSize, totalRecords=count, query=query
    )
