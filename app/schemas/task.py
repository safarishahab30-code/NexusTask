from typing import Optional
from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
  title: str
  description: Optional[str] = None
  owner_id: int


class TaskCreate(TaskBase):
  pass


class TaskResponse(TaskBase):
  id: int

  model_config = ConfigDict(from_attributes=True)
