from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy.orm import relationship, backref
from app.db import Base
from app.models.user_preference_category import UserPreferenceCategory

class PreferenceCategory(Base):
    __tablename__ = "preference_category"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False)
    user_preference_category = relationship(UserPreferenceCategory, backref=backref('preference_category', lazy=True))

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.is_active = True
