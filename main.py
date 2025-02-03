from fastapi import FastAPI
from contextlib import asynccontextmanager
from app import init_db
from app import routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(routes.router)



