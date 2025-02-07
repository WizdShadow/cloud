import bcrypt
from app.database import get_user
import os

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