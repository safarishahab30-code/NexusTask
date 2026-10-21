from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.security import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_task = Task(
        title=task_in.title,
        description=task_in.description,
        is_completed=task_in.is_completed,
        owner_id=current_user.id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/", response_model=List[TaskResponse])
def get_user_tasks(
    completed: Optional[bool] = Query(
        default=None,
        description="فیلتر بر اساس وضعیت انجام تسک (true یا false)",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="تعداد آیتم‌ها در هر صفحه (حداکثر ۱۰۰)",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="تعداد آیتم‌هایی که نادیده گرفته می‌شوند (شروع صفحه)",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Task).filter(Task.owner_id == current_user.id)

    if completed is not None:
        query = query.filter(Task.is_completed == completed)

    tasks = (
        query.order_by(Task.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="تسک مورد نظر یافت نشد.")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="تسک مورد نظر یافت نشد.")

    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="تسک مورد نظر یافت نشد.")

    db.delete(task)
    db.commit()
    return None
