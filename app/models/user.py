from sqlalchemy import Boolean, Column, Integer, String, Text, text  # type: ignore
from sqlalchemy.dialects.postgresql import TIMESTAMP  # type: ignore
from sqlalchemy.sql import func  # type: ignore

from app.database.base import Base


class User(Base):
    """
    Defines the user model
    """

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    username = Column(String(255), nullable=False, unique=True)
    surname = Column(String(255))
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    activation_code = Column(String(255), index=True)
    persist_code = Column(String(255))
    reset_password_code = Column(String(255), index=True)
    permissions = Column(Text)
    activated_at = Column(TIMESTAMP(precision=0), server_default=func.now())
    last_login = Column(TIMESTAMP(precision=0))
    is_activated = Column(Boolean, nullable=False, server_default=text("false"))
    is_guest = Column(Boolean, nullable=False, server_default=text("false"))
    is_superuser = Column(Boolean, nullable=False, server_default=text("false"))
    last_activity = Column(TIMESTAMP(precision=0))
    last_seen = Column(TIMESTAMP(precision=0))
    created_ip_address = Column(String(255))
    last_ip_address = Column(String(255))
