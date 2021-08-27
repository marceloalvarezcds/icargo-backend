from enum import auto
from fastapi_utils.enums import StrEnum


class ProductStatus(StrEnum):
    out_of_stock = auto()
    in_stock = auto()
    running_low = auto()

