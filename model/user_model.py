from dbconfig import Database
from view.share import Error
from view.user_view import Token, CustomizeRaise
from dotenv import load_dotenv

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request
import bcrypt
import jwt
import datetime
import os

load_dotenv()

# ---------- User behavior model  ----------
class UserModel:
    def check_email_exist(email: str) -> bool:
        if (Database.read_one("SELECT 1 FROM user WHERE email = %s", (email,))):
            return True
        else:
            return False
    
    def signup(name:str, email: str, password: str) -> bool:
        hash_password = make_hash_password(password)
        result = Database.create("INSERT INTO user (name, email, hash_password) VALUES (%s, %s, %s)", (name, email, hash_password))
        if (result > 0):
            return True
        else:
            return False
        
    def signin(email: str, password: str) -> Token | Error:
        current_user = Database.read_one("SELECT * FROM user WHERE email = %s", (email,))
        if current_user is None:
            return Error(message="此email沒有註冊過")

        
        verification = bcrypt.checkpw(password.encode(), current_user["hash_password"].encode())
        if not verification:
            return Error(message="密碼輸入錯誤")

        token = make_JWT(id=current_user["id"], name=current_user["name"], email=current_user["email"])
        return Token(token=token)

# ---------- JWT setting and model  ----------

SECRET_KEY = os.getenv("SECRET")
ALGORITHM = "HS256"
expire = datetime.datetime.now() + datetime.timedelta(days=7)


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise CustomizeRaise(status_code=403, message="錯誤的authentication scheme.")
            payload = self.decode_JWT(credentials.credentials)
            if not payload:
                raise CustomizeRaise(status_code=403, message="無效token或是過期")
            return payload
        else:
            raise CustomizeRaise(status_code=403, message="未登入系統或是授權碼無效")

    def decode_JWT(self, token):
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
            return decoded_token 
        except jwt.ExpiredSignatureError:
            return {}
        except jwt.InvalidTokenError:
            return {}       

# --------------------

def make_hash_password(password: str):
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def make_JWT(id, name, email) -> str:
    payload={"id" : id, "name": name, "email" : email, "exp": expire}
    token = jwt.encode(payload=payload, key= SECRET_KEY, algorithm = ALGORITHM)
    return token

