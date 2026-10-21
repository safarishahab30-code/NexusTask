from datetime import datetime
from pydantic import BaseModel, EmailStr


# فرمت داده ورودی ثبت نام
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# فرمت خروجی اطلاعات کاربر (مطابق با ایمپورت UserResponse در پروژه)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# جهت سازگاری کامل با بخش‌هایی که احیاناً UserOut را صدا می‌زنند
UserOut = UserResponse


# ساختار خروجی توکن بعد از لاگین موفق
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
