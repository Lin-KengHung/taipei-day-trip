from sqlalchemy import Column, BigInteger, String, Index
from sqlalchemy.orm import relationship
from db.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False, comment="name")
    email = Column(String(255), nullable=False, unique=True, comment="email")
    hash_password = Column(String(255), nullable=False, comment="hash_password")

    booking = relationship("Booking", back_populates="user", uselist=False)

