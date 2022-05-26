from decimal import Decimal, InvalidOperation

from app.config import DECIMAL_PRECISION


class RoundedDecimal(Decimal):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            value = Decimal(v)
        except InvalidOperation:
            raise ValueError(f"El decimal {v} no es un válido")
        return round(value, DECIMAL_PRECISION)
