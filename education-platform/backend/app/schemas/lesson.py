from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LessonBase(BaseModel):
    school_class_id: int
    teacher_id: int
    subject: str
    description: str | None = None
    schedule_info: str | None = None


class LessonCreate(LessonBase):
    pass


class LessonUpdate(BaseModel):
    school_class_id: int | None = None
    teacher_id: int | None = None
    subject: str | None = None
    description: str | None = None
    schedule_info: str | None = None


class LessonRead(LessonBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
