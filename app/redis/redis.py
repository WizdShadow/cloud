import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0)


async def redis_set(key, value):
    return redis_client.set(key, value, ex=66000)

async def redis_get(key):
    key = key.replace("Bearer ", "")
    return redis_client.get(key)