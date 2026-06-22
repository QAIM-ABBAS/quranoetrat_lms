from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SchoolClassBase(BaseModel):
    name: str
    term: str
    description: str | None = None


class SchoolClassCreate(SchoolClassBase):
    pass


class SchoolClassUpdate(BaseModel):
    name: str | None = None
    term: str | None = None
    description: str | None = None


class SchoolClassRead(SchoolClassBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
