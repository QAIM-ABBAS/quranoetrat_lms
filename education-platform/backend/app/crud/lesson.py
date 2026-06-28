from __future__ import annotations

from app.crud.base import CRUDBase
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate, LessonUpdate


class CRUDLesson(CRUDBase[Lesson, LessonCreate, LessonUpdate]):
    pass


lesson = CRUDLesson(Lesson)
