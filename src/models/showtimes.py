from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .orm_db import Base

class Showtime(Base):
    __tablename__ = "showtimes"
    
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    screen_id = Column(Integer, ForeignKey('screens.id'), nullable=False)
    show_time = Column(String(8), nullable=False)  
    show_date = Column(String(10), nullable=False)  # YYYY-MM-DD format
    base_price = Column(Float, nullable=False)
    available_seats = Column(Integer)  