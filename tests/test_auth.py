def test_register_ok(client):
    payload = {"email": "pytest_user@example.com", "password": "Password123!"}
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert "id" in data
    assert data["email"] == payload["email"]

def test_register_duplicate_email(client):
    payload = {"email": "duplicate@example.com", "password": "Password123!"}
    r1 = client.post("/auth/register", json=payload)
    assert r1.status_code == 201, r1.text
    r2 = client.post("/auth/register", json=payload)
    assert r2.status_code == 400, r2.text

def test_login_success(client):
    user_data = {"email": "login_test@example.com", "password": "Password123!"}
    client.post("/auth/register", json=user_data)

    login_form = {"username": user_data["email"], "password": user_data["password"]}
    r = client.post("/auth/login", data=login_form)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "access_token" in data
    assert data.get("token_type") in ("bearer", "Bearer")

def test_login_wrong_password(client):
    user_data = {"email": "wrong_pwd@example.com", "password": "Password123!"}
    client.post("/auth/register", json=user_data)

    login_form = {"username": user_data["email"], "password": "WrongPassword!"}
    r = client.post("/auth/login", data=login_form)
    assert r.status_code == 401, r.text
