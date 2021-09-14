from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, String  # type: ignore
from sqlalchemy.dialects.postgresql import JSON  # type: ignore

from app.database import Base


class AuditDatabase(Base):
    """
    Defines the audit database model
    """

    id = Column(BigInteger, primary_key=True)
    row_id = Column(BigInteger)
    table_name = Column(String)
    action = Column(String)
    user = Column(String)
    date_hour = Column(DateTime, default=datetime.now)
    row = Column(JSON)

    def __repr__(self) -> str:
        return f"<AuditDatabase table_name={self.table_name}, action={self.action}>"
