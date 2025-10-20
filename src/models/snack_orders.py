from sqlalchemy import Column, Integer, Float, ForeignKey
from .orm_db import Base

class SnackOrder(Base):
    __tablename__ = "snack_orders"
    
    id = Column(Integer, primary_key=True)
    reservation_id = Column(Integer, ForeignKey('reservations.id'), nullable=False)
    snack_id = Column(Integer, ForeignKey('snacks.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)