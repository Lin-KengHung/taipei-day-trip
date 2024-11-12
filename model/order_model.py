from sqlalchemy import Column, String, BigInteger, ForeignKey, SmallInteger, DateTime, Enum, INTEGER
from sqlalchemy.orm import relationship
from db.base import Base
import datetime


class Purchase(Base):
    __tablename__ = "purchase"

    id = Column(String(9), primary_key=True, comment="Order number")
    prime = Column(String(255), nullable=False, comment="Tappay prime")
    attraction_id = Column(BigInteger, ForeignKey("attraction.id"), nullable=False, comment="Attraction ID for order attraction")
    date = Column(String(10), nullable=False, comment="Order date")
    time = Column(Enum("morning", "afternoon", name="time_enum"), nullable=False)
    price = Column(INTEGER, nullable=False) 
    name = Column(String(255), nullable=False, comment="Contact name")
    email = Column(String(255), nullable=False, comment="Contact email")
    phone = Column(String(15), nullable=False, comment="Contact phone")
    paid = Column(SmallInteger, nullable=False, comment="Order is paid or not")
    created_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, comment="Created time")

    # Relationship
    attraction = relationship("Attraction", back_populates="purchases")
    payments = relationship("Payment", back_populates="purchase")


class Payment(Base):
    __tablename__ = "payment"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="Unique ID")
    purchase_id = Column(String(9), ForeignKey("purchase.id"), nullable=False, comment="Order number")
    status = Column(SmallInteger, nullable=False, comment="Tappay payment status")
    msg = Column(String(255), nullable=False, comment="Tappay payment message")
    rec_trade_id = Column(String(255), nullable=False, comment="Tappay rec_trade_id")
    created_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, comment="Created time")

    # Relationship
    purchase = relationship("Purchase", back_populates="payments")
