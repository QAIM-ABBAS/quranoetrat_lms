from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    classes,
    enrollments,
    lessons,
    students,
    teachers,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(teachers.router)
api_router.include_router(students.router)
api_router.include_router(classes.router)
api_router.include_router(lessons.router)
api_router.include_router(enrollments.router)
