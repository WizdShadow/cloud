from app.shema.shema import Users, Status, Login
from app.func.func import hash_parol, check_parol, crt_fold, create_token, sec_key, alg, kafka_producer
from fastapi import Depends, APIRouter, Response, status, Request, Form, HTTPException
from fastapi.responses import RedirectResponse  
from app.database.func_models import get_session, get_user, User
from datetime import date
import asyncio
from typing import Annotated
from app.config.config import templates
import jwt
from app.redis.redis import redis_set, redis_get

router = APIRouter()   


@router.get("/add/file")
async def add_file():
    return {"message": "Hello World"}

@router.get("/")
async def get_index(request: Request = None):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/register")
async def get_register(request: Request = None):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/login")
async def get_login(request: Request = None):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/register")
async def post_register(user: Annotated[Users, Form()], session=Depends(get_session), response: Response = None,):
    name = await get_user(session, user.username)
    if name:
        return Status(result=False)
    
    pasw =  await hash_parol(user.password)
    asyncio.create_task(kafka_producer(user.username))
    
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
    response = RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="token", value=await create_token({"username":user.username}), httponly=True, secure=False)
    return response


@router.post("/login")
async def login(login: Login, session=Depends(get_session)):
    pasw_db, status = await check_parol(login.username, login.password, session)
    if not status:
        return Status(result=False)
    elif not status.username:
        return Status(result=False)
    elif not pasw_db:
        return Status(result=False)
    token = await create_token({"username":login.username})
    return {"result": True, "token": token} 


@router.get("/profile")
async def profile(request: Request = None):
    return templates.TemplateResponse("profile.html", {"request": request})


@router.get("/check")
async def check(request: Request = None):
    token = request.headers.get("Authorization")
    print(token)
    if not token:
        return {"status": False}
    token = await redis_get(token)
    if token is None:
        return {"status": False}
    return {"status": True}