from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.task import Task as TaskModel
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    # تبدیل داده ورودی Pydantic به مدل دیتابیس SQLAlchemy
    new_task = TaskModel(**task_in.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
