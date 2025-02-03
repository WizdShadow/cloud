from main import app
from shema import User, Status
from func import hash_parol
from fastapi import Depends, APIRouter
from database import get_session, get_user
from datetime import datetime

router = APIRouter()    

@app.get("/add/file")
async def add_file():
    return {"message": "Hello World"}

@app.post("/register")
async def register(user: User, session=Depends(get_session)):
    name = get_user(session, user.username)
    if name:
        return Status(result=False)
    
    pasw =  await hash_parol(user.password)
    
    user =User(username=user.username,
               email=user.email,
               password=pasw,
               created_at=datetime.now().strftime("%Y-%m-%d"),
               updated_at=datetime.now().strftime("%Y-%m-%d"),
               is_active=True,
               storage_limit=10737418240,
               storage_used=0)
    session.add(user)
    await session.commit()
    return Status(result=True)