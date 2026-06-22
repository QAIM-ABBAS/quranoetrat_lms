from __future__ import annotations

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.enrollment import Enrollment
from app.models.school_class import SchoolClass
from app.models.student import Student
from app.schemas.enrollment import BulkEnrollmentResponse


async def enroll(
    db: AsyncSession,
    school_class_id: int,
    student_id: int,
) -> Enrollment:
    school_class = await db.get(SchoolClass, school_class_id)
    if school_class is None:
        raise NotFoundError("School class not found")

    student = await db.get(Student, student_id)
    if student is None:
        raise NotFoundError("Student not found")

    existing = await db.execute(
        select(Enrollment).where(
            Enrollment.school_class_id == school_class_id,
            Enrollment.student_id == student_id,
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise ConflictError("Student is already enrolled in this class")

    enrollment = Enrollment(
        school_class_id=school_class_id,
        student_id=student_id,
    )
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment


async def bulk_enroll(
    db: AsyncSession,
    school_class_id: int,
    student_ids: list[int],
) -> BulkEnrollmentResponse:
    school_class = await db.get(SchoolClass, school_class_id)
    if school_class is None:
        raise NotFoundError("School class not found")

    student_ids = list(dict.fromkeys(student_ids))
    if not student_ids:
        return BulkEnrollmentResponse(
            class_id=school_class_id,
            inserted=0,
            skipped=0,
        )

    # Validate students before attempting bulk insert.
    seen_students = await db.execute(
        select(Student.id).where(Student.id.in_(student_ids))
    )
    valid_student_ids = set(seen_students.scalars().all())
    missing = [student_id for student_id in student_ids if student_id not in valid_student_ids]
    if missing:
        raise NotFoundError(
            f"Students not found: {', '.join(str(item) for item in missing)}"
        )

    stmt = (
        insert(Enrollment)
        .values(
            [
                {"school_class_id": school_class_id, "student_id": student_id}
                for student_id in student_ids
            ]
        )
        .on_conflict_do_nothing(
            index_elements=[Enrollment.school_class_id, Enrollment.student_id]
        )
    )

    result = await db.execute(stmt)
    await db.commit()

    inserted = result.rowcount or 0
    skipped = len(student_ids) - inserted
    return BulkEnrollmentResponse(
        class_id=school_class_id,
        inserted=inserted,
        skipped=skipped,
    )


async def unenroll(
    db: AsyncSession,
    school_class_id: int,
    student_id: int,
) -> bool:
    enrollment = await db.execute(
        select(Enrollment).where(
            Enrollment.school_class_id == school_class_id,
            Enrollment.student_id == student_id,
        )
    )
    enrollment_record = enrollment.scalar_one_or_none()
    if enrollment_record is None:
        return False

    await db.delete(enrollment_record)
    await db.commit()
    return True


async def get_roster(
    db: AsyncSession,
    school_class_id: int,
) -> list[Student]:
    school_class = await db.get(SchoolClass, school_class_id)
    if school_class is None:
        raise NotFoundError("School class not found")

    result = await db.execute(
        select(Student)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .where(Enrollment.school_class_id == school_class_id)
    )
    return list(result.scalars().all())
