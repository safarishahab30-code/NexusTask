from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from app.database import Base, engine
from app.models import task, user
from app.routers import auth, tasks
from app.security import get_current_user
from app.models.user import User


# چرخه حیات اپلیکیشن و ساخت جداول دیتابیس در زمان استارت‌آپ
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="NexusTask API",
    description="سیستم مدیریت تسک با احراز هویت JWT و پایگاه داده",
    version="1.0.0",
    lifespan=lifespan
)

# رجیستر کردن روترها
app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/")
def read_root():
    return {"message": "خوش آمدید به پروژه نکسوس‌تسک!"}


@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    """دریافت مشخصات کاربری که لاگین کرده با استفاده از توکن JWT"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active
    }
