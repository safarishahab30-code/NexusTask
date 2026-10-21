import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

# اگر این کاربر قبلاً وجود داشته باشد، register خطای 400 می‌دهد که مشکلی نیست.
EMAIL = "user@example.com"
PASSWORD = "string"


def pretty(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2)


def check_server():
    try:
        r = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"[OK] Server reachable: GET / -> {r.status_code}")
        return True
    except requests.RequestException as e:
        print("[FAIL] Server is not reachable.")
        print("Reason:", e)
        print("Fix: run -> uvicorn app.main:app --reload")
        return False


def register():
    payload = {"email": EMAIL, "password": PASSWORD}
    r = requests.post(f"{BASE_URL}/auth/register", json=payload, timeout=10)

    # 201: ساخته شد | 400: ایمیل تکراری (قابل قبول)
    if r.status_code in (201, 400):
        print(f"[OK] Register: {r.status_code}")
        try:
            print(pretty(r.json()))
        except Exception:
            print(r.text)
        return True

    print(f"[FAIL] Register failed: {r.status_code}")
    print(r.text)
    return False


def login_get_token():
    # مهم: /auth/login با OAuth2PasswordRequestForm کار می‌کند => form-data
    data = {
        "username": EMAIL,
        "password": PASSWORD,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    r = requests.post(f"{BASE_URL}/auth/login", data=data, headers=headers, timeout=10)
    if r.status_code != 200:
        print(f"[FAIL] Login failed: {r.status_code}")
        print(r.text)
        return None

    j = r.json()
    # چون کلید access token در پروژه شما ممکنه 'access_token' یا همان کلید عجیب باشد،
    # هر کلیدی که مقدارش شبیه JWT باشد را پیدا می‌کنیم.
    token = None
    for k, v in j.items():
        if isinstance(v, str) and v.count(".") == 2:  # JWT has 2 dots
            token = v
            break

    if not token:
        print("[FAIL] Token not found in login response:")
        print(pretty(j))
        return None

    print("[OK] Login succeeded. Token extracted.")
    return token


def users_me(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/users/me", headers=headers, timeout=10)

    if r.status_code != 200:
        print(f"[FAIL] GET /users/me failed: {r.status_code}")
        print(r.text)
        return False

    print("[OK] GET /users/me succeeded:")
    print(pretty(r.json()))
    return True


def main():
    if not check_server():
        sys.exit(1)

    if not register():
        sys.exit(1)

    token = login_get_token()
    if not token:
        sys.exit(1)

    ok = users_me(token)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
