from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime


Base = declarative_base()


# Association table for many-to-many relationship between classes and teachers
class_teachers = Table(
    'class_teachers',
    Base.metadata,
    Column('class_id', Integer, ForeignKey('classes.id'), primary_key=True),
    Column('teacher_id', Integer, ForeignKey('users.id'), primary_key=True)
)


# Association table for many-to-many relationship between classes and students
class_students = Table(
    'class_students',
    Base.metadata,
    Column('class_id', Integer, ForeignKey('classes.id'), primary_key=True),
    Column('student_id', Integer, ForeignKey('users.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # 'teacher' or 'student'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    taught_classes = relationship(
        'Class',
        secondary=class_teachers,
        back_populates='teachers'
    )
    enrolled_classes = relationship(
        'Class',
        secondary=class_students,
        back_populates='students'
    )
    lesson_progress = relationship('LessonProgress', back_populates='student')


class Class(Base):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    teachers = relationship(
        'User',
        secondary=class_teachers,
        back_populates='taught_classes'
    )
    students = relationship(
        'User',
        secondary=class_students,
        back_populates='enrolled_classes'
    )
    lessons = relationship('Lesson', back_populates='class')


class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String)  # Could be text or HTML content
    video_url = Column(String(500))  # URL to video content
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    class_ = relationship('Class', back_populates='lessons')
    progress = relationship('LessonProgress', back_populates='lesson')


class LessonProgress(Base):
    __tablename__ = 'lesson_progress'

    student_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), primary_key=True)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True))

    # Relationships
    student = relationship('User', back_populates='lesson_progress')
    lesson = relationship('Lesson', back_populates='progress')