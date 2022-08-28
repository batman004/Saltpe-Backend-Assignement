from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    disabled: Optional[bool]

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    email: str


class TokenPayload(BaseModel):
    sub: str
    exp: int
