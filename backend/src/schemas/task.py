from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from schemas.priority import PriorityRead
from models import Task


class TaskBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TaskCreate(TaskBase):
    name: str = Field(..., examples=["Task name"], min_length=3, max_length=100)
    description: str = Field(..., examples=["Task description"], min_length=3, max_length=1000)
    priority_id: int = Field(..., examples=[1], ge=1)


class TaskUpdate(TaskBase):
    name: Optional[str] = Field(None, examples=["Project name"], min_length=3, max_length=100)
    description: Optional[str] = Field(None, examples=["Project description"], min_length=3, max_length=1000)
    priority_id: Optional[int] = Field(None, examples=[1], ge=1)


class TaskRead(TaskBase):
    id: int
    name: str
    description: str
    date_created: date
    date_finished: Optional[date] = None
    timestamp: Optional[datetime] = None
    priority: PriorityRead

    @classmethod
    def from_task(cls, task: Task):
        return cls(
            id=task.id,
            name=task.name,
            description=task.description,
            date_created=task.date_created,
            date_finished=task.date_finished if task.date_finished is not None else None,
            timestamp=task.timestamp if task.timestamp is not None else None,
            priority=PriorityRead.from_priority(task.priority)
        )
