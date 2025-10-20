from sqlalchemy import Column, Integer, String, Float, Boolean
from .orm_db import Base

class Snack(Base):
    __tablename__ = "snacks"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))  # popcorn, drinks, candy, nachos, soda
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    min_stock_level = Column(Integer, default=10)
    is_available = Column(Boolean, default=True)