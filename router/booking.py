from fastapi import *
from pydantic import BaseModel, EmailStr, Field
from . import connection_pool, Error, Success, JWTBearer
from fastapi.responses import JSONResponse


router = APIRouter(
     prefix="/api", 
)

security = JWTBearer()

class BookingInput(BaseModel):
    attractionId: int
    date: str
    time: str
    price: int
 


@router.get("/booking", summary="取得尚未確認下單的預定行程", response_model=Success, responses={400:{"model":Error}})
async def booking():
    return Success;

@router.post("/booking", dependencies=[Depends(security)], summary="建立新的預定行程", response_model=Success, responses={400:{"model":Error}})
async def booking(data: BookingInput, request: Request,):
    print(data)
    return Success;

@router.delete("/booking", summary="刪除目前的預定行程", response_model=Success, responses={400:{"model":Error}})
async def booking():
    return Success;
