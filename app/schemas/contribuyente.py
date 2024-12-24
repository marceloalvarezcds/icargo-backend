from typing import Optional
from pydantic import BaseModel


class Contribuyente(BaseModel):
    id: int
    contribuyente: Optional[str]
    ruc: Optional[str]

    class Config:
        orm_mode = True
        use_enum_values = True
