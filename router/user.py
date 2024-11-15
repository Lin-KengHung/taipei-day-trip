from fastapi import *
from fastapi.responses import JSONResponse

from model.user_model import UserModel, JWTBearer
from view.user_view import Token, User, UserOut, UserSignInInput, UserSignUpInput
from view.share import Error, Success


router = APIRouter(
     prefix="/api", 
     tags=["User"]
)
security = JWTBearer()


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
    
    result = UserModel.signin(email=user.email, password=user.password)
    
    if (isinstance(result, Token)):
        return result
    
    if (isinstance(result, Error)):
        return JSONResponse(status_code=400, content=result.model_dump())

@router.get("/user/auth",  summary="取得當前登入的會員資訊", response_model=UserOut)
async def get_user(payload =  Depends(security)):
    return UserOut(data=User(id=payload["id"], name=payload["name"], email=payload["email"]))



