from pydantic import BaseModel, Field, field_validator
import re

# ---------- User data verification schema ----------
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

# ---------- User information schema ----------
class User(BaseModel):
    id: int
    name: str
    email: str

class UserOut(BaseModel):
    data: User

class Token(BaseModel):
    token: str = Field(description="包含JWT加密字串")

# ---------- 403 error raise schema ----------
class CustomizeRaise(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message