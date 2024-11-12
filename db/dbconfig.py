from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .base import Base
from dotenv import load_dotenv
import os
from model.attraction_model import Attraction, Image  
from model.user_model import User
from model.booking_model import Booking
from model.order_model import Purchase, Payment


load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"

engine = create_engine(DATABASE_URL, pool_size=15, max_overflow=5)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """創建資料表"""
    Base.metadata.create_all(bind=engine)