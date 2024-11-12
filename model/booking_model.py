from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from db.base import Base
import datetime

class Booking(Base):
    __tablename__ = "booking"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, comment="Unique ID")
    attraction_id = Column(BigInteger, ForeignKey("attraction.id"), nullable=False, comment="Attraction ID for booking")
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False, unique=True, comment="User ID for booking")
    date = Column(String(10), nullable=False, comment="Date")
    time = Column(Enum("morning", "afternoon", name="time_enum"), nullable=False, comment="Time")
    price = Column(Enum("2000", "2500", name="price_enum"), nullable=False, comment="Price")
    created_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, comment="Created Time")

    # Relationships
    attraction = relationship("Attraction", back_populates="bookings")
    user = relationship("User", back_populates="booking")
