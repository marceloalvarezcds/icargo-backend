from http import HTTPStatus
from typing import Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class ApiResponseData(GenericModel, Generic[T]):
    data: T
    code: int = HTTPStatus.OK
    message: str = ""

    def __init__(self, data: T, code: int = HTTPStatus.OK, message: str = "") -> None:
        super().__init__(data=data, code=code, message=message)
