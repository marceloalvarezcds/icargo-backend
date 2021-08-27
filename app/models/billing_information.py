from sqlalchemy import Boolean, Column, Integer, String, JSON, BigInteger, ForeignKey
from app.db import Base

class BillingInformation(Base):
    __tablename__ = "billing_information"

    id = Column(BigInteger, primary_key=True, index=True)
    razon_social = Column(String, nullable=True)
    ruc = Column(String, nullable=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    is_active = Column(Boolean, nullable=False)

    def __init__(self, razon_social, ruc, user_id):
        self.razon_social = razon_social
        self.ruc = ruc
        self.user_id = user_id
        self.is_active = True
