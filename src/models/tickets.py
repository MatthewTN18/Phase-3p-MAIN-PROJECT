from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .orm_db import Base

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer, ForeignKey('reservations.id'), nullable=False)
    seat_id = Column(Integer, ForeignKey('seats.id'), nullable=False)
    ticket_number = Column(String(50), unique=True, nullable=False)
    status = Column(String(20), default='active')  # active, used, or cancelled
    created_at = Column(DateTime, default=func.now())