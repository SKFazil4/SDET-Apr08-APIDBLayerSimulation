from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app_db.db.base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_name = Column(String(250), unique=True, nullable=False)
    price = Column(Integer, nullable=False)

    user = relationship("User", back_populates="orders")