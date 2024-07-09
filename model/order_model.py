from dbconfig import Database
from view.order_view import OrderInput, render_order_out, OrderOut
from view.share import Error
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class OrderModel:
     def submit_unpaid_order(order_number, data : OrderInput):
          sql = """
            INSERT INTO purchase (id, prime, attraction_id, price, date, time, name, email, phone, paid)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
          """
          val = (order_number, data.prime, data.order.trip.attraction.id, data.order.price, str(data.order.trip.date), data.order.trip.time, data.order.contact.name, data.order.contact.email,  data.order.contact.phone, 0)
          result = Database.create(sql, val)
          if result>0:
               print ("成功新增一筆未付款訂單")
          else:
               print("資料庫操作有誤")
               
     def call_TapPay_by_prime(order_number, data : OrderInput):
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
                    "email": data.order.contact.email
               },
               "remember": False
          }

          headers = {
               "Content-Type": "application/json",
               "x-api-key": "partner_fyMX8OF619f3dNiAHquASYdYRuwsjemaLrCJKkqYlHKe4wzRURS9E5IZ"
          }

          response = requests.post(
               "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime",
               json=post_data,
               headers=headers
          )
          response = response.json()

          OrderModel.submit_payment(order_number=order_number, status=response["status"], msg=response["msg"], rec_trade_id=response["rec_trade_id"])
          
          return response["status"], response["msg"]

     def submit_payment(order_number, status, msg, rec_trade_id):
          sql = """
            INSERT INTO payment (purchase_id, status, msg, rec_trade_id)
            VALUES (%s, %s, %s, %s)
          """
          val = (order_number, status, msg, rec_trade_id)
          Database.create(sql, val)

     def update_order_to_paid(order_number):
          sql = "UPDATE purchase SET paid = 1 where id = %s"
          val = (order_number,)
          result = Database.update(sql, val)
          if result > 0:
               print(f"訂單編號{order_number}更新為已付款")

     def get_order_info(order_number) -> OrderOut | bool:
          sql = """
               SELECT p.id order_number, p.price, p.date, p.time, p.name, p.email, p.phone, a.id attraction_id, a.name attraction_name, a.address, i.url, pay.status
               FROM purchase p 
               JOIN attraction a ON p.attraction_id = a.id 
               JOIN image i ON a.id = i.attraction_id
               JOIN payment pay ON p.id = pay.purchase_id
               WHERE p.id = %s
               LIMIT 1;
               """
          val = (order_number,)
          data = Database.read_one(sql, val)
          if data != None:
               order_out = render_order_out(order_number=data["order_number"], status=data["status"], price=data["price"], attraction_id=data["attraction_id"], attraction_name=data["attraction_name"], address=data["address"], img=data["url"], date=data["date"], time=data["time"], name=data["name"], email=data["email"], phone=data["phone"])
               return order_out
          else:
               return Error(message="錯誤訂單編號")
         
         