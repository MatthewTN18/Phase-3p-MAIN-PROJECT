from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DB_NAME = "cinema_kiosk"
DB_USER = "tt"
DB_PASSWORD = "mypassword"
DB_HOST = "172.22.135.239"
DB_PORT = "5432"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)