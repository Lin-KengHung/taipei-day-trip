from pydantic import BaseModel, EmailStr
from datetime import date

class Attraction(BaseModel):
    id : int
    name : str
    address : str
    image : str
class Contact(BaseModel):
     name : str
     email : EmailStr
     phone : str

class Trip(BaseModel):
     attraction : Attraction
     date : date
     time: str

class Order(BaseModel):
     price : int
     trip : Trip
     contact : Contact

class OrderInput(BaseModel):
     prime: str
     order: Order

class OrderData(Order):
    number: str
    status: int

class OrderOut(BaseModel):
     data: OrderData

class Payment(BaseModel):
     status: int
     message: str

class PaymentData(BaseModel):
     number: str
     payment: Payment

class PaymentOut(BaseModel):
     data: PaymentData


def render_payment_out(order_number, status, msg) -> PaymentOut:
    data = PaymentOut(data=PaymentData(number=order_number, payment=Payment(status=status, message=msg)))
    return data

def render_order_out(order_number, status, price, date, time, name, email, phone, attraction_id, attraction_name, address, img) -> OrderOut:
    data = OrderOut(data=OrderData(number=order_number, status=status, price=price, trip=Trip(attraction=Attraction(id=attraction_id, name=attraction_name, address=address, image=img), date=date, time=time), contact=Contact(name=name, email=email, phone=phone)))
    return data