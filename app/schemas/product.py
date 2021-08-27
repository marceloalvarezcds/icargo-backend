from typing import List

from pydantic import BaseModel

from app.models import ProductStatus


class ProductBase(BaseModel):
    name: str
    price: float
    brand: str
    status: ProductStatus

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    details: List


class Product(ProductBase):
    id: int


class ProductFull(ProductBase):
    id: int
    active: bool
    details: List


class ProductDetail(BaseModel):
    product_id: int
    details: List
