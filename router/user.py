from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from repository.user_repository import UserRepository
from db.dbconfig import get_db
from view.user_view import Token, UserSignUpInput, UserSignInInput, UserOut
from view.share import Error, Success
from utils.jwt_bearer import JWTBearer

router = APIRouter(prefix="/api", tags=["User"])
security = JWTBearer()

@router.post("/user", summary="註冊一個新會員", response_model=Success, responses={400: {"model": Error}})
def signup(user: UserSignUpInput, db: Session = Depends(get_db)):
    if UserRepository.check_email_exist(db, user.email):
        raise HTTPException(status_code=400, detail="Email 已經註冊過")
    
    if UserRepository.signup(db, user.name, user.email, user.password):
        return Success(ok=True)
    raise HTTPException(status_code=400, detail="註冊失敗")

@router.put("/user/auth", summary="登入會員帳戶", response_model=Token, responses={400: {"model": Error}})
def signin(user: UserSignInInput, db: Session = Depends(get_db)):
    result = UserRepository.signin(db, user.email, user.password)
    if isinstance(result, Error):
        raise HTTPException(status_code=400, detail=result.message)
    return result

@router.get("/user/auth", summary="取得當前登入的會員資訊", response_model=UserOut)
def get_user(payload=Depends(security)):
    return UserOut(data={"id": payload["id"], "name": payload["name"], "email": payload["email"]})
