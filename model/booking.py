from datetime import datetime, date
from pydantic import BaseModel
from model.share import Error
from dbconfig import Database

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


class BookingModel:
    def submit_new_booking(userId:int, attractionId:int , booking_date:date, time:str, price:str) -> bool | Error:
        # 確認時間在今天之後
        if BookingModel.check_date_after_today(booking_date) is False:
            return Error(message="不要活在過去，請放眼未來")
        
        # 確認正確的景點編號
        attraction_exist = Database.read_one("SELECT 1 FROM attraction WHERE id = %s LIMIT 1", (attractionId, ))
        if attraction_exist is None:
            return Error(message="景點編號錯誤")
        
        # 新增訂單 或是 更新訂單
        sql = """
            INSERT INTO booking (attraction_id, user_id, date, time, price)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                attraction_id = VALUES(attraction_id),
                date = VALUES(date),
                time = VALUES(time),
                price = VALUES(price);
            """

        val = (attractionId, userId, str(booking_date), time, price)
        result = Database.create(sql, val)


        if result > 0:
            print ("新增一筆新訂單")
            return True
        else:
            print ("資料庫操作錯誤")
            return False

    def delete_booking(user_id:int) -> bool:
        result = Database.delete("DELETE FROM booking where user_id = %s", (user_id,))
        if result > 0:
            print("正確的刪除一筆資料")
            return True
        else:
            print("資料庫操作錯誤")
            return False

    def get_booking_data(user_id:int) -> BookingOut | Error:

        # 資料庫查詢
        sql = """
            SELECT a.id, a.name, a.address, b.date, b.time, b.price, i.url 
            FROM booking b 
            JOIN attraction a ON b.attraction_id = a.id 
            JOIN image i ON a.id = i.attraction_id 
            WHERE user_id = %s
            LIMIT 1;
            """
        val = (user_id,)
        booking_data = Database.read_one(sql, val)        # 確認使用者有無訂單
        if booking_data is None:
            return Error(message="此人沒有訂單")

        # 資料格式處理
        data = BookingOut(data=Booking(date=booking_data["date"], time=booking_data["time"], price=int(booking_data["price"]) ,attraction=Attraction(id=booking_data["id"],name=booking_data["name"], address=booking_data["address"], image= booking_data["url"])))
        return data

    def check_date_after_today(booking_date:date):
        today = date(int(datetime.today().strftime("%Y")), int(datetime.today().strftime("%m")), int(datetime.today().strftime("%d")))
        return True if booking_date >= today else False