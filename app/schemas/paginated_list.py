from typing import Generic, List, Optional, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginatedList(GenericModel, Generic[T]):
    """
    Represent a list that is paginated.

    Includes the current page, the total results and the current page.
    """

    rows: List[T]
    query: Optional[str]
    page: int
    pageSize: int
    totalRecords: int
