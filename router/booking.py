from fastapi import *
from pydantic import BaseModel, Field
from . import connection_pool, Error, Success, JWTBearer
from fastapi.responses import JSONResponse
from enum import Enum
from datetime import datetime, date


router = APIRouter(
     prefix="/api", 
     tags=["Booking"]
)

security = JWTBearer()

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

class BookingAttraction(BaseModel):
    id : int
    name : str
    address : str
    image : str
class Booking(BaseModel):
    attraction: BookingAttraction
    date: date
    time: Time
    price: Price
class DataOut(BaseModel):
    data: Booking


@router.get("/booking", summary="取得尚未確認下單的預定行程", response_model=DataOut, responses={400:{"model":Error}})
async def get_booking_data(payload =  Depends(security)):
    connect = connection_pool.get_connection()
    mycursor = connect.cursor(dictionary=True)
    
    # 由於專案的設計只有要一筆資料，我的database又沒有設計成一個user只能有一筆訂單，故這裡的邏輯我先寫成抓一筆最新的訂單
    mycursor.execute(
        """
        WITH filtered_booking AS (SELECT * FROM booking WHERE user_id = %s ORDER by id DESC LIMIT 1)
        SELECT a.id, a.name, a.address, b.date, b.time, b.price, i.url
        FROM filtered_booking AS b
        JOIN attraction AS a ON b.attraction_id = a.id
        JOIN image AS i ON a.id = i.attraction_id
        LIMIT 1;
        """
        ,(payload["id"],))
    booking_data = mycursor.fetchone()

    # check booking is exist
    if booking_data is None:
        return JSONResponse(status_code=400, content=Error(message="此人沒有訂單").model_dump())

    response = DataOut(data=Booking(date=booking_data["date"], time=booking_data["time"], price=int(booking_data["price"]) ,attraction=BookingAttraction(id=booking_data["id"],name=booking_data["name"], address=booking_data["address"], image= booking_data["url"])))
 
    mycursor.close()
    connect.close()
    return response;

@router.post("/booking", summary="建立新的預定行程", response_model=Success, responses={400:{"model":Error}})
async def submit_new_booking(data: BookingInput,  payload =  Depends(security)):
    print("提交booking data")
    connect = connection_pool.get_connection()
    mycursor = connect.cursor(dictionary=True)
    # check booking date is after today
    if check_date_after_today(data.date) is False:
        return JSONResponse(status_code=400, content=Error(message="不要活在過去，請放眼未來").model_dump())
    # verify if attraction id is exist in database
    mycursor.execute("SELECT 1 FROM attraction WHERE id = %s LIMIT 1", (data.attractionId,))
    exist = mycursor.fetchone()
    if exist is None:
        return JSONResponse(status_code=400, content=Error(message="景點編號錯誤").model_dump())
    
    # insert booking data to booking table
    # 如果很要求database 中只能有一筆資料，就要寫判斷該user id 是否有訂單，再去決定用insert or update booking table
    mycursor.execute("INSERT INTO booking (attraction_id, user_id, date, time, price) VALUES (%s, %s, %s, %s, %s)", (data.attractionId, payload["id"], data.date, data.time.value, str(data.price.value)))
    connect.commit()
    
    mycursor.close()
    connect.close()
    return Success;

@router.delete("/booking", summary="刪除目前的預定行程", response_model=Success)
async def delete_booking(payload =  Depends(security)):
    connect = connection_pool.get_connection()
    mycursor = connect.cursor(dictionary=True)
    
    mycursor.execute("DELETE FROM booking where user_id = %s", (payload["id"],)) 
    connect.commit()

    mycursor.close()
    connect.close()
    return Success;


def check_date_after_today(booking_date:date):
    today = date(int(datetime.today().strftime("%Y")), int(datetime.today().strftime("%m")), int(datetime.today().strftime("%d")))
    return True if booking_date >= today else False