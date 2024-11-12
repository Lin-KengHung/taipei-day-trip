from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from model.user_model import User
from view.share import Error
from view.user_view import Token
import bcrypt
import jwt
import datetime
import os


# JWT 設定
SECRET_KEY = os.getenv("SECRET")
ALGORITHM = "HS256"
EXPIRE_DAYS = 7

def make_hash_password(password: str) -> str:
    """生成雜湊密碼"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()

def make_JWT(id: int, name: str, email: str) -> str:
    """生成 JWT Token"""
    expire = datetime.datetime.utcnow() + datetime.timedelta(days=EXPIRE_DAYS)
    payload = {"id": id, "name": name, "email": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

class UserRepository:

    @staticmethod
    def check_email_exist(db: Session, email: str) -> bool:
        # 檢查 email 是否已註冊
        return db.query(User).filter(User.email == email).first() is not None

    @staticmethod
    def signup(db: Session, name: str, email: str, password: str) -> bool:
        # 註冊新用戶
        hashed_password = make_hash_password(password)
        new_user = User(name=name, email=email, hash_password=hashed_password)
        try:
            db.add(new_user)
            db.commit()
            return True
        except IntegrityError:
            db.rollback()
            return False

    @staticmethod
    def signin(db: Session, email: str, password: str) -> Token | Error:
        # 用戶登入
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return Error(message="此 email 尚未註冊")
        
        if not bcrypt.checkpw(password.encode(), user.hash_password.encode()):
            return Error(message="密碼輸入錯誤")
        
        token = make_JWT(id=user.id, name=user.name, email=user.email)
        return Token(token=token)
