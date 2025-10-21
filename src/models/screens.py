from sqlalchemy import Column, Integer, String
from .orm_db import Base

class Screen(Base):
    __tablename__ = "screens"
    
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False, unique=True)
    capacity = Column(Integer)
    screen_type = Column(String(50))  # IMAX, Standard, VIP