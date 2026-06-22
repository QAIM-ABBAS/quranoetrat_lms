from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TeacherBase(BaseModel):
    first_name: str
    last_name: str
    phone: str | None = None
    department: str | None = None


class TeacherCreate(TeacherBase):
    user_id: int


class TeacherUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    department: str | None = None


class TeacherRead(TeacherBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
