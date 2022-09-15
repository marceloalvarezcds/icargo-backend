from http import HTTPStatus
from typing import Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class ApiResponseData(GenericModel, Generic[T]):
    data: T
    status_code: int = HTTPStatus.OK
    detail: str = ""

    def __init__(
        self, data: T, status_code: int = HTTPStatus.OK, detail: str = ""
    ) -> None:
        super().__init__(data=data, status_code=status_code, detail=detail)
