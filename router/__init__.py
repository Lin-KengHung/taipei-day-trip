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

## JWT
SECRET_KEY = "secret"
ALGORITHM = "HS256"
expire = datetime.datetime.now() + datetime.timedelta(days=7)

def make_JWT(id, name, email) -> str:
    payload={"id" : id, "name": name, "email" : email, "exp": expire}
    token = jwt.encode(payload=payload, key= SECRET_KEY, algorithm = ALGORITHM)
    return token

def decode_JWT(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        return decoded_token
    except jwt.ExpiredSignatureError:
        return Error(error=True, message="Token has expired")
    except jwt.InvalidTokenError:
        return Error(error=True, message="Invalid token")


# class JWTBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super(JWTBearer, self).__init__(auto_error=auto_error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
#         if credentials:
#             if not credentials.scheme == "Bearer":
#                 return JSONResponse(status_code=400, content=Error(message="你輸入的不是Bearer scheme").model_dump())
#                 # raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
#             if not self.verify_JWT(credentials.credentials):
#                 return JSONResponse(status_code=400, content=Error(message="Token無效或是過期").model_dump())
#                 # raise HTTPException(status_code=403, detail="Invalid token or expired token.")
#             return credentials.credentials
#         else:
#             raise JSONResponse(status_code=400, content=Error(message="驗證失敗").model_dump())

#     def verify_JWT(self, jwtoken: str) -> bool:
#         isTokenValid: bool = False

#         try:
#             payload = decode_JWT(jwtoken)
#         except:
#             payload = None
#         if payload:
#             isTokenValid = True

#         return isTokenValid

