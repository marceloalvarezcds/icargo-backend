from types import FunctionType

from fastapi import FastAPI, Request
from sqlalchemy.orm import Session  # type: ignore
from starlette.middleware.base import BaseHTTPMiddleware

from app.audits.audit_request import AuditRequest
from app.constants import AUTHORIZATION
from app.services import get_user_from_request


class AuditRequestMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        *,
        database_connection_function: FunctionType,
    ):
        if database_connection_function is None:
            raise ValueError("Params database_connection_function is required")
        super().__init__(app)
        self.get_db_conn_func_tuple = (database_connection_function,)

    async def dispatch(self, request: Request, call_next):
        database_connection_function = self.get_db_conn_func_tuple[0]
        db_conn = database_connection_function()
        db = Session(bind=db_conn)
        user = None
        if AUTHORIZATION in request.headers:
            user = get_user_from_request(request, self.get_db_conn_func_tuple[0])
        audit_request = AuditRequest(
            ip=request.client.host,
            url=str(request.url),
            user=user.username if user else None,
        )
        db.add(audit_request)
        db.commit()
        db.close()
        response = await call_next(request)
        return response
