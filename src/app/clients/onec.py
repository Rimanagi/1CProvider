import httpx


class OneCClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client
