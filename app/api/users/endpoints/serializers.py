from faulthandler import disable
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    disabled: Optional[bool]

    class Config:
        orm_mode = True
