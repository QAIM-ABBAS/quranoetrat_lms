from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_role
from app.crud import teacher as teacher_crud
from app.db.session import get_db
from app.models.user import User
from app.schemas.teacher import TeacherCreate, TeacherRead, TeacherUpdate
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get(
    "",
    response_model=list[TeacherRead],
    dependencies=[Depends(require_role("admin"))],
)
async def list_teachers(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
) -> list[TeacherRead]:
    return await teacher_crud.get_multi(db, skip=skip, limit=limit)


@router.get(
    "/{teacher_id}",
    response_model=TeacherRead,
    dependencies=[Depends(require_role("admin"))],
)
async def get_teacher(
    teacher_id: int,
    db: AsyncSession = Depends(get_db),
) -> TeacherRead:
    teacher = await teacher_crud.get(db, teacher_id)
    if teacher is None:
        raise NotFoundError("Teacher not found")
    return teacher


@router.post(
    "",
    response_model=TeacherRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))],
)
async def create_teacher(
    payload: TeacherCreate,
    db: AsyncSession = Depends(get_db),
) -> TeacherRead:
    return await teacher_crud.create(db, payload)


@router.patch(
    "/{teacher_id}",
    response_model=TeacherRead,
    dependencies=[Depends(require_role("admin"))],
)
async def update_teacher(
    teacher_id: int,
    payload: TeacherUpdate,
    db: AsyncSession = Depends(get_db),
) -> TeacherRead:
    teacher = await teacher_crud.get(db, teacher_id)
    if teacher is None:
        raise NotFoundError("Teacher not found")
    return await teacher_crud.update(db, teacher, payload)


@router.delete(
    "/{teacher_id}",
    dependencies=[Depends(require_role("admin"))],
)
async def delete_teacher(
    teacher_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    teacher = await teacher_crud.remove(db, teacher_id)
    if teacher is None:
        raise NotFoundError("Teacher not found")
    return {"message": "Teacher deleted successfully"}
