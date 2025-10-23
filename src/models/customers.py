from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .orm_db import Base

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    phone = Column(String(20))
    created_at = Column(DateTime, default=func.now())