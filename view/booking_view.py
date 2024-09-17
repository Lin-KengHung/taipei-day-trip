from pydantic import BaseModel
from datetime import date
from enum import Enum

class Attraction(BaseModel):
    id : int
    name : str
    address : str
    image : str

class Booking(BaseModel):
    attraction: Attraction
    date: date
    time: str
    price: int

class BookingOut(BaseModel):
    data: Booking

class Time(Enum):
    morning = "morning"
    afternoon = "afternoon"

class Price(Enum):
    VALUE_2000 = 2000
    VALUE_2500 = 2500
    
class BookingInput(BaseModel):
    attractionId: int
    date: date
    time: Time
    price: Price