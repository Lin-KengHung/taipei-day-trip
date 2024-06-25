from fastapi import *
from pydantic import BaseModel, field_validator, Field
from . import  Error, Success
from fastapi.responses import JSONResponse
import re
from model.user import UserModel, JWTBearer


router = APIRouter(
     prefix="/api", 
     tags=["User"]
)
security = JWTBearer()

# ---------- View and data verification  ----------
class User(BaseModel):
    id: int
    name: str
    email: str   

class UserOut(BaseModel):
    data: User
    
class UserSignUpInput(BaseModel):
    name: str
    email: str
    password: str

    @field_validator("email")
    def email_match(cls, v: str):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, v):
            raise ValueError("Email格式不正確")
        return v

class UserSignInInput(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    token: str = Field(description="包含JWT加密字串")

# ---------- End point ----------

@router.post("/user", summary="註冊一個新會員", response_model=Success, responses={400:{"model":Error}})
async def signup(user: UserSignUpInput):

    if (UserModel.check_email_exist(user.email)):
        return JSONResponse(status_code=400, content=Error(message="Email已經註冊過").model_dump())
    
    result = UserModel.signup(user.name, user.email, user.password)
    if (result):
        return Success(ok=True)

@router.put("/user/auth", summary="登入會員帳戶", response_model=Token, responses={400:{"model":Error}})
async def signin(user: UserSignInInput):
    
    token = UserModel.signin(email=user.email, password=user.password)
    
    if (token):
        return Token(token=token)
    else:
        return JSONResponse(status_code=400, content=Error(message="email或密碼錯誤").model_dump())

@router.get("/user/auth",  summary="取得當前登入的會員資訊", response_model=UserOut)
async def get_user(payload =  Depends(security)):
    return UserOut(data=User(id=payload["id"], name=payload["name"], email=payload["email"]))



