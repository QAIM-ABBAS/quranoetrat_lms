from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_role
from app.crud import student as student_crud
from app.core.exceptions import NotFoundError
from app.db.session import get_db
from app.schemas.student import StudentCreate, StudentRead, StudentUpdate

router = APIRouter(prefix="/students", tags=["students"])


@router.get(
    "",
    response_model=list[StudentRead],
    dependencies=[Depends(require_role("admin", "teacher"))],
)
async def list_students(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
) -> list[StudentRead]:
    return await student_crud.get_multi(db, skip=skip, limit=limit)


@router.get(
    "/{student_id}",
    response_model=StudentRead,
    dependencies=[Depends(require_role("admin", "teacher"))],
)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
) -> StudentRead:
    student = await student_crud.get(db, student_id)
    if student is None:
        raise NotFoundError("Student not found")
    return student


@router.post(
    "",
    response_model=StudentRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))],
)
async def create_student(
    payload: StudentCreate,
    db: AsyncSession = Depends(get_db),
) -> StudentRead:
    return await student_crud.create(db, payload)


@router.patch(
    "/{student_id}",
    response_model=StudentRead,
    dependencies=[Depends(require_role("admin"))],
)
async def update_student(
    student_id: int,
    payload: StudentUpdate,
    db: AsyncSession = Depends(get_db),
) -> StudentRead:
    student = await student_crud.get(db, student_id)
    if student is None:
        raise NotFoundError("Student not found")
    return await student_crud.update(db, student, payload)


@router.delete(
    "/{student_id}",
    dependencies=[Depends(require_role("admin"))],
)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    student = await student_crud.remove(db, student_id)
    if student is None:
        raise NotFoundError("Student not found")
    return {"message": "Student deleted successfully"}
