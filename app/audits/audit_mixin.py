from datetime import date, datetime
from typing import Any

from simplejson import dumps
from sqlalchemy import Column, DateTime, String, text  # type: ignore
from sqlalchemy.orm import declarative_mixin  # type: ignore


def format_value_by_instance(value: Any, for_json=True):
    if for_json and (isinstance(value, datetime) or isinstance(value, date)):
        return value.isoformat()
    elif isinstance(value, list):
        return [format_value_by_instance(val, for_json) for val in value]
    elif isinstance(value, AuditMixin):
        return value.as_dict(for_json)
    else:
        return value


@declarative_mixin
class AuditMixin:
    __tablename__: str
    id: int

    created_by = Column(String(255), server_default="system")
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    modified_by = Column(String(255), server_default="system")
    modified_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    def as_dict(self, for_json=True):
        d = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            d[c.name] = format_value_by_instance(value, for_json)
        return d

    def for_json(self):
        return dumps(
            self.as_dict(), skipkeys=True, iterable_as_array=True, for_json=True
        )
