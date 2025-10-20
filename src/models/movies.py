from sqlalchemy import Column, Integer, String, Boolean, Text
from .orm_db import Base

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    genre = Column(String(100))
    duration = Column(Integer)  # in minutes
    rating = Column(String(10))  # G, PG, PG-13, or R- rated
    description = Column(Text)
    is_active = Column(Boolean, default=True)