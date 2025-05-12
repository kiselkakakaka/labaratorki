import requests

BASE = "http://127.0.0.1:8000"

def test_auth():
    print("🔐 Получаем токены...")
    r = requests.post(BASE + "/token", data={"client_id": "john", "access_key": "secret"})
    assert r.status_code == 200
    tokens = r.json()
    print("✔️ Access:", tokens["access_token"])
    print("✔️ Refresh:", tokens["refresh_token"])

    print("👤 Доступ к /users/me...")
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    r = requests.get(BASE + "/users/me", headers=headers)
    print("Response:", r.json())
    assert r.status_code == 200

    print("🔄 Обновляем токен...")
    r = requests.post(BASE + "/refresh", data={"refresh_token": tokens["refresh_token"]})
    print("New tokens:", r.json())

if __name__ == "__main__":
    test_auth()
