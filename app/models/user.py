from sqlalchemy import Boolean, Column, Integer, String, BigInteger
from sqlalchemy.orm import relationship, backref
from app.db import Base
from app.models.address import Address
from app.models.user_preference import UserPreference
from app.models.user_preference_category import UserPreferenceCategory
from app.models.billing_information import BillingInformation

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    ruc = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    token = Column(String)
    icargo_user = Column(Boolean, default = True)
    google_user = Column(Boolean, default=False)
    fb_user = Column(Boolean, default=False)
    apple_user = Column(Boolean, default=False)
    address = relationship(Address, backref=backref('users', lazy=True))
    billing_information = relationship(BillingInformation, backref=backref('users', lazy=True))
    user_preference = relationship(UserPreference, backref=backref('users', lazy=True))
    user_preference_category = relationship(UserPreferenceCategory, backref=backref('users', lazy=True))

    def __init__(self, email, password, name, last_name, phone_number, ruc, icargo_user, google_user, fb_user, apple_user):
        self.email = email
        self.password = password
        self.name = name
        self.last_name = last_name
        self.phone_number = phone_number
        self.ruc = ruc
        self.is_active = True
        self.icargo_user = icargo_user
        self.google_user = google_user
        self.fb_user = fb_user
        self.apple_user = apple_user
