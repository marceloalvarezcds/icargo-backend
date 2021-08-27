from typing import List

from pydantic import BaseModel

from app.models import ProductStatus


class ProductDetailBase(BaseModel):
    description: str


class ProductDetail(ProductDetailBase):
    pass

    class Config:
        orm_mode = True
