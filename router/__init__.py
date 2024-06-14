import mysql.connector
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import jwt
import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi import Request

## .env
load_dotenv()
password = os.getenv("PASSWORD")


## connect to MySQL
mydb = {
    "host" : "localhost",
    "user" : "root",
    "password" : password,
    "database" : "taipei_day_trip"
}
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="my_pool", pool_size=10, **mydb)

## universal model
class Error(BaseModel):
    error : bool = True
    message : str

class Success(BaseModel):
    ok: bool = True

class CustomizeRaise(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

## JWT
SECRET_KEY = "secret"
ALGORITHM = "HS256"
expire = datetime.datetime.now() + datetime.timedelta(days=7)

def make_JWT(id, name, email) -> str:
    payload={"id" : id, "name": name, "email" : email, "exp": expire}
    token = jwt.encode(payload=payload, key= SECRET_KEY, algorithm = ALGORITHM)
    return token

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


