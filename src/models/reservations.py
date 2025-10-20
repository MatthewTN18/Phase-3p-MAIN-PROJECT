from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .orm_db import Base

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True)
    showtime_id = Column(Integer, ForeignKey('showtimes.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default='confirmed')  # confirmed, cancelled, or completed
    payment_method = Column(String(50))
    created_at = Column(DateTime, default=func.now())