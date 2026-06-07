from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import controllers

from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return "Home page"

@app.post("/students")
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    return controllers.create_student(db, student)


@app.get("/students")
def get_students(
    db: Session = Depends(get_db)
):
    return controllers.get_students(db)


@app.get("/students/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = controllers.get_student(db, student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student