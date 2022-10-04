from typing import Optional

from fastapi import Request


def get_host_from_request(request: Request) -> Optional[str]:
    return request.client.host if request.client else None
