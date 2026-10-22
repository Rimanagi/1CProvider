import uvicorn

from src.app.core.config import Settings
from src.app.core.logger import configure_logging
from src.app.factory import create_app

settings = Settings()  # pyright: ignore[reportCallIssue]
configure_logging(settings.log)
app = create_app(settings)

if __name__ == "__main__":
    uvicorn.run(app=app, port=settings.app.port, host=settings.app.host)
