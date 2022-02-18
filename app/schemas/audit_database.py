from typing import Any, Dict

from pydantic import BaseModel
from simplejson import loads

from .date_model import Date


class AuditDatabase(BaseModel):
    id: int
    row_id: int
    table_name: str
    action: str
    user: str
    date_hour: Date
    row: Dict

    class Config:
        orm_mode = True
        use_enum_values = True

    @classmethod
    def from_orm(cls, obj: Any) -> "AuditDatabase":
        if hasattr(obj, "row"):
            obj.row = loads(obj.row)
        return super().from_orm(obj)
