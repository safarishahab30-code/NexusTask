from typing import Optional
from pydantic import BaseModel, ConfigDict


# فیلدهای پایه که کاربر ارسال می‌کند (بدون owner_id)
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False


# اسکیمای ساخت تسک جدید
class TaskCreate(TaskBase):
    pass


# اسکیمای آپدیت تسک
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


# اسکیمای خروجی که به کلاینت نمایش داده می‌شود (شامل id و owner_id)
class TaskResponse(TaskBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
