from datetime import date, datetime

from pydantic import BaseModel


def validate(date_text: str, format: str) -> bool:
    try:
        datetime.strptime(date_text, format)
        return True
    except ValueError:
        return False


class Date(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, date):
            return v
        if validate(v, "%Y-%m-%dT%H:%M:%S.%fZ"):
            return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%fZ").date() if v else None
        if validate(v, "%Y-%m-%dT%H:%M:%S"):
            return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S").date() if v else None
        raise ValueError(f"La fecha {v} es inválida")
