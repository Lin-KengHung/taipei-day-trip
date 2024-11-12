from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
import jwt
import os

SECRET_KEY = os.getenv("SECRET")
ALGORITHM = "HS256"

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="錯誤的 authentication scheme")
            payload = self.decode_JWT(credentials.credentials)
            if not payload:
                raise HTTPException(status_code=403, detail="無效 token 或已過期")
            return payload
        else:
            raise HTTPException(status_code=403, detail="未提供 token")

    def decode_JWT(self, token: str):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
