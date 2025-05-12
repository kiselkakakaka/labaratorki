from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

import uuid

def test_create_user():
    unique_id = uuid.uuid4().hex
    client_id = f"testuser_{unique_id}"
    email = f"{client_id}@example.com"

    response = client.post(
        "/register/",
        json={
            "client_id": client_id,
            "email": email,
            "full_name": "Test Client Unique",
            "access_key": "password123"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["client_id"] == client_id
    assert data["email"] == email

    response = client.post(
        "/register/",
        json={
            "client_id": client_id,
            "email": email,
            "full_name": "Test Client Unique",
            "access_key": "password123"
        },
    )
    assert response.status_code == 400

def test_login_for_access_token():
    client.post(
        "/register/",
        json={"client_id": "testuser3", "email": "testuser3@example.com", "full_name": "Test Client 3", "access_key": "password123"},
    )

    response = client.post(
        "/token",
        data={"client_id": "testuser3", "access_key": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    response = client.post(
        "/token",
        data={"client_id": "testuser3", "access_key": "wrongpassword"},
    )
    assert response.status_code == 401

    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalidtoken"},
    )
    assert response.status_code == 401

def test_get_current_user():
    client.post(
        "/register/",
        json={"client_id": "testuser5", "email": "testuser5@example.com", "full_name": "Test Client 5", "access_key": "password123"},
    )

    response = client.post(
        "/token",
        data={"client_id": "testuser5", "access_key": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    token = data["access_token"]

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["client_id"] == "testuser5"

def test_update_user():
    unique_id = uuid.uuid4().hex
    client_id = f"testuser_{unique_id}"
    email = f"{client_id}@example.com"

    response = client.post(
        "/register/",
        json={
            "client_id": client_id,
            "email": email,
            "full_name": "Test Client Unique",
            "access_key": "password123"
        },
    )
    assert response.status_code == 200
    user_id = response.json()["id"]

    response = client.post(
        "/token",
        data={"client_id": client_id, "access_key": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    token = data["access_token"]

    response = client.put(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"full_name": "Updated Test Client Unique"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Test Client Unique"

    response = client.put(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"email": "invalidemail"},
    )
    assert response.status_code == 400  

    response = client.put(
        f"/users/{user_id}",
        headers={"Authorization": "Bearer invalidtoken"},
        json={"full_name": "Updated Test Client Unique"},
    )
    assert response.status_code == 401


def test_delete_user():
    response = client.post(
        "/register/",
        json={"client_id": "testuser7", "email": "testuser7@example.com", "full_name": "Test Client 7", "access_key": "password123"},
    )
    assert response.status_code == 200
    user_id = response.json()["id"]

    response = client.post(
        "/token",
        data={"client_id": "testuser7", "access_key": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    token = data["access_token"]

    response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    response = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404

def test_cors():
    response = client.get("/", headers={"Origin": "http://allowed-origin.com"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://allowed-origin.com"