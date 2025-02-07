from pydantic import BaseModel, EmailStr
from typing import List


class Users(BaseModel):
    username: str
    email: EmailStr
    password: str

class Status(BaseModel):
    result: bool
    
class Login(BaseModel):
    username: str
    password: str