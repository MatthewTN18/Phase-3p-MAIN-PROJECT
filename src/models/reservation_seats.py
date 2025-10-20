from sqlalchemy import Column, Integer, Float, ForeignKey
from .orm_db import Base

class ReservationSeat(Base):
    __tablename__ = "reservation_seats"
    
    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer, ForeignKey('reservations.id'), nullable=False)
    seat_id = Column(Integer, ForeignKey('seats.id'), nullable=False)
    final_price = Column(Float, nullable=False)