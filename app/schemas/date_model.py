from datetime import date, datetime

from pydantic import BaseModel


class Date(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, date):
            return v
        return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%fZ").date() if v else None
