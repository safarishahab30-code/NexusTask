from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class Task(Base):
  __tablename__ = "tasks"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True, nullable=False)
  description = Column(Text, nullable=True)
  owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
