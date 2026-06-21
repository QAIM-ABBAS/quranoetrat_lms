from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    teacher = "teacher"
    student = "student"


# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Class Schemas
class ClassBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ClassCreate(ClassBase):
    pass


class ClassUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class Class(ClassBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    teachers: List[User] = []
    students: List[User] = []

    class Config:
        orm_mode = True


# Lesson Schemas
class LessonBase(BaseModel):
    class_id: int
    title: str
    content: Optional[str] = None
    video_url: Optional[str] = None


class LessonCreate(LessonBase):
    pass


class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None


class Lesson(LessonBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    class_: Class

    class Config:
        orm_mode = True


# Lesson Progress Schemas
class LessonProgressBase(BaseModel):
    student_id: int
    lesson_id: int
    is_completed: bool = False


class LessonProgressCreate(LessonProgressBase):
    pass


class LessonProgressUpdate(BaseModel):
    is_completed: bool


class LessonProgress(LessonProgressBase):
    completed_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None