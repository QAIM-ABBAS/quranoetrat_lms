from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_role
from app.core.exceptions import NotFoundError
from app.crud import enrollment as enrollment_crud
from app.db.session import get_db
from app.schemas.enrollment import (
    BulkEnrollmentRequest,
    BulkEnrollmentResponse,
    EnrollmentCreate,
    EnrollmentRead,
)
from app.services.enrollment_service import bulk_enroll, enroll, unenroll

router = APIRouter(prefix="/enrollments", tags=["enrollments"])


@router.get(
    "",
    response_model=list[EnrollmentRead],
    dependencies=[Depends(require_role("admin", "teacher", "student"))],
)
async def list_enrollments(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    school_class_id: int | None = None,
    student_id: int | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[EnrollmentRead]:
    return await enrollment_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        school_class_id=school_class_id,
        student_id=student_id,
    )


@router.post(
    "",
    response_model=EnrollmentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))],
)
async def create_enrollment(
    payload: EnrollmentCreate,
    db: AsyncSession = Depends(get_db),
) -> EnrollmentRead:
    return await enroll(db, payload.school_class_id, payload.student_id)


@router.post(
    "/bulk",
    response_model=BulkEnrollmentResponse,
    dependencies=[Depends(require_role("admin"))],
)
async def bulk_enrollment(
    payload: BulkEnrollmentRequest,
    db: AsyncSession = Depends(get_db),
) -> BulkEnrollmentResponse:
    return await bulk_enroll(db, payload.class_id, payload.student_ids)


@router.delete(
    "/{school_class_id}/{student_id}",
    dependencies=[Depends(require_role("admin"))],
)
async def delete_enrollment(
    school_class_id: int,
    student_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    deleted = await unenroll(db, school_class_id, student_id)
    if not deleted:
        raise NotFoundError("Enrollment not found")
    return {"message": "Enrollment deleted successfully"}
