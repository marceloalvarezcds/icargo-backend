from typing import List, TypeVar, Generic, Optional
from pydantic.generics import GenericModel

from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.cache import (
    get_ciudades_in_cache,
    get_ciudades_total_records_in_cache,
    set_ciudades_in_cache,
    set_ciudades_total_records_in_cache
)
from app.schemas import Ciudad

T = TypeVar("T")

class PaginatedList(GenericModel, Generic[T]):
    """
    Represent a list that is paginated.

    Includes the current page, the total results and the current page.

    TODO move to another file
    """
    rows: List[T]
    query: Optional[str]
    page: int
    pageSize: int
    totalRecords: int

    # def __init__(self, data: List[T], page: int, pageSize: int, totalRecords: int, query: str = None) -> None:
        # self.rows = data
        # self.query = query
        # self.page = page
        # self.pageSize = pageSize
        # self.totalRecords = totalRecords


def get_ciudad_list(db: Session, page: int, pageSize: int, query: str) -> PaginatedList[Ciudad]:

    if query is not None and len(query) > 15:
        # Trim to 15 to prevent overflow
        query = query[:15]

    key = f"{page}__{pageSize}__{query}"
    count_key = f"{query}"

    result = get_ciudades_in_cache(key)
    if result is None:
        result = repositories.get_ciudad_list(db, page, pageSize, query)
        result = [Ciudad.from_orm(x) for x in result]
        set_ciudades_in_cache(key, result)
    count = get_ciudades_total_records_in_cache(count_key)
    if count is None:
        count = repositories.get_ciudad_count(db, query)
        set_ciudades_total_records_in_cache(count_key, count)


    return PaginatedList(rows=result, page=page, pageSize=pageSize, totalRecords=count, query=query)



