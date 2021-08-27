from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from app.db import Base
from sqlalchemy.orm import relationship


class ProductDetail(Base):
    __tablename__ = "product_detail"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    product_id = Column(Integer, ForeignKey('product.id'), index=True, nullable=False)

    def __init__(self, description, product_id):
        self.description = description
        self.product_id = product_id

    def __repr__(self):
        return "<Detail %r>" % self.id
