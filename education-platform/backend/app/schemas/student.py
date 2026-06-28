from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    phone: str | None = None
    grade: str | None = None


class StudentCreate(StudentBase):
    user_id: int


class StudentUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    grade: str | None = None


class StudentRead(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
