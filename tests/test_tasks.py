import pytest

@pytest.fixture
def auth_headers(client):
    email = "task_runner@example.com"
    password = "Password123!"

    # Register (may already exist across some setups; accept 201 or 400)
    reg = client.post("/auth/register", json={"email": email, "password": password})
    assert reg.status_code in (201, 400), reg.text

    # Login (OAuth2PasswordRequestForm expects username + password)
    login = client.post("/auth/login", data={"username": email, "password": password})
    assert login.status_code == 200, login.text

    token = login.json()["access_token"]
    assert token, login.text

    # IMPORTANT: must be "Bearer <token>"
    return {"Authorization": f"Bearer {token}"}


def test_tasks_unauthorized(client):
    r = client.get("/tasks/")
    assert r.status_code == 401, r.text


def test_task_full_lifecycle(client, auth_headers):
    # ?) Create task 1 (not completed)
    res_t1 = client.post(
        "/tasks/",
        json={"title": "Task 1", "description": "Desc 1", "is_completed": False},
        headers=auth_headers,
    )
    assert res_t1.status_code == 201, res_t1.text
    t1_id = res_t1.json()["id"]

    # ?) Create task 2 (completed)
    res_t2 = client.post(
        "/tasks/",
        json={"title": "Task 2", "description": "Desc 2", "is_completed": True},
        headers=auth_headers,
    )
    assert res_t2.status_code == 201, res_t2.text
    t2_id = res_t2.json()["id"]

    # ?) List tasks
    res_list = client.get("/tasks/", headers=auth_headers)
    assert res_list.status_code == 200, res_list.text
    assert len(res_list.json()) == 2

    # ?) Filter completed=true
    res_true = client.get("/tasks/", headers=auth_headers, params={"completed": "true"})
    assert res_true.status_code == 200, res_true.text
    tasks_true = res_true.json()
    assert len(tasks_true) == 1
    assert tasks_true[0]["id"] == t2_id
    assert tasks_true[0]["is_completed"] is True

    # ?) Filter completed=false
    res_false = client.get("/tasks/", headers=auth_headers, params={"completed": "false"})
    assert res_false.status_code == 200, res_false.text
    tasks_false = res_false.json()
    assert len(tasks_false) == 1
    assert tasks_false[0]["id"] == t1_id
    assert tasks_false[0]["is_completed"] is False

    # ?) Pagination
    res_paginated = client.get("/tasks/", headers=auth_headers, params={"limit": 1, "offset": 0})
    assert res_paginated.status_code == 200, res_paginated.text
    assert len(res_paginated.json()) == 1

    # ?) Update task 1 -> completed
    res_update = client.put(f"/tasks/{t1_id}", json={"is_completed": True}, headers=auth_headers)
    assert res_update.status_code == 200, res_update.text
    assert res_update.json()["is_completed"] is True

    # ?) Delete task 1
    res_del = client.delete(f"/tasks/{t1_id}", headers=auth_headers)
    assert res_del.status_code == 204, res_del.text

    # ?) Verify deleted
    res_check = client.get(f"/tasks/{t1_id}", headers=auth_headers)
    assert res_check.status_code == 404, res_check.text
