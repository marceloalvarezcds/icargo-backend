from sqlalchemy import Boolean, Column, Integer, String, JSON, BigInteger, ForeignKey
from app.db import Base

class Address(Base):
    __tablename__ = "address"

    id = Column(BigInteger, primary_key=True, index=True)
    address = Column(String, nullable=False)
    lat_lng = Column(JSON, default=lambda: {})
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    is_active = Column(Boolean, nullable=False)

    def __init__(self, address, lat_lng, user_id):
        self.address = address
        self.lat_lng = lat_lng
        self.user_id = user_id
        self.is_active = True
