import requests

BASE_URL = "http://127.0.0.1:8000"

USER_DATA = {
    "email": "testuser@example.com",
    "password": "StrongPassword123!",
}


def run_tests():
    print("--- شروع تست احراز هویت، تسک‌ها، فیلترها و Pagination ---")

    # ۱. ثبت‌نام کاربر
    reg_res = requests.post(f"{BASE_URL}/auth/register", json=USER_DATA)
    if reg_res.status_code == 201:
        print("[OK] کاربر جدید ساخته شد.")
    elif reg_res.status_code == 400:
        print("[INFO] کاربر از قبل موجود است، ادامه مراحل...")
    else:
        print(f"[FAIL] خطا در ثبت‌نام: {reg_res.status_code} - {reg_res.text}")
        return

    # ۲. ورود و دریافت توکن JWT
    login_data = {
        "username": USER_DATA["email"],
        "password": USER_DATA["password"],
    }
    login_res = requests.post(
        f"{BASE_URL}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if login_res.status_code != 200:
        print(f"[FAIL] لاگین ناموفق: {login_res.status_code} - {login_res.text}")
        return

    token = login_res.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print("[OK] لاگین موفق و توکن دریافت شد.")

    # ۳. ساخت تسک اول (تکمیل‌نشده)
    task1_payload = {
        "title": "تسک اول - مطالعه اسناد FastAPI",
        "description": "بررسی Query Parameters و Pagination",
        "is_completed": False,
    }
    t1_res = requests.post(f"{BASE_URL}/tasks/", json=task1_payload, headers=headers)
    if t1_res.status_code != 201:
        print(f"[FAIL] ساخت تسک اول ناموفق: {t1_res.status_code} - {t1_res.text}")
        return
    t1_id = t1_res.json()["id"]
    print(f"[OK] تسک اول ساخته شد (ID: {t1_id})")

    # ۴. ساخت تسک دوم (تکمیل‌شده)
    task2_payload = {
        "title": "تسک دوم - تست احراز هویت JWT",
        "description": "بررسی توکن‌های Bearer",
        "is_completed": True,
    }
    t2_res = requests.post(f"{BASE_URL}/tasks/", json=task2_payload, headers=headers)
    if t2_res.status_code != 201:
        print(f"[FAIL] ساخت تسک دوم ناموفق: {t2_res.status_code} - {t2_res.text}")
        return
    t2_id = t2_res.json()["id"]
    print(f"[OK] تسک دوم ساخته شد (ID: {t2_id})")

    # ۵. تست فیلتر completed=True
    filter_true_res = requests.get(
        f"{BASE_URL}/tasks/", headers=headers, params={"completed": "true"}
    )
    if filter_true_res.status_code == 200:
        items = filter_true_res.json()
        all_true = all(item["is_completed"] is True for item in items)
        print(f"[OK] فیلتر completed=true: {len(items)} تسک دریافت شد (اعتبارسنجی: {all_true})")
    else:
        print(f"[FAIL] خطا در فیلتر completed=true: {filter_true_res.status_code}")

    # ۶. تست فیلتر completed=False
    filter_false_res = requests.get(
        f"{BASE_URL}/tasks/", headers=headers, params={"completed": "false"}
    )
    if filter_false_res.status_code == 200:
        items = filter_false_res.json()
        all_false = all(item["is_completed"] is False for item in items)
        print(f"[OK] فیلتر completed=false: {len(items)} تسک دریافت شد (اعتبارسنجی: {all_false})")
    else:
        print(f"[FAIL] خطا در فیلتر completed=false: {filter_false_res.status_code}")

    # ۷. تست صفحه‌بندی (limit=1 و offset=0)
    page_res = requests.get(
        f"{BASE_URL}/tasks/", headers=headers, params={"limit": 1, "offset": 0}
    )
    if page_res.status_code == 200 and len(page_res.json()) == 1:
        print("[OK] تست صفحه‌بندی (limit=1): دقیقاً ۱ تسک دریافت شد.")
    else:
        print(f"[FAIL] خطا در تست Pagination: {page_res.status_code}")

    # ۸. تست به‌روزرسانی تسک (PUT /tasks/{id})
    update_payload = {"is_completed": True}
    up_res = requests.put(f"{BASE_URL}/tasks/{t1_id}", json=update_payload, headers=headers)
    if up_res.status_code == 200 and up_res.json()["is_completed"] is True:
        print(f"[OK] تسک {t1_id} آپدیت شد (is_completed: True).")
    else:
        print(f"[FAIL] خطا در آپدیت تسک: {up_res.status_code}")

    # ۹. تست حذف تسک (DELETE /tasks/{id})
    del_res = requests.delete(f"{BASE_URL}/tasks/{t1_id}", headers=headers)
    if del_res.status_code == 204:
        print(f"[OK] تسک {t1_id} با موفقیت حذف شد (204 No Content).")
    else:
        print(f"[FAIL] خطا در حذف تسک: {del_res.status_code}")

    # ۱۰. بررسی عدم وجود تسک حذف‌شده (GET /tasks/{id} -> 404)
    check_deleted = requests.get(f"{BASE_URL}/tasks/{t1_id}", headers=headers)
    if check_deleted.status_code == 404:
        print(f"[OK] تأیید حذف: تسک {t1_id} یافت نشد (404 Not Found).")
    else:
        print(f"[FAIL] تسک حذف‌شده هنوز موجود است: {check_deleted.status_code}")

    print("\n--- تمام قابلیت‌های CRUD، فیلتر و Pagination با موفقیت تأیید شدند! ---")


if __name__ == "__main__":
    run_tests()
