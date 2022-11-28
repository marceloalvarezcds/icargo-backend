from threading import Thread

from fastapi import Request
from sqlalchemy.orm import Session  # type: ignore
from starlette.middleware.base import BaseHTTPMiddleware

from app.audits.audit_request import AuditRequest
from app.dependencies import get_database_connection
from app.services import (
    get_auth_user_from_authorization_header,
    get_authorization_header,
)
from app.utils import get_host_from_request


def save_audit_request(ip: str, url: str, auth: str):
    user = get_auth_user_from_authorization_header(auth)
    username = user.username if user else ""
    db_conn = get_database_connection()
    db = Session(bind=db_conn)
    audit_request = AuditRequest(
        ip=ip,
        url=url,
        user=username,
    )
    db.add(audit_request)
    db.commit()
    db.close()


class AuditRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        ip = get_host_from_request(request)
        url = str(request.url)
        auth = get_authorization_header(request.headers)
        thread = Thread(target=save_audit_request, args=(ip, url, auth))
        thread.start()
        return response
