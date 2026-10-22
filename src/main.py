import uvicorn

from src.app.core.config import Settings
from src.app.factory import create_app

settings = Settings()  # pyright: ignore[reportCallIssue]
app = create_app(settings)

if __name__ == "__main__":
    uvicorn.run(app=app, port=settings.app.port, host=settings.app.host)
