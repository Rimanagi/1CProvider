async def test_health(cl):
    url = "/api/v1/health/"
    response = await cl.get(url)
    assert response.status_code == 200
    assert response.json() == {
        "status": "OK",
        "service": "?",
        "version": "?",
    }