from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from .orm_db import Base

class Seat(Base):
    __tablename__ = "seats"
    
    id = Column(Integer, primary_key=True)
    screen_id = Column(Integer, ForeignKey('screens.id'), nullable=False)
    row_letter = Column(String(1), nullable=False)
    seat_number = Column(Integer, nullable=False)
    seat_type = Column(String(20), default='standard')  # standard, vip, handicap
    is_available = Column(Boolean, default=True)