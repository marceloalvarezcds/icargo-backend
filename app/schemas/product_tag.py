from typing import List

from pydantic import BaseModel

from app.models import ProductStatus


class TagBase(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int


class TagAssignment(TagBase):
    product_id: int
    tag_id: int
