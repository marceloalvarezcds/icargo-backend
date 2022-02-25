from decimal import Decimal
from typing import Optional


def number_format(num: Optional[Decimal] = None) -> str:
    return (
        "{:,.2f}".format(num).replace(".", "#").replace(",", ".").replace("#", ",")
        if num
        else "0"
    )
