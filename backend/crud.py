from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas
from typing import List


# USER CRUD OPERATIONS
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: dict):
    db_user = models.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


# CLASS CRUD OPERATIONS
def get_class(db: Session, class_id: int):
    return db.query(models.Class).filter(models.Class.id == class_id).first()


def get_classes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Class).offset(skip).limit(limit).all()


def create_class(db: Session, class_: schemas.ClassCreate):
    db_class = models.Class(**class_.dict())
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class


def update_class(db: Session, class_id: int, class_update: schemas.ClassUpdate):
    db_class = get_class(db, class_id)
    if db_class:
        for field, value in class_update.dict(exclude_unset=True).items():
            setattr(db_class, field, value)
        db.commit()
        db.refresh(db_class)
    return db_class


def delete_class(db: Session, class_id: int):
    db_class = get_class(db, class_id)
    if db_class:
        db.delete(db_class)
        db.commit()
        return True
    return False


# LESSON CRUD OPERATIONS
def get_lesson(db: Session, lesson_id: int):
    return db.query(models.Lesson).filter(models.Lesson.id == lesson_id).first()


def get_lessons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lesson).offset(skip).limit(limit).all()


def create_lesson(db: Session, lesson: schemas.LessonCreate):
    db_lesson = models.Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


def update_lesson(db: Session, lesson_id: int, lesson_update: schemas.LessonUpdate):
    db_lesson = get_lesson(db, lesson_id)
    if db_lesson:
        for field, value in lesson_update.dict(exclude_unset=True).items():
            setattr(db_lesson, field, value)
        db.commit()
        db.refresh(db_lesson)
    return db_lesson


def delete_lesson(db: Session, lesson_id: int):
    db_lesson = get_lesson(db, lesson_id)
    if db_lesson:
        db.delete(db_lesson)
        db.commit()
        return True
    return False


# LESSON PROGRESS CRUD OPERATIONS
def get_lesson_progress(db: Session, student_id: int, lesson_id: int):
    return db.query(models.LessonProgress).filter(
        models.LessonProgress.student_id == student_id,
        models.LessonProgress.lesson_id == lesson_id
    ).first()


def get_lesson_progresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.LessonProgress).offset(skip).limit(limit).all()


def create_lesson_progress(db: Session, progress: schemas.LessonProgressCreate):
    # Check if the progress record already exists
    existing_progress = get_lesson_progress(db, progress.student_id, progress.lesson_id)
    if existing_progress:
        # Update the existing record instead of creating a new one
        return update_lesson_progress(
            db, 
            progress.student_id, 
            progress.lesson_id, 
            schemas.LessonProgressUpdate(is_completed=progress.is_completed)
        )
    
    db_progress = models.LessonProgress(**progress.dict())
    if progress.is_completed:
        from datetime import datetime
        db_progress.completed_at = datetime.utcnow()
    
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress


def update_lesson_progress(db: Session, student_id: int, lesson_id: int, progress_update: schemas.LessonProgressUpdate):
    db_progress = get_lesson_progress(db, student_id, lesson_id)
    if db_progress:
        for field, value in progress_update.dict(exclude_unset=True).items():
            setattr(db_progress, field, value)
        
        if progress_update.is_completed and db_progress.completed_at is None:
            from datetime import datetime
            db_progress.completed_at = datetime.utcnow()
        elif not progress_update.is_completed:
            db_progress.completed_at = None
        
        db.commit()
        db.refresh(db_progress)
    return db_progress


def delete_lesson_progress(db: Session, student_id: int, lesson_id: int):
    db_progress = get_lesson_progress(db, student_id, lesson_id)
    if db_progress:
        db.delete(db_progress)
        db.commit()
        return True
    return False


# CLASS ENROLLMENT FUNCTIONS
def enroll_student_to_class(db: Session, class_id: int, student_id: int):
    # Get the class and student to verify they exist
    class_ = get_class(db, class_id)
    student = get_user(db, student_id)
    
    if not class_ or not student or student.role != 'student':
        return False
    
    # Add student to class
    class_.students.append(student)
    db.commit()
    return True


def assign_teacher_to_class(db: Session, class_id: int, teacher_id: int):
    # Get the class and teacher to verify they exist
    class_ = get_class(db, class_id)
    teacher = get_user(db, teacher_id)
    
    if not class_ or not teacher or teacher.role != 'teacher':
        return False
    
    # Add teacher to class
    class_.teachers.append(teacher)
    db.commit()
    return True