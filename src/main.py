from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.app.api import router as api_router
from src.app.core.config import settings as s


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App loading", s.app.url)

    yield
    print("App Shutting down")


app = FastAPI(
    title=s.app.title,
    lifespan=lifespan
)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app=app, port=s.app.port, host=s.app.host)
