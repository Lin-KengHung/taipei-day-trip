from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date
from model.booking_model import Booking
from model.attraction_model import Attraction
from view.share import Error
from view.booking_view import Attraction as AttractionView, Booking as BookingView, BookingOut


class BookingRepository:

    @staticmethod
    def submit_new_booking(db: Session, user_id: int, attraction_id: int, booking_date: date, time: str, price: str) -> bool | Error:
        """
        提交新訂單或更新現有訂單
        """
        # 確認時間在今天之後
        if not BookingRepository.check_date_after_today(booking_date):
            return Error(message="不要活在過去，請放眼未來")
        
        # 確認正確的景點編號
        attraction_exist = db.query(Attraction).filter(Attraction.id == attraction_id).first()
        if not attraction_exist:
            return Error(message="景點編號錯誤")
        
        # 新增或更新訂單
        try:
            booking = (
                db.query(Booking)
                .filter(Booking.user_id == user_id)
                .first()
            )
            if booking:
                # 更新訂單
                booking.attraction_id = attraction_id
                booking.date = str(booking_date)
                booking.time = time
                booking.price = price
            else:
                # 新增訂單
                booking = Booking(
                    attraction_id=attraction_id,
                    user_id=user_id,
                    date=str(booking_date),
                    time=time,
                    price=price
                )
                db.add(booking)
            db.commit()
            return True
        except IntegrityError:
            db.rollback()
            return Error(message="資料庫操作錯誤")

    @staticmethod
    def delete_booking(db: Session, user_id: int) -> bool:
        """
        刪除訂單
        """
        result = db.query(Booking).filter(Booking.user_id == user_id).delete()
        db.commit()
        return result > 0

    @staticmethod
    def get_booking_data(db: Session, user_id: int) -> BookingOut | Error:
        """
        獲取訂單資料
        """
        booking_data = (
            db.query(Booking, Attraction)
            .join(Attraction, Booking.attraction_id == Attraction.id)
            .filter(Booking.user_id == user_id)
            .first()
        )

        if not booking_data:
            return Error(error=True, message="此人沒有訂單")

        booking, attraction = booking_data

        data = BookingOut(
            data=BookingView(
                date=booking.date,
                time=booking.time,
                price=int(booking.price),
                attraction=AttractionView(
                    id=attraction.id,
                    name=attraction.name,
                    address=attraction.address,
                    image=attraction.images[0].url if attraction.images else ""
                )
            )
        )
        return data

    @staticmethod
    def check_date_after_today(booking_date: date) -> bool:
        """
        確認日期是否在今天或之後
        """
        today = datetime.utcnow().date()
        return booking_date >= today
