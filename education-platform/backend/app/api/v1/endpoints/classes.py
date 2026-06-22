from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_role
from app.core.exceptions import NotFoundError
from app.crud import school_class as school_class_crud
from app.db.session import get_db
from app.schemas.school_class import (
    SchoolClassCreate,
    SchoolClassRead,
    SchoolClassUpdate,
)

router = APIRouter(prefix="/classes", tags=["classes"])


@router.get(
    "",
    response_model=list[SchoolClassRead],
    dependencies=[Depends(require_role("admin", "teacher", "student"))],
)
async def list_classes(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
) -> list[SchoolClassRead]:
    return await school_class_crud.get_multi(db, skip=skip, limit=limit)


@router.get(
    "/{class_id}",
    response_model=SchoolClassRead,
    dependencies=[Depends(require_role("admin", "teacher", "student"))],
)
async def get_class(
    class_id: int,
    db: AsyncSession = Depends(get_db),
) -> SchoolClassRead:
    school_class = await school_class_crud.get(db, class_id)
    if school_class is None:
        raise NotFoundError("Class not found")
    return school_class


@router.post(
    "",
    response_model=SchoolClassRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin"))],
)
async def create_class(
    payload: SchoolClassCreate,
    db: AsyncSession = Depends(get_db),
) -> SchoolClassRead:
    return await school_class_crud.create(db, payload)


@router.patch(
    "/{class_id}",
    response_model=SchoolClassRead,
    dependencies=[Depends(require_role("admin"))],
)
async def update_class(
    class_id: int,
    payload: SchoolClassUpdate,
    db: AsyncSession = Depends(get_db),
) -> SchoolClassRead:
    school_class = await school_class_crud.get(db, class_id)
    if school_class is None:
        raise NotFoundError("Class not found")
    return await school_class_crud.update(db, school_class, payload)


@router.delete(
    "/{class_id}",
    dependencies=[Depends(require_role("admin"))],
)
async def delete_class(
    class_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    school_class = await school_class_crud.remove(db, class_id)
    if school_class is None:
        raise NotFoundError("Class not found")
    return {"message": "Class deleted successfully"}
