from fastapi import FastAPI
from app.routes.routes import router
from app.asynccontextmanager.asynccontextmanager import lifespan
import uvicorn

app = FastAPI(lifespan=lifespan)

app.include_router(router)



if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)