# NexusTask | سامانه مدیریت وظایف

**NexusTask** یک API برای مدیریت وظایف است که با **FastAPI** و **SQLAlchemy** ساخته شده است. کاربران می‌توانند ثبت‌نام و وارد شوند و وظایف خود را به‌صورت امن مدیریت کنند.

## قابلیت‌ها

- ثبت‌نام و ورود کاربران
- احراز هویت با توکن JWT و طرح Bearer
- ذخیره امن گذرواژه‌ها به‌صورت هش‌شده
- ایجاد، مشاهده، ویرایش و حذف وظایف
- فیلتر وظایف بر اساس وضعیت تکمیل‌شدن
- صفحه‌بندی فهرست وظایف با `limit` و `offset`
- مستندات تعاملی API با Swagger و ReDoc
- تست‌های خودکار با Pytest و پایگاه‌داده جداگانه برای تست

## فناوری‌های استفاده‌شده

- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite
- JWT و bcrypt
- Pytest و HTTPX

## ساختار پروژه

```text
NexusTask/
├── app/
│   ├── core/          # پیکربندی و اتصال پایگاه‌داده
│   ├── models/        # مدل‌های کاربر و وظیفه
│   ├── routers/       # مسیرهای احراز هویت و وظایف
│   └── schemas/       # اعتبارسنجی داده‌های ورودی و خروجی
├── scripts/
│   └── run_all_tests.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_tasks.py
├── .gitignore
├── requirements.txt
└── README.md
------------------------------------------------------------------
پیش‌نیازها
نصب Python 3.13 یا نسخه سازگار
نصب Git
دریافت پروژه

git clone https://github.com/safarishahab30-code/NexusTask.git
cd NexusTask
ساخت و فعال‌سازی محیط مجازی
در ویندوز و PowerShell:


python -m venv .venv
.\.venv\Scripts\Activate.ps1
در Linux یا macOS:


python3 -m venv .venv
source .venv/bin/activate
نصب وابستگی‌ها

pip install -r requirements.txt
اجرای برنامه

uvicorn app.main:app --reload
پس از اجرا، برنامه در نشانی زیر در دسترس خواهد بود:


http://127.0.0.1:8000
مستندات API
پس از اجرای برنامه، مستندات تعاملی در این نشانی‌ها قابل‌دسترسی است:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
اجرای تست‌ها
برای اجرای تست‌ها با Pytest:


pytest -v
یا با اسکریپت پروژه:


python scripts/run_all_tests.py
نمونه درخواست‌ها
ثبت‌نام

curl -X POST "http://127.0.0.1:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"your-password"}'
دریافت توکن ورود

curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=&password=your-password"
ساخت وظیفه

curl -X POST "http://127.0.0.1:8000/tasks/" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title":"مطالعه FastAPI","description":"مرور مستندات و ساخت یک API"}'
دریافت فهرست وظایف همراه با فیلتر و صفحه‌بندی

curl -X GET "http://127.0.0.1:8000/tasks/?completed=false&limit=10&offset=0" \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"