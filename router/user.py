from fastapi import *
from pydantic import BaseModel, field_validator, Field
from . import connection_pool, Error, Success, make_JWT, JWTBearer
from fastapi.responses import JSONResponse
import bcrypt
import re


router = APIRouter(
     prefix="/api", 
     tags=["User"]
)

security = JWTBearer()
# ----------model part----------
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

# ----------api part----------

@router.post("/user", summary="註冊一個新會員", response_model=Success, responses={400:{"model":Error}})
async def signup(user: UserSignUpInput):
    connect = connection_pool.get_connection()
    mycursor = connect.cursor(dictionary=True)

    ## Verify if the email has existed in database
    mycursor.execute("SELECT 1 FROM user WHERE email = %s", (user.email,))
    exist = mycursor.fetchone()
    if exist:
        return JSONResponse(status_code=400, content=Error(message="Email已經註冊過").model_dump())

    ## signup and hash password
    hash_password = make_hash_password(user.password)
    mycursor.execute("INSERT INTO user (name, email, hash_password) VALUES (%s, %s, %s)", (user.name, user.email, hash_password))
    connect.commit()
    
    mycursor.close()
    connect.close()
    return Success(ok=True)

@router.put("/user/auth", summary="登入會員帳戶", response_model=Token, responses={400:{"model":Error}})
async def signin(user: UserSignInInput):
    connect = connection_pool.get_connection()
    mycursor = connect.cursor(dictionary=True)

    ## Verify if user email exist
    mycursor.execute("SELECT * FROM user WHERE email = %s", (user.email,))
    current_user = mycursor.fetchone()
    if current_user is None:
        return JSONResponse(status_code=400, content=Error(message="此email不存在").model_dump())
    
    ## Verify user password
    verification = bcrypt.checkpw(user.password.encode(), current_user["hash_password"].encode())
    if not verification:
        return JSONResponse(status_code=400, content=Error(message="密碼輸入錯誤").model_dump())

    token = make_JWT(id=current_user["id"], name=current_user["name"], email=current_user["email"])
    mycursor.close()
    connect.close()
    return Token(token=token)

@router.get("/user/auth",  summary="取得當前登入的會員資訊", response_model=UserOut)
async def get_user(payload =  Depends(security)):
    return UserOut(data=User(id=payload["id"], name=payload["name"], email=payload["email"]))


# ----------function part----------

def make_hash_password(password: str):
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


