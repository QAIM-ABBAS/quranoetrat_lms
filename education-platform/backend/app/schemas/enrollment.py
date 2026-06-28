from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EnrollmentBase(BaseModel):
    school_class_id: int
    student_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentRead(EnrollmentBase):
    model_config = ConfigDict(from_attributes=True)

    enrolled_at: datetime


class BulkEnrollmentRequest(BaseModel):
    class_id: int
    student_ids: list[int]


class BulkEnrollmentResponse(BaseModel):
    class_id: int
    inserted: int
    skipped: int
