import bcrypt

async def hash_parol(parol):
    hash = bcrypt.hashpw(parol, bcrypt.gensalt())
    return hash