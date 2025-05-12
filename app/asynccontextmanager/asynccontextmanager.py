from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.func_models import init_db
from aiokafka import AIOKafkaProducer

producer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    app.state.producer = AIOKafkaProducer(bootstrap_servers="localhost:9094")
    await app.state.producer.start()
    yield