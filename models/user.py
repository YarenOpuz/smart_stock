from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    office_address = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    image_path = Column(String, nullable=True)
    user_type = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    warehouses = relationship("Warehouse", back_populates="owner")