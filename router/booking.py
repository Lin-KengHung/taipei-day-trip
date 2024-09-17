from fastapi import *
from fastapi.responses import JSONResponse

from view.share import Error, Success
from view.booking_view import BookingInput
from model.user_model import JWTBearer
from model.booking_model import BookingModel, BookingOut

router = APIRouter(
     prefix="/api", 
     tags=["Booking"]
)
security = JWTBearer()

@router.get("/booking", summary="取得尚未確認下單的預定行程", response_model=BookingOut, responses={400:{"model":Error}})
async def get_booking_data(payload =  Depends(security)):
    result = BookingModel.get_booking_data(user_id=payload["id"])
    if isinstance(result, Error):
        return JSONResponse(status_code=400, content=result.model_dump())
    
    if isinstance(result, BookingOut):
        return result

@router.post("/booking", summary="建立新的預定行程", response_model=Success, responses={400:{"model":Error}})
async def submit_new_booking(data: BookingInput,  payload =  Depends(security)):
    result = BookingModel.submit_new_booking(attractionId=data.attractionId, userId=payload["id"], booking_date=data.date, time= data.time.value, price=str(data.price.value))
    if (isinstance(result, Error)):
        return JSONResponse(status_code=400, content=result.model_dump())
    
    return Success

@router.delete("/booking", summary="刪除目前的預定行程", response_model=Success)
async def delete_booking(payload =  Depends(security)):
    result = BookingModel.delete_booking(user_id=payload["id"])
    if result is True:
        return Success;
