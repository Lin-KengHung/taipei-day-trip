from fastapi import *
from fastapi.responses import JSONResponse
import uuid

from model.user import JWTBearer
from model.order import OrderModel
from view.order_view import PaymentOut, OrderInput, OrderOut, render_payment_out
from model.booking import BookingModel
from model.share import Error

router = APIRouter(
     prefix="/api", 
     tags=["Order"]
)

security = JWTBearer()

@router.post("/orders", summary="建立新的訂單，並完成付款程序", response_model=PaymentOut)
async def submit_order(data: OrderInput,  payload =  Depends(security)):
     
     # 製作 unique 訂單編號
     order_number = str(uuid.uuid4())[:8]

    # 儲存未付款訂單資料到資料庫
     OrderModel.submit_unpaid_order(order_number=order_number, data=data)
    
    # call TapPay api, return payment number
     status, msg = OrderModel.call_TapPay_by_prime(order_number=order_number, data=data)
    
    # 刪除購物車資料 和 更新訂單付款資訊
     if status == 0:
          BookingModel.delete_booking(user_id=payload["id"])
          OrderModel.update_order_to_paid(order_number=order_number)
          
    # 回傳order number, status, message 給前端
     response = render_payment_out(order_number=order_number, status=status, msg=msg)
     return response

@router.get("/order/{order_number}", summary="根據訂單編號取得預定資訊",response_model=OrderOut, responses={400:{"model":Error}})
async def get_order(payload =  Depends(security), order_number: str = None):

     # 資料庫查詢
     result = OrderModel.get_order_info(order_number=order_number)

     # 回傳資料與錯誤處裡
     if isinstance(result, Error):
          return JSONResponse(status_code=400, content=result.model_dump())
     else:
          return result
     
