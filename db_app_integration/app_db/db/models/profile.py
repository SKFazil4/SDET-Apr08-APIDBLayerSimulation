from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app_db.db.base import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    bio = Column(String(250))

    user = relationship("User", back_populates="profile")