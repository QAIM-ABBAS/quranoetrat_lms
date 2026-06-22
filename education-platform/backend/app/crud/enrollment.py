from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.enrollment import Enrollment
from app.models.school_class import SchoolClass
from app.models.student import Student
from app.schemas.enrollment import EnrollmentCreate, EnrollmentRead


class CRUDEnrollment(CRUDBase[Enrollment, EnrollmentCreate, EnrollmentCreate]):
    async def get_by_class_and_student(
        self,
        db: AsyncSession,
        *,
        school_class_id: int,
        student_id: int,
    ) -> Enrollment | None:
        result = await db.execute(
            select(Enrollment).where(
                Enrollment.school_class_id == school_class_id,
                Enrollment.student_id == student_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
        school_class_id: int | None = None,
        student_id: int | None = None,
    ) -> list[Enrollment]:
        query = select(Enrollment).offset(skip).limit(limit)
        if school_class_id is not None:
            query = query.where(Enrollment.school_class_id == school_class_id)
        if student_id is not None:
            query = query.where(Enrollment.student_id == student_id)
        result = await db.execute(query)
        return list(result.scalars().all())

    async def ensure_exists(
        self,
        db: AsyncSession,
        *,
        school_class_id: int,
        student_id: int,
    ) -> Enrollment:
        existing = await self.get_by_class_and_student(
            db,
            school_class_id=school_class_id,
            student_id=student_id,
        )
        if existing is not None:
            return existing

        enrollment = Enrollment(
            school_class_id=school_class_id,
            student_id=student_id,
        )
        db.add(enrollment)
        await db.commit()
        await db.refresh(enrollment)
        return enrollment


enrollment = CRUDEnrollment(Enrollment)
