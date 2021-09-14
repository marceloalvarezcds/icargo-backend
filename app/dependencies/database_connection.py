from typing import Optional

from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.engine import Engine as Database  # type: ignore

from app import app
from app.config import SQLALCHEMY_DATABASE_URI

_db_conn: Optional[Database] = create_engine(
    SQLALCHEMY_DATABASE_URI, pool_pre_ping=True
)


@app.on_event("startup")
def open_database_connection_pools():
    global _db_conn
    if _db_conn is None:
        _db_conn = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)


@app.on_event("shutdown")
def close_database_connection_pools():
    global _db_conn
    if _db_conn:
        _db_conn.dispose()


def get_database_connection() -> Database:
    assert _db_conn is not None
    return _db_conn
