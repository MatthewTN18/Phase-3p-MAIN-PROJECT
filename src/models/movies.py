from sqlalchemy import Column, Integer, String, Boolean
from .orm_db import Base

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    genre = Column(String(100))
    duration = Column(Integer)  # minutes
    is_active = Column(Boolean, default=True)