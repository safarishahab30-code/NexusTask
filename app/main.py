from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
import app.models
from app.routers import tasks

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# ابتدا lifespan تعریف شد، حالا شیء app ساخته می‌شود:
app = FastAPI(title="NexusTask API", version="1.0.0", lifespan=lifespan)

# ثبت روتر بعد از ساخت app
app.include_router(tasks.router)

@app.get("/")
def read_root():
    return {"message": "خوش آمدید به پروژه نکسوس‌تسک!"}
