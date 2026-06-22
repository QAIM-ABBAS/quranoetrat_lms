from __future__ import annotations

from app.crud.base import CRUDBase
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class CRUDStudent(CRUDBase[Student, StudentCreate, StudentUpdate]):
    pass


student = CRUDStudent(Student)
