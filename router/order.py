from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from repository.order_repository import OrderRepository
from db.dbconfig import get_db
from view.order_view import PaymentOut, OrderInput, OrderOut
from view.share import Error
from repository.booking_repository import BookingRepository
from utils.jwt_bearer import JWTBearer
import uuid

router = APIRouter(prefix="/api", tags=["Order"])

security = JWTBearer()


@router.post("/orders", summary="建立新的訂單，並完成付款程序", response_model=PaymentOut)
def submit_order(data: OrderInput, payload=Depends(security), db: Session = Depends(get_db)):
    order_number = str(uuid.uuid4())[:8]  # 生成訂單編號
    # 儲存未付款訂單
    OrderRepository.submit_unpaid_order(db, order_number, data)

    # 呼叫 TapPay API
    status, msg = OrderRepository.call_tappay_by_prime(db, order_number, data)

    # 刪除購物車 & 更新訂單付款狀態
    if status == 0:
        BookingRepository.delete_booking(db=db, user_id=payload["id"])
        OrderRepository.update_order_to_paid(db, order_number)
    
    return {"data": {"number": order_number, "payment": {"status": status, "message": msg}}}


@router.get("/order/{order_number}", summary="根據訂單編號取得預定資訊", response_model=OrderOut, responses={400: {"model": Error}})
def get_order(order_number: str, db: Session = Depends(get_db)):
    result = OrderRepository.get_order_info(db, order_number)

    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.message)
    return result
