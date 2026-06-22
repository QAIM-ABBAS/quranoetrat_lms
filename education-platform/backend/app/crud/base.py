from __future__ import annotations

from typing import Any, Generic, TypeVar

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    async def get(self, db: AsyncSession, obj_id: int) -> ModelType | None:
        return await db.get(self.model, obj_id)

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
        **filters: Any,
    ) -> list[ModelType]:
        query = select(self.model).offset(skip).limit(limit)

        for field, value in filters.items():
            if value is not None:
                query = query.where(getattr(self.model, field) == value)

        result = await db.execute(query)
        return list(result.scalars().all())

    async def create(
        self,
        db: AsyncSession,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, obj_id: int) -> ModelType | None:
        obj = await self.get(db, obj_id)
        if obj is None:
            return None

        await db.delete(obj)
        await db.commit()
        return obj
