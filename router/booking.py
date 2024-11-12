from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from repository.booking_repository import BookingRepository
from db.dbconfig import get_db
from view.booking_view import BookingInput, BookingOut
from view.share import Error, Success
from utils.jwt_bearer import JWTBearer

router = APIRouter(prefix="/api", tags=["Booking"])
security = JWTBearer()

@router.get("/booking", summary="取得尚未確認下單的預定行程", response_model=BookingOut, responses={400: {"model": Error}})
def get_booking_data(payload=Depends(security), db: Session = Depends(get_db)):
    result = BookingRepository.get_booking_data(db, user_id=payload["id"])
    if isinstance(result, Error):
        return JSONResponse(status_code=400, content=result.model_dump())
    return result

@router.post("/booking", summary="建立新的預定行程", response_model=Success, responses={400: {"model": Error}})
def submit_new_booking(data: BookingInput, payload=Depends(security), db: Session = Depends(get_db)):
    result = BookingRepository.submit_new_booking(
        db,
        user_id=payload["id"],
        attraction_id=data.attractionId,
        booking_date=data.date,
        time=data.time.value,
        price=str(data.price.value)
    )
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.message)
    return Success(ok=True)

@router.delete("/booking", summary="刪除目前的預定行程", response_model=Success)
def delete_booking(payload=Depends(security), db: Session = Depends(get_db)):
    result = BookingRepository.delete_booking(db, user_id=payload["id"])
    if result:
        return Success(ok=True)
    raise HTTPException(status_code=400, detail="刪除失敗")
