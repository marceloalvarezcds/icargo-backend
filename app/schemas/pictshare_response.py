from pydantic import BaseModel


class PictShareResponse(BaseModel):
    status: str
    hash: str
    url: str
    filetype: str
    delete_code: str
    delete_url: str
