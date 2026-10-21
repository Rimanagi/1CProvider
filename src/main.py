import uvicorn

from src.app.core.config import Settings
from src.app.factory import create_app

s = Settings() # pyright: ignore[reportCallIssue]
app = create_app(s)

if __name__ == "__main__":
    uvicorn.run(app=app, port=s.app.port, host=s.app.host)
