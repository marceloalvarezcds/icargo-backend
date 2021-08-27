from sqlalchemy import Enum, Column, Integer, String, Float, Boolean
from app.db import Base
from sqlalchemy.orm import relationship, backref

from app.models.product_status import ProductStatus
from app.models.product_tag import association_table


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    price = Column(Float)
    brand = Column(String)
    active = Column(Boolean, nullable=False, default=True)
    status = Column(Enum(ProductStatus), nullable=False)

    details = relationship('ProductDetail', lazy='select',
                           backref=backref('product_detail', lazy='joined'))

    tags = relationship(
        "Tag",
        secondary=association_table,
        back_populates="products")

    def __init__(self, name, price, brand, status, details=[]):
        self.name = name
        self.price = price
        self.brand = brand
        self.status = status
        self.details = details
