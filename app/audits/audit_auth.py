from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, String  # type: ignore

from app.database import Base


class AuditAuth(Base):
    """
    Defines the auth audit model
    """

    id = Column(BigInteger, primary_key=True)
    action = Column(String)
    user_id = Column(BigInteger)
    user = Column(String)
    date_hour = Column(DateTime, default=datetime.now)
    ip = Column(String)

    def __repr__(self) -> str:
        return f"<AuditAuth table_name={self.table_name}, action={self.action}>"
