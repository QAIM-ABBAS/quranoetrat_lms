from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uvicorn
from . import models, schemas, database, auth, crud
from .database import engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LMS API", description="Learning Management System API", version="1.0.0")


@app.on_event("startup")
def startup_event():
    print("Starting up LMS API...")


@app.on_event("shutdown")
def shutdown_event():
    print("Shutting down LMS API...")


@app.get("/")
def read_root():
    return {"message": "Welcome to the LMS API!"}


# AUTHENTICATION ENDPOINTS
@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Register a new user"""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = auth.get_password_hash(user.password)
    user_dict = user.dict()
    user_dict['password_hash'] = hashed_password
    del user_dict['password']  # Remove plain password
    
    return crud.create_user(db=db, user=user_dict)


@app.post("/login", response_model=schemas.Token)
def login(credentials: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Login and return JWT token"""
    user = auth.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role.value},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# USER ENDPOINTS
@app.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(auth.get_current_active_user)):
    """Get current user info"""
    return current_user


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(database.get_db)):
    """Get user by ID"""
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# CLASS ENDPOINTS
@app.post("/classes/", response_model=schemas.Class)
def create_class(class_: schemas.ClassCreate, current_user: schemas.User = Depends(auth.get_current_teacher), db: Session = Depends(database.get_db)):
    """Create a new class (Teachers only)"""
    return crud.create_class(db=db, class_=class_)


@app.get("/classes/", response_model=List[schemas.Class])
def read_classes(skip: int = 0, limit: int = 100, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(database.get_db)):
    """Get all classes"""
    classes = crud.get_classes(db, skip=skip, limit=limit)
    return classes


@app.get("/classes/{class_id}", response_model=schemas.Class)
def read_class(class_id: int, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(database.get_db)):
    """Get class by ID"""
    class_ = crud.get_class(db, class_id=class_id)
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_


@app.put("/classes/{class_id}", response_model=schemas.Class)
def update_class(class_id: int, class_update: schemas.ClassUpdate, current_user: schemas.User = Depends(auth.get_current_teacher), db: Session = Depends(database.get_db)):
    """Update class (Teachers only)"""
    updated_class = crud.update_class(db, class_id=class_id, class_update=class_update)
    if not updated_class:
        raise HTTPException(status_code=404, detail="Class not found")
    return updated_class


@app.delete("/classes/{class_id}")
def delete_class(class_id: int, current_user: schemas.User = Depends(auth.get_current_teacher), db: Session = Depends(database.get_db)):
    """Delete class (Teachers only)"""
    deleted = crud.delete_class(db, class_id=class_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Class not found")
    return {"message": "Class deleted successfully"}


# LESSON ENDPOINTS
@app.post("/lessons/", response_model=schemas.Lesson)
def create_lesson(lesson: schemas.LessonCreate, current_user: schemas.User = Depends(auth.get_current_teacher), db: Session = Depends(database.get_db)):
    """Create a new lesson (Teachers only)"""
    return crud.create_lesson(db=db, lesson=lesson)


@app.get("/lessons/", response_model=List[schemas.Lesson])
def read_lessons(skip: int = 0, limit: int = 100, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(database.get_db)):
    """Get all lessons"""
    lessons = crud.get_lessons(db, skip=skip, limit=limit)
    return lessons


@app.get("/lessons/{lesson_id}", response_model=schemas.Lesson)
def read_lesson(lesson_id: int, current_user: schemas.User = Depends(auth.get_current_active_user), db: Session = Depends(database.get_db)):
    """Get lesson by ID"""
    lesson = crud.get_lesson(db, lesson_id=lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@app.put("/lessons/{lesson_id}", response_model=schemas.Lesson)
def update_lesson(lesson_id: int, lesson_update: schemas.LessonUpdate, current_user: schemas.User = Depends(auth.get_current_teacher), db: Session = Depends(database.get_db)):
    """Update lesson (Teachers only)"""
    updated_lesson = crud.update_lesson(db, lesson_id=lesson_id, lesson_update=lesson_update)
    if not updated_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return updated_lesson


@app.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: int, current_user: schemas.User = Depends(auth.get_current_teacher), db: Session = Depends(database.get_db)):
    """Delete lesson (Teachers only)"""
    deleted = crud.delete_lesson(db, lesson_id=lesson_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"message": "Lesson deleted successfully"}


# PROGRESS ENDPOINTS
@app.post("/progress/", response_model=schemas.LessonProgress)
def track_progress(progress: schemas.LessonProgressCreate, current_user: schemas.User = Depends(auth.get_current_student), db: Session = Depends(database.get_db)):
    """Track lesson progress (Students only)"""
    return crud.create_lesson_progress(db=db, progress=progress)


@app.put("/progress/{student_id}/{lesson_id}", response_model=schemas.LessonProgress)
def update_progress(student_id: int, lesson_id: int, progress_update: schemas.LessonProgressUpdate, current_user: schemas.User = Depends(auth.get_current_student), db: Session = Depends(database.get_db)):
    """Update lesson progress (Students only)"""
    updated_progress = crud.update_lesson_progress(db, student_id=student_id, lesson_id=lesson_id, progress_update=progress_update)
    if not updated_progress:
        raise HTTPException(status_code=404, detail="Progress record not found")
    return updated_progress


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)