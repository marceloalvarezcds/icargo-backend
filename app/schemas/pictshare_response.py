from typing import Optional

from pydantic import BaseModel


class PictShareResponse(BaseModel):
    status: str
    hash: Optional[str] = None
    url: Optional[str] = None
    filetype: str
    delete_code: Optional[str] = None
    delete_url: Optional[str] = None
