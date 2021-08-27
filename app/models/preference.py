from sqlalchemy import Column, String, BigInteger, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from app.db import Base
from app.models.user_preference import UserPreference

class Preference(Base):
    __tablename__ = "preference"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False)
    preference_category_id = Column(BigInteger, ForeignKey('preference_category.id'), nullable=False)
    user_preference = relationship(UserPreference, backref=backref('preference', lazy=True))

    def __init__(self, name, description, preference_category_id):
        self.name = name
        self.description = description
        self.preference_category_id = preference_category_id
        self.is_active = True
