from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_role
from app.core.exceptions import NotFoundError
from app.crud import lesson as lesson_crud
from app.db.session import get_db
from app.schemas.lesson import LessonCreate, LessonRead, LessonUpdate

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get(
    "",
    response_model=list[LessonRead],
    dependencies=[Depends(require_role("admin", "teacher"))],
)
async def list_lessons(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    school_class_id: int | None = None,
    teacher_id: int | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[LessonRead]:
    return await lesson_crud.get_multi(
        db,
        skip=skip,
        limit=limit,
        school_class_id=school_class_id,
        teacher_id=teacher_id,
    )


@router.get(
    "/{lesson_id}",
    response_model=LessonRead,
    dependencies=[Depends(require_role("admin", "teacher"))],
)
async def get_lesson(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
) -> LessonRead:
    lesson = await lesson_crud.get(db, lesson_id)
    if lesson is None:
        raise NotFoundError("Lesson not found")
    return lesson


@router.post(
    "",
    response_model=LessonRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))],
)
async def create_lesson(
    payload: LessonCreate,
    db: AsyncSession = Depends(get_db),
) -> LessonRead:
    return await lesson_crud.create(db, payload)


@router.patch(
    "/{lesson_id}",
    response_model=LessonRead,
    dependencies=[Depends(require_role("admin"))],
)
async def update_lesson(
    lesson_id: int,
    payload: LessonUpdate,
    db: AsyncSession = Depends(get_db),
) -> LessonRead:
    lesson = await lesson_crud.get(db, lesson_id)
    if lesson is None:
        raise NotFoundError("Lesson not found")
    return await lesson_crud.update(db, lesson, payload)


@router.delete(
    "/{lesson_id}",
    dependencies=[Depends(require_role("admin"))],
)
async def delete_lesson(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    lesson = await lesson_crud.remove(db, lesson_id)
    if lesson is None:
        raise NotFoundError("Lesson not found")
    return {"message": "Lesson deleted successfully"}
