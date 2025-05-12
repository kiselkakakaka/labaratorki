from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    def test_get_users():
        response = client.get("/users/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["client_id"] == "string"

