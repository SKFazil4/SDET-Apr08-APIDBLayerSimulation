from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app_db.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)