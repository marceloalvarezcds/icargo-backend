from sqlalchemy import Boolean, Column, BigInteger, ForeignKey
from app.db import Base

class UserPreference(Base):
    __tablename__ = "user_preference"

    id = Column(BigInteger, primary_key=True, index=True)
    is_active = Column(Boolean, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    preference_id = Column(BigInteger, ForeignKey('preference.id'), nullable=False)

    def __init__(self, user_id, preference_id):
        self.is_active = True
        self.user_id = user_id
        self.preference_id = preference_id
