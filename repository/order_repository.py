from sqlalchemy.orm import Session, aliased
from model.order_model import Purchase, Payment
from model.attraction_model import Attraction, Image
from view.order_view import OrderInput, render_order_out
from view.share import Error
import requests
import os
from datetime import datetime
from sqlalchemy.exc import IntegrityError



class OrderRepository:

    @staticmethod
    def submit_unpaid_order(db: Session, order_number: str, data: OrderInput):
        """
        儲存未付款訂單到資料庫
        """
        try:
            purchase = Purchase(
                id=order_number,
                prime=data.prime,
                attraction_id=data.order.trip.attraction.id,
                price=data.order.price,
                date=str(data.order.trip.date),
                time=data.order.trip.time,
                name=data.order.contact.name,
                email=data.order.contact.email,
                phone=data.order.contact.phone,
                paid=0,  # 未付款
                created_time=datetime.utcnow()
            )
            db.add(purchase)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise ValueError("資料庫操作失敗")

    @staticmethod
    def call_tappay_by_prime(db, order_number: str, data: OrderInput):
        """
        呼叫 TapPay API 完成付款
        """
        post_data = {
            "prime": data.prime,
            "partner_key": os.getenv("PARTNERKEY"),
            "merchant_id": "alfyn_FUBON_POS_1",
            "amount": data.order.price,
            "currency": "TWD",
            "details": f"景點id: {data.order.trip.attraction.id}",
            "cardholder": {
                "phone_number": data.order.contact.phone,
                "name": data.order.contact.name,
                "email": data.order.contact.email,
            },
            "remember": False,
        }

        headers = {
            "Content-Type": "application/json",
            "x-api-key": "partner_fyMX8OF619f3dNiAHquASYdYRuwsjemaLrCJKkqYlHKe4wzRURS9E5IZ",
        }

        response = requests.post(
            "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime",
            json=post_data,
            headers=headers,
        )
        response = response.json()

        # 儲存付款結果
        OrderRepository.submit_payment(
            db=db,
            order_number=order_number,
            status=response["status"],
            msg=response["msg"],
            rec_trade_id=response.get("rec_trade_id", ""),
        )

        return response["status"], response["msg"]

    @staticmethod
    def submit_payment(db: Session, order_number: str, status: int, msg: str, rec_trade_id: str):
        """
        儲存付款記錄到資料庫
        """
        payment = Payment(
            purchase_id=order_number,
            status=status,
            msg=msg,
            rec_trade_id=rec_trade_id,
            created_time=datetime.utcnow(),
        )
        db.add(payment)
        db.commit()

    @staticmethod
    def update_order_to_paid(db: Session, order_number: str):
        """
        將訂單更新為已付款
        """
        purchase = db.query(Purchase).filter(Purchase.id == order_number).first()
        if purchase:
            purchase.paid = 1
            db.commit()

    @staticmethod
    def get_order_info(db: Session, order_number: str):
        """
        根據訂單編號查詢訂單詳情
        """
        # Alias for the Image model to simplify join
        ImageAlias = aliased(Image)

        query = (
            db.query(
                Purchase.id.label("order_number"),
                Purchase.price,
                Purchase.date,
                Purchase.time,
                Purchase.name,
                Purchase.email,
                Purchase.phone,
                Attraction.id.label("attraction_id"),
                Attraction.name.label("attraction_name"),
                Attraction.address,
                ImageAlias.url.label("img"),
                Payment.status,
            )
            .join(Attraction, Purchase.attraction_id == Attraction.id)
            .join(ImageAlias, Attraction.id == ImageAlias.attraction_id)  # Join with image table
            .join(Payment, Purchase.id == Payment.purchase_id)
            .filter(Purchase.id == order_number)
        ).first()

        if not query:
            return Error(message="錯誤訂單編號")

        return render_order_out(
            order_number=query.order_number,
            status=query.status,
            price=query.price,
            attraction_id=query.attraction_id,
            attraction_name=query.attraction_name,
            address=query.address,
            img=query.img,
            date=query.date,
            time=query.time,
            name=query.name,
            email=query.email,
            phone=query.phone,
        )
