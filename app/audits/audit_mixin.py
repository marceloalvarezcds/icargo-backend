from sqlalchemy import Column, String  # type: ignore
from sqlalchemy.orm import declarative_mixin  # type: ignore


@declarative_mixin
class AuditMixin:
    __tablename__: str
    id: int

    modified_by = Column(String)
