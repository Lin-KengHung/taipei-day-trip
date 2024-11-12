from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

class Attraction(Base):
    __tablename__ = "attraction"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    address = Column(Text, nullable=False)
    transport = Column(Text, nullable=False)
    mrt = Column(String(255), nullable=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

    images = relationship("Image", back_populates="attraction")
    bookings = relationship("Booking", back_populates="attraction")
    purchases = relationship("Purchase", back_populates="attraction")

    

class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    attraction_id = Column(Integer, ForeignKey("attraction.id"), nullable=False)

    attraction = relationship("Attraction", back_populates="images")
