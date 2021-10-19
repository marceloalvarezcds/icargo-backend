from datetime import date, datetime

from simplejson import dumps
from sqlalchemy import Column, DateTime, String, text  # type: ignore
from sqlalchemy.orm import declarative_mixin  # type: ignore


@declarative_mixin
class AuditMixin:
    __tablename__: str
    id: int

    modified_by = Column(String(255), server_default="system")
    modified_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, datetime) or isinstance(value, date):
                d[c.name] = value.isoformat()
            else:
                d[c.name] = value
        return d

    def for_json(self):
        return dumps(
            self.as_dict(), skipkeys=True, iterable_as_array=True, for_json=True
        )
