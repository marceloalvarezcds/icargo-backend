from sqlalchemy import Enum, Column, Integer, String, Float, Boolean, Table, ForeignKey, UniqueConstraint
from app.db import Base
from sqlalchemy.orm import relationship, backref

from app.models.product_status import ProductStatus

association_table = Table('product_tag', Base.metadata,
                          Column('product_id', Integer, ForeignKey('product.id')),
                          Column('tag_id', Integer, ForeignKey('tag.id')),
                          UniqueConstraint('product_id', 'tag_id', name='uix_1'))


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)
    products = relationship(
        "Product",
        secondary=association_table,
        back_populates="tags")

    def __init__(self, name, description):
        self.name = name
        self.description = description
