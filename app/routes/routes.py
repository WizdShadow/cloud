from app.shema import Users, Status, Login
from app.func import hash_parol, check_parol, crt_fold
from fastapi import Depends, APIRouter
from app.database import get_session, get_user, User
from datetime import date
import asyncio

router = APIRouter()    

@router.get("/add/file")
async def add_file():
    return {"message": "Hello World"}

@router.post("/register")
async def register(user: Users, session=Depends(get_session)):
    name = await get_user(session, user.username)
    if name:
        return Status(result=False)
    
    pasw =  await hash_parol(user.password)
    asyncio.create_task(crt_fold(user.username))
    
    user =User(username=user.username,
               email=user.email,
               password_hash=pasw,
               created_at=date.today(),
               updated_at=date.today(),
               is_active=True,
               storage_limit=10737418240,
               storage_used=0)
    session.add(user)
    await session.commit()
    return Status(result=True)

@router.post("/login")
async def login(login: Login, session=Depends(get_session)):
    
    pasw_db, status = await check_parol(login.username, login.password, session)
    if not status:
        return Status(result=False)
    elif not status.username:
        return Status(result=False)
    elif not pasw_db:
        return Status(result=False)
    
    return Status(result=True)