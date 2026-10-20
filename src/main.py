from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.app.core.config import settings as s


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App loading")
    yield
    print("App Shutting down")


app = FastAPI(
    title=s.app.title,
    lifespan=lifespan
)

if __name__ == "__main__":
    uvicorn.run(app=app, port=s.app.port, host=s.app.host)
