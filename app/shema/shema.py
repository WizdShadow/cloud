from pydantic import BaseModel
from typing import List, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    password: str

class Status(BaseModel):
    result: bool