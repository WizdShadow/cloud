import bcrypt
import os
import jwt
from datetime import datetime, timedelta
from aiokafka import AIOKafkaProducer
from app.database.func_models import get_user
from app.redis.redis import redis_set

sec_key="secret"
alg = "HS256"
time_token=3660 


async def kafka():
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9094")
    await producer.start()
    return producer
    
async def hash_parol(parol):
    hash = bcrypt.hashpw(parol.encode('utf-8'), bcrypt.gensalt())
    return hash.decode('utf-8')

async def check_parol(login, parol, session):
    hash = await get_user(session, login)
    if not hash:
        return False, False
    return bcrypt.checkpw(parol.encode('utf-8'), hash.password_hash.encode('utf-8')), hash

async def crt_fold(name):
    fl =["text_file", "image", "video", "web", "exe", "other", "archive", "sound", "table"]
    for  i in fl:
        os.makedirs(f"upload/{name}/{i}")
        
async def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=time_token)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, sec_key, algorithm=alg)
    await redis_set("token", encoded_jwt)
    return encoded_jwt
    
async def kafka_producer(name):
    producer = await kafka()
    await producer.send("file", name.encode('utf-8'))
    await producer.stop()
    
    
            