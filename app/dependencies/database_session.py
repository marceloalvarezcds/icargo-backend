from typing import AsyncIterable

from fastapi import Depends
from sqlalchemy.orm import Session  # type: ignore

from .database_connection import get_database_connection


async def get_db_session(
    db_conn=Depends(get_database_connection),  # noqa: B008
) -> AsyncIterable[Session]:
    session = Session(bind=db_conn, autocommit=False, autoflush=False)
    try:
        yield session
    finally:
        session.close()
